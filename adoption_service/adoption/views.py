import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import AdoptionRequest
from adoption_service.utils import get_service_url
from adoption.messaging.producer import publish_adoption


# -------------------------------------------------------------------
# 🔐 ADMIN SECURITY CHECK
# -------------------------------------------------------------------
def is_admin(user):
    return user.is_authenticated and user.is_staff


# -------------------------------------------------------------------
# 🏠 HOME PAGE (CLIENT)
# -------------------------------------------------------------------
def home(request):
    return render(request, "client/home.html")


# -------------------------------------------------------------------
# 📝 CREATE ADOPTION REQUEST (CLIENT)
# -------------------------------------------------------------------
@login_required
def create_request(request):
    if request.method == "GET":
        return render(request, "client/form_adoption.html")

    if request.method == "POST":
        user_id = request.user.id       # secure: automatic user
        animal_id = request.POST.get("animal_id")
        appointment_id = request.POST.get("appointment_id")

        if not animal_id:
            return render(request, "client/form_adoption.html", {
                "error": "Animal ID is required."
            })

        req = AdoptionRequest.objects.create(
            user_id=user_id,
            animal_id=int(animal_id),
            appointment_id=int(appointment_id) if appointment_id else None,
            status="pending"
        )

        return render(request, "client/success_adoption.html", {"request": req})


# -------------------------------------------------------------------
# 📄 LIST USER REQUESTS (CLIENT)
# -------------------------------------------------------------------
@login_required
def user_requests(request, user_id):
    # Security: only owner can view their own requests
    if request.user.id != int(user_id):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    reqs = AdoptionRequest.objects.filter(user_id=user_id).order_by("-date_requested")
    return render(request, "client/liste_adoptions.html", {"reqs": reqs})


# -------------------------------------------------------------------
# 📌 REQUEST STATUS (OPTIONAL API)
# -------------------------------------------------------------------
def request_status(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)
        return JsonResponse({
            "id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id,
            "status": req.status,
            "date": req.date_requested
        })
    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


# -------------------------------------------------------------------
# 🗑 CANCEL REQUEST (CLIENT)
# -------------------------------------------------------------------
@login_required
def cancel_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        if req.user_id != request.user.id:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        if req.status != "pending":
            return JsonResponse({"error": "Cannot cancel a processed request"}, status=400)

        req.status = "cancelled"
        req.save()
        return JsonResponse({"success": True})

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)


# -------------------------------------------------------------------
# 🛑 ADMIN — LIST ALL REQUESTS
# -------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def admin_list(request):
    reqs = AdoptionRequest.objects.all().order_by("-date_requested")
    return render(request, "admin/admin_list.html", {"reqs": reqs})


# -------------------------------------------------------------------
# 🟢 ADMIN — APPROVE REQUEST
# -------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def approve_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        req.status = "approved"
        req.save()

        # Send RabbitMQ event
        publish_adoption({
            "event": "adoption_approved",
            "request_id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id
        })

        return redirect("/adoption/admin/requests/")

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)


# -------------------------------------------------------------------
# 🔴 ADMIN — REJECT REQUEST
# -------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def reject_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        req.status = "rejected"
        req.save()

        publish_adoption({
            "event": "adoption_rejected",
            "request_id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id
        })

        return redirect("/adoption/admin/requests/")

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)
