from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
import requests

from .models import Animal
from .serializers import AnimalSerializer

# ==================================================
# 🖼 UI VIEWS
# ==================================================
# ==================================================
# 🖼 UI VIEWS
# ==================================================
def catalog_view(request):
    return render(request, "animals/catalog.html")

def admin_page(request):
    return render(request, "animals/admin_list.html")

# ==================================================
# 👤 CLIENT API (Public or Authenticated)
# ==================================================

class AnimalListCreateAPI(generics.ListCreateAPIView):
    """
    List animals (Public)
    Create animal (Propose animal - authenticated users)
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()] # List is public

    def perform_create(self, serializer):
        serializer.save(
            status='available', # Pending/Available logic
            submitted_by_user=True
        )


class AnimalRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (Public)
    Update/Delete (Owner or Admin)
    """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [AllowAny] # We handle granular permissions inside or override

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_update(self, serializer):
        # Only admin can update (since ownership is not tracked in Model)
        print(f"DEBUG: Update Animal. User={self.request.user.username}")
        
        if not self.request.user.has_perm('animals.change_animal'):
            raise PermissionDenied("Admin permission required")
            
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.has_perm('animals.delete_animal'):
             raise PermissionDenied("Admin permission required")
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_adoption_api(request, pk):
    """
    User requests to adopt an animal.
    Calls adoption_service.
    """
    animal = get_object_or_404(Animal, pk=pk)
    
    # Check if available
    if animal.status != 'available':
        return Response({"error": "Animal not available"}, status=400)
    
    return Response({"message": "Please use Adoption Service API to request adoption"}, status=302)


# ==================================================
# 🛠 ADMIN API
# ==================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_animal_api(request, pk):
    if not request.user.has_perm('animals.change_animal'):
        raise PermissionDenied("Admin permission required")
        
    animal = get_object_or_404(Animal, pk=pk)
    animal.status = 'available'
    animal.save()
    return Response({"message": "Animal approved/available"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_animal_api(request, pk):
    if not request.user.has_perm('animals.delete_animal'): # or change
        raise PermissionDenied("Admin permission required")
        
    animal = get_object_or_404(Animal, pk=pk)
    animal.status = 'rejected'
    animal.save()
    return Response({"message": "Animal rejected"})
