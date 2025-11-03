from rest_framework import serializers
from .models import User
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'tr_number', 'role']


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['tr_number', 'password', 'confirm_password']

    def validate_tr_number(self, value):
        if not re.match(r'^\d{5}$', value):
            raise serializers.ValidationError("TR Number must be exactly 5 digits.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        tr_number = validated_data['tr_number']
        user = User.objects.create_user(
            tr_number=tr_number,
            username=tr_number,  # ✅ use TR No as username
            password=validated_data['password'],
            role='student'
        )
        return user
