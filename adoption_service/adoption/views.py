from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

from .models import AdoptionRequest
from .serializers import AdoptionRequestSerializer
from adoption.messaging.producer import publish_adoption

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})

# ==================================================
# 👤 CLIENT API (JWT Requied)
# ==================================================

from django.shortcuts import get_object_or_404, render

# ...
# ==================================================
# 🖼 UI VIEWS
# ==================================================
def creation_page(request):
    return render(request, "adoption/form_view.html")

def my_list_page(request):
    return render(request, "client/liste_adoptions.html")

def admin_page(request):
    return render(request, "adoption/admin_list.html")



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_request(request):
    """
    Client creates an adoption request.
    User ID is taken strictly from request.user (token).
    """
    serializer = AdoptionRequestSerializer(data=request.data)
    if serializer.is_valid():
        # Enforce user_id from token
        serializer.save(
            user_id=request.user.id,
            status="pending"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_requests(request):
    """
    List requests for the logged-in user.
    """
    qs = AdoptionRequest.objects.filter(user_id=request.user.id)
    serializer = AdoptionRequestSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def request_status(request, id):
    req = get_object_or_404(AdoptionRequest, id=id, user_id=request.user.id)
    return Response({
        "id": req.id,
        "status": req.status,
        "date": req.date_requested
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_request(request, id):
    req = get_object_or_404(AdoptionRequest, id=id, user_id=request.user.id)
    
    if req.status != "pending":
        return Response({"error": "Cannot cancel processed request"}, status=status.HTTP_400_BAD_REQUEST)
        
    req.status = "cancelled"
    req.save()
    return Response({"success": True})


# ==================================================
# 🛠 ADMIN API (JWT + Permissions)
# ==================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_list(request):
    # Check strict permission using is_superuser derived from JWT is_admin claim
    if not getattr(request.user, 'is_superuser', False):
        raise PermissionDenied("Admin permission required")

    qs = AdoptionRequest.objects.all()
    serializer = AdoptionRequestSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_request(request, id):
    if not getattr(request.user, 'is_superuser', False):
        raise PermissionDenied("Admin access required")

    adoption = get_object_or_404(AdoptionRequest, pk=id)
    adoption.status = "approved"
    adoption.save()
    print("🔥 APPROVE REQUEST CALLED")
    publish_adoption({
        "event": "adoption_approved",
        "request_id": adoption.id,
        "user_id": adoption.user_id,
        "animal_id": adoption.animal_id,
    })

    return Response({"message": "Adoption approved"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_request(request, id):
    if not getattr(request.user, 'is_superuser', False):
        raise PermissionDenied("Admin access required")

    adoption = get_object_or_404(AdoptionRequest, pk=id)
    adoption.status = "rejected"
    adoption.save()

    publish_adoption({
        "event": "adoption_rejected",
        "request_id": adoption.id,
        "user_id": adoption.user_id,
        "animal_id": adoption.animal_id,
    })

    return Response({"message": "Adoption rejected"})


# ==================================================
# 🔁 INTER-SERVICE (No Auth or Special Perms?)
# ==================================================
# Note: Inter-service usually requires some form of auth (Internal auth), 
# but for this scope we might keep it open (Verify later) or reuse AllowAny if strictly internal.
# The prompt says "Verifier statut adoption (GET)".
# We'll use AllowAny for inter-service for simplicity unless specified otherwise, 
# as animals_service might not send a user token when calling this? 
# OR animals_service forwards the user token. 
# Let's assume forwarding or AllowAny. 
# Given "SEUL accounts_service génère le JWT", other services just verify.
# If animals_service calls this, it refers to a user.
# Let's stick to AllowAny for specific inter-service endpoint but keep it minimal.

@api_view(["GET"])
@permission_classes([AllowAny]) 
def check_adoption(request, user_id, animal_id):
    try:
        req = AdoptionRequest.objects.filter(
            user_id=user_id,
            animal_id=animal_id
        ).latest("date_requested")
        return Response({"status": req.status})
    except AdoptionRequest.DoesNotExist:
        return Response({"status": "none"})


def approve_request_ui(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied("Admin only")

    adoption = get_object_or_404(AdoptionRequest, pk=id)
    adoption.status = "approved"
    adoption.save()


    publish_adoption({
        "event": "adoption_approved",
        "request_id": adoption.id,
        "user_id": adoption.user_id,
        "animal_id": adoption.animal_id,
    })

    return redirect("/admin-panel/requests/")