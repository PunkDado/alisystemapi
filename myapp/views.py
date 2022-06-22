from distutils.log import error
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, UsuarioSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Usuario, Login
from .serializers import UserSerializer, LoginSerializer

class UsuarioApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'id': request.data.get('id'),
            'nome': request.data.get('nome'),
            'login': request.data.get('login'),
            'senha': request.data.get('senha'),
            'perfil': request.data.get('perfil')
        }
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):

    def get(self, request, *args, **kwargs):
        logins = Login.objects.all()
        serializer = LoginSerializer(logins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'login': request.data.get('login'),
            'senha': request.data.get('senha')
        }
        login_serializer = LoginSerializer(data=data)
        usuario = Usuario.objects.filter(login = request.data.get('login'))
        usuario_request = {
            'id': usuario[0].id,
            'nome': usuario[0].nome,
            'login': usuario[0].login,
            'senha': usuario[0].senha,
            'perfil': usuario[0].perfil
        }
        if request.data.get('senha') == usuario[0].senha:
            user_serializer = UsuarioSerializer(data=usuario_request)
            if user_serializer.is_valid():
                if login_serializer.is_valid(): 
                    login_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if login_serializer.is_valid():
            return Response(login_serializer.errors, status=status.HTTP_403_FORBIDDEN)
        return Response(login_serializer.errors, status=status.HTTP_403_FORBIDDEN)