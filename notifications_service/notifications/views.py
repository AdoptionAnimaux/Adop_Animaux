from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

# UI View
def ui_notifications_list(request):
    return render(request, "notifications/list.html")

# ==================================================
# 👤 USER API
# ==================================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    """
    Get notifications for the logged-in user.
    Uses request.user.id from the verified JWT.
    """
    notifications = Notification.objects.filter(
        user_id=request.user.id
    ).order_by("-created_at")
    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


# ==================================================
# 🛠 SYSTEM/ADMIN API
# ==================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})
