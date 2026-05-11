from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone", "password", "password2"]
        extra_kwargs = {"password": {'write_only': True}}

    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("phone must be 11 digits")
        if not value.is_digit():
            raise serializers.ValidationError("phone must be digit")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("password and password2 not equal")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["phone", "date_joined"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError("The new password is the same as the current password.")
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError("new password and confirm password not equal")
        return attrs

    def save(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh_token"]
        return attrs

    def save(self, **kwargs):
        try:
            refresh_toke = RefreshToken(self.token)
            refresh_toke.blacklist()
        except TokenError:
            raise serializers.ValidationError({"detail": "Token is invalid or expired"})
