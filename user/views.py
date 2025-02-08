
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AdminRegisterSerializer
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_messages = serializer.errors
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(
            {'message':'User is succussfully Registered.'}
        )

class AdminRegistration(generics.CreateAPIView):
    serializer_class = AdminRegisterSerializer

    def validate(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        if not serializer.is_valid():
            error_messages = serializer.errors
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

class UserTestAuthenticationView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)

        return Response(serializer.data)