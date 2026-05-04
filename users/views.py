from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from users import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import serializers as drf_serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import JobSeekerProfileSerializer, RecruiterProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser


# =========================
# REGISTER
# =========================
RegistrationSuccess = inline_serializer(
    name="RegistrationSuccess",
    fields={"message": drf_serializers.CharField()},
)

RegistrationError = inline_serializer(
    name="RegistrationError",
    fields={"error": drf_serializers.DictField()},
)

@extend_schema(
    summary="Register a new user",
    tags=["Authentication"],
    request=serializers.UserSerializer,
    responses={201: RegistrationSuccess, 400: RegistrationError},
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = serializers.UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "registered successful"}, status=201)
    else:
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

    if user is None:
        return Response({"error": "invalid credentials"}, status=401)

    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)

    return Response({
    "message": "signin successful",
    "access_token": str(access),
    "refresh_token": str(refresh),
    "user_type": user.user_type,   # ✅ ADD THIS
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
            serializer = JobSeekerProfileSerializer(profile)
        else:
            profile = user.recruiterprofile
            serializer = RecruiterProfileSerializer(profile)

        return Response(serializer.data)

    except Exception:
        return Response({"error": "Profile not found"}, status=404)


# =========================
# UPDATE PROFILE
# =========================
@api_view(['PATCH', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    user = request.user
    parser_classes = [MultiPartParser, FormParser]

    if user.user_type == "job_seeker":
        profile = user.jobseekerprofile
        serializer = JobSeekerProfileSerializer(profile, data=request.data, partial=True)
    else:
        profile = user.recruiterprofile
        serializer = RecruiterProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)