
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'message':'User is succussfully Registered.'}
        )

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response