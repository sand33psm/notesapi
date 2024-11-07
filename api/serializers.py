from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User

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
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):   
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
