from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from .permissions import IsSuperUserOrAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django.db.models import Min, Max, Avg, Count
from .models import Sensor, SensorModel, SensorReading
from .serializers import SensorModelSerializer, SensorSerializer, SensorReadingSerializer
from rest_framework.pagination import PageNumberPagination

class SensorModelViewSet(viewsets.ModelViewSet):
    queryset = SensorModel.objects.all()
    serializer_class = SensorModelSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

#Páginação para o front
class ReadingsPagination(PageNumberPagination):
    page_size = 150  # Número de registros por página
    page_size_query_param = 'page_size'  
    max_page_size = 500  # Tamanho máximo da página

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer
    permission_classes = [IsSuperUserOrAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = {
        'sr_sen' : ['exact'], 
        'sr_measured_at' : ['gte', 'lte', 'date'], 
    }

    ordering_fields = ['sr_measured_value', 'sr_measured_at'] 
    ordering = ['-sr_measured_at']

    @action(detail=False, methods=['get'], url_path='statistics', url_name='statistics')
    def statistical_summary(self, request):
        raw_sensor_id = (
            request.query_params.get('sr_sen') or 
            request.query_params.get('sensor') or 
            request.query_params.get('sr_sen_id')
        )

        if not raw_sensor_id:
            return Response(
                {"error": "The parameter 'sr_sen' (or 'sensor') is mandatory in the query string."}, 
                status=400
            )

        try:
            clean_sensor_id = str(raw_sensor_id).replace('/', '').strip()
            sensor_id = int(clean_sensor_id)
        except ValueError:
            return Response(
                {"error": f"The sensor ID '{raw_sensor_id}' is invalid. It must be an integer."}, 
                status=400
            )

        readings = SensorReading.objects.filter(sr_sen_id=sensor_id)

        if not readings.exists():
            return Response(
                {"error": f"No readings found for the sensor with ID {sensor_id}."}, 
                status=404
            )

        stats = readings.aggregate(
            total_count=Count('sr_id'),
            min_value=Min('sr_measured_value'),
            max_value=Max('sr_measured_value'),
            average_value=Avg('sr_measured_value')
        )

        return Response({
            "sensor_id": sensor_id,
            "statistics": stats
        })

    @action(detail=False, methods=['get'], url_path='recents', url_name='recents')
    def recent_readings(self, request):
        time_limit = timezone.now() - timedelta(hours=24)
        readings = SensorReading.objects.filter(sr_measured_at__gte=time_limit).order_by('-sr_measured_at')
        
        serializer = self.get_serializer(readings, many=True)
        return Response({
            "period": "last_24_hours",
            "total_records": readings.count(),
            "results": serializer.data
        })

    @action(detail=False, methods=['get'], url_path='latest-per-sensor', url_name='latest_per_sensor')
    def latest_reading_per_sensor(self, request):
        latest_ids = (
            SensorReading.objects.values('sr_sen')
            .annotate(latest_date=Max('sr_measured_at'))
        )
        
        recent_readings_list = []
        for item in latest_ids:
            reading = SensorReading.objects.filter(
                sr_sen=item['sr_sen'], 
                sr_measured_at=item['latest_date']
            ).first()
            if reading:
                recent_readings_list.append(reading)

        serializer = self.get_serializer(recent_readings_list, many=True)
        return Response({
            "total_sensors": len(recent_readings_list),
            "results": serializer.data
        })