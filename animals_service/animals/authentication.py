from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth.models import User

class StatelessJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that does NOT check the local database for the user.
    Instead, it creates a transient (unsaved) User object from the token claims.
    """
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        # Create a transient user (not saved to DB)
        user = User()
        user.id = user_id
        user.pk = user_id
        user.username = validated_token.get('email', f'user_{user_id}')
        user.email = validated_token.get('email', '')
        user.is_active = True
        
        # Map claims to Django permissions
        user.is_staff = validated_token.get('is_staff', False)
        user.is_superuser = validated_token.get('is_admin', False) # Map is_admin to superuser for simplicity

        # Important: Allow this user to be "authenticated"
        return user
