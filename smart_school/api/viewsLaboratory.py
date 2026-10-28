from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from .models import Laboratory
from .serializers import LaboratorySerializer

class LaboratoryViewSet(viewsets.ModelViewSet):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]