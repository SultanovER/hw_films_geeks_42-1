from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserBaseValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserAuthSerializer(UserBaseValidateSerializer):
    pass

class UserRegisterSerializer(UserBaseValidateSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError("User already exists")