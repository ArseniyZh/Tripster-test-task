from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from user.schemas import registration_params, token_schema


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=registration_params,
        responses={200: token_schema},
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).first():
            return Response({"error": "Username already exist"})

        user = User.objects.create_user(username=username, password=password)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
