from rest_framework import serializers
from .models import User, JobSeekerProfile, RecruiterProfile


# =========================
# USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "user_type",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# =========================
# JOB SEEKER PROFILE
# =========================
class JobSeekerProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_type = serializers.CharField(source="user.user_type", read_only=True)

    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = JobSeekerProfile
        fields = [
            "profile_image",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "bio",
            "skills",
            "experience",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None


# =========================
# RECRUITER PROFILE
# =========================
class RecruiterProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    user_type = serializers.CharField(source="user.user_type", read_only=True)

    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = RecruiterProfile
        fields = [
            "profile_image",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "company_name",
            "company_website",
        ]

    def get_profile_image(self, obj):
        request = self.context.get("request")
        if obj.profile_image:
            return request.build_absolute_uri(obj.profile_image.url)
        return None