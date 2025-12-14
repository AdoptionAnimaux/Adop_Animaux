from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'is_admin', 'is_active']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'firstname', 'lastname']
    

    def create(self, validated_data):
        # Fix: User model has no create_user manager method
        user = User(
            email=validated_data['email'],
            firstname=validated_data.get('firstname', ''),
            lastname=validated_data.get('lastname', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
