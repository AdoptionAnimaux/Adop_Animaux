from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
from .models import User

# ==========================================
# 🖼 UI VIEWS (Stateless, REST compliant)
# ==========================================
# We serve the HTML templates here so the user has a "Frontend".
# These views do NOT use sessions for logic. They just return the HTML file.
# The HTML file then uses JS to talk to the API.

def login_page(request):
    return render(request, "accounts/login.html")

def register_page(request): 
    return render(request, "accounts/register.html")

def profile_page(request):
    return render(request, "accounts/profile.html")

def admin_dashboard_page(request):
    return render(request, "accounts/admin_dashboard.html")

def home_page(request):
    return render(request, "accounts/home.html")

# ==========================================
# 🔐 AUTH API (JWT)
# ==========================================

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)
    
    if user is not None:
        if not user.is_active:
            return Response({"error": "Account disabled"}, status=status.HTTP_403_FORBIDDEN)
            
        refresh = RefreshToken.for_user(user)
        # Add custom claims for Stateless Auth in other services
        refresh['email'] = user.email
        refresh['is_admin'] = user.is_admin
        refresh['is_staff'] = user.is_staff
        
        # Add custom claims to Access Token (Critical for Stateless Auth)
        access_token = refresh.access_token
        access_token['email'] = user.email
        access_token['is_admin'] = user.is_admin
        access_token['is_staff'] = user.is_staff
        
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'is_admin': user.is_admin
            }
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': "User created successfully",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ==========================================
# 👤 USER API (Protected)
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ==========================================
# 🛠 ADMIN API
# ==========================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_list_users(request):
    users = User.objects.all() # Show all users for admin
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.id == request.user.id:
        return Response({"error": "Cannot delete self"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.delete()
    return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return Response({
        "message": f"User status toggled. Active: {user.is_active}",
        "user_id": user.id,
        "is_active": user.is_active
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok"})
