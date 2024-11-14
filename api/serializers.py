from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User
import re

class NoteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    created_at = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'author', 'created_at']
        extra_kwargs = {'author': {'read_only': True}}

    def get_author(self, obj):
        return obj.author.username

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}, 'confirm_password': {'write_only': True}}

    def validate_username(self, value):
        """ Check if the username is already taken """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_password(self, value):
        """ Validate password strength (e.g., min 8 characters, must contain at least one number and one letter) """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value

    def validate(self, data):
        """ Ensure the password and confirm password match """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """ Create a user with validated data """
        validated_data.pop('confirm_password')  # We don't need to store confirm_password
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user