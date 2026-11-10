from django.shortcuts import render
from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from .models import User
from .serializers import UserSerializer

from rest_framework.exceptions import PermissionDenied

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if user and user.is_authenticated and user.is_superuser:
            return User.objects.all()
        elif user and user.is_authenticated and user.is_staff:
            raise PermissionDenied("Apenas superusuários podem acessar a lista de usuários.")
        else:
            raise PermissionDenied("Você não tem permissão para acessar a lista de usuários.")
        

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Apenas superusuários podem criar novos usuários.")
        serializer.save()

