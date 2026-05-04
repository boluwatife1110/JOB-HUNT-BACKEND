from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema

from users import serializers
from .serializers import JobSeekerProfileSerializer, RecruiterProfileSerializer


# =========================
# REGISTER
# =========================
@extend_schema(summary="Register a new user", tags=["Authentication"])
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "registered successfully"}, status=201)

    return Response({"errors": serializer.errors}, status=400)


# =========================
# SIGNIN
# =========================
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if not user:
        return Response({"error": "invalid credentials"}, status=401)

    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "signin successful",
        "access_token": str(access),
        "refresh_token": str(refresh),
        "user_type": user.user_type,
    })


# =========================
# GET PROFILE
# =========================
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    user = request.user

    try:
        if user.user_type == "job_seeker":
            profile = user.jobseekerprofile
            serializer = JobSeekerProfileSerializer(
                profile,
                context={"request": request}
            )
        else:
            profile = user.recruiterprofile
            serializer = RecruiterProfileSerializer(
                profile,
                context={"request": request}
            )

        return Response(serializer.data)

    except Exception:
        return Response({"error": "Profile not found"}, status=404)


# =========================
# UPDATE PROFILE
# =========================
@api_view(['PATCH', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile(request):
    user = request.user

    if user.user_type == "job_seeker":
        profile = user.jobseekerprofile
        serializer = JobSeekerProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )
    else:
        profile = user.recruiterprofile
        serializer = RecruiterProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)