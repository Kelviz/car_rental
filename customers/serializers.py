from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from .models import UserAccount


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('user_id', 'email', 'first_name', 'last_name', 'phone', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def validate_user_id(self, value):
        if UserAccount.objects.filter(id=value).exists():
            raise serializers.ValidationError("User ID already exists.")
        return value

    def create(self, validated_data):
        user = UserAccount.objects.create_user(**validated_data)
        return user
        

class UserSerializer(serializers.ModelSerializer):
        class Meta:
                model = UserAccount
                fields = ('user_id', 'email', 'first_name', 'last_name', 'phone')


class LoginSerializer(Serializer):
    email = CharField(required=True)
    password = CharField(required=True)