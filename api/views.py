from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .models import Visita, Loja, Rito, Grau, Potencia
from .serializers import (
    VisitaSerializer, LojaSerializer, RitoSerializer,
    GrauSerializer, PotenciaSerializer
)

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Por favor, forneça usuário e senha'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {'error': 'Credenciais inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })

class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer

class RitoViewSet(viewsets.ModelViewSet):
    queryset = Rito.objects.all()
    serializer_class = RitoSerializer

class GrauViewSet(viewsets.ModelViewSet):
    queryset = Grau.objects.all()
    serializer_class = GrauSerializer

class PotenciaViewSet(viewsets.ModelViewSet):
    queryset = Potencia.objects.all()
    serializer_class = PotenciaSerializer

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.select_related('loja', 'rito', 'grau', 'potencia').all()
    serializer_class = VisitaSerializer
