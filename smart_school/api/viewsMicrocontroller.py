from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from .models import MicrocontrollerModel, Microcontroller
from .serializers import MicrocontrollerModelSerializer, MicrocontrollerSerializer

class MicrocontrollerModelViewSet(viewsets.ModelViewSet):
    queryset = MicrocontrollerModel.objects.all()
    serializer_class = MicrocontrollerModelSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

class MicrocontrollerViewSet(viewsets.ModelViewSet):
    queryset = Microcontroller.objects.all()
    serializer_class = MicrocontrollerSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]
