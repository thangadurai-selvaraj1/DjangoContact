import jwt
from django.conf import settings
from django.contrib import auth
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializar import UserSerializer


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode({'username': user.username}, 'settings.JWT_SECRET_KEY')

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}
            return Response(data=data, status=status.HTTP_200_OK)
        if username == '':
            return Response(data={'error': {'username': 'enter valid username'}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': 'enter valid username / password'}, status=status.HTTP_400_BAD_REQUEST)
