from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import re

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_check']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError("Username cannot exceed 150 characters")
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError("Email cannot exceed 254 characters")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")

        # Перевірка складності паролю
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter")

        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError({"password_check": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_check')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()