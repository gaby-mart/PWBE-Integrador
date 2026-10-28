from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from .models import MeasurementUnit
from .serializers import MeasuredUnitSerializer

class MeasuredUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasuredUnitSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]