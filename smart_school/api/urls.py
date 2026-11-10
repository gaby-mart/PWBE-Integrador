from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsUser import UserViewSet
from .viewsLaboratory import LaboratoryViewSet
from .viewsMicrocontroller import MicrocontrollerModelViewSet, MicrocontrollerViewSet
from .viewsMeasurementUnit import MeasuredUnitViewSet
from .viewSensor import SensorModelViewSet, SensorViewSet, SensorReadingViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .viewsAuth import CustomTokenObtainPairView, MeView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'laboratories', LaboratoryViewSet, basename='laboratories')
router.register(r'microcontroller-models', MicrocontrollerModelViewSet, basename='microcontroller-models')
router.register(r'microcontrollers', MicrocontrollerViewSet, basename='microcontrollers')
router.register(r'measurement-units', MeasuredUnitViewSet, basename='measurement-unit')
router.register(r'sensor-models', SensorModelViewSet, basename='sensor-models')
router.register(r'sensors', SensorViewSet, basename='sensors')
router.register(r'sensor-readings', SensorReadingViewSet, basename='sensor-readings')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
]