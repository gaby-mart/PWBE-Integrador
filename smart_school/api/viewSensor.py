from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from .models import Sensor, SensorModel, SensorReading
from .serializers import SensorModelSerializer, SensorSerializer, SensorReadingSerializer

class SensorModelViewSet(viewsets.ModelViewSet):
    queryset = SensorModel.objects.all()
    serializer_class = SensorModelSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]