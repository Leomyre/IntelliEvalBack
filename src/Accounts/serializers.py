from rest_framework import serializers
from .models import User, StudentProfile, TeacherProfile, AdminProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["student_id", "major"]

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ["teacher_id", "department"]

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ["admin_id"]
