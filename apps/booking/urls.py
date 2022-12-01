from django.urls import path, register_converter, include
from rest_framework import routers
from apps.booking.infrastructure.ping_view import PingView
from .converters import DateParamConverter
from .views import AvailabilityView
from .viewsets import HotelViewSet, RoomViewSet, RateViewSet, InventoryViewSet

app_name = 'booking'

router = routers.DefaultRouter()
router.register(r'hotel', HotelViewSet)
router.register(r'room', RoomViewSet)
router.register(r'rate', RateViewSet)
router.register(r'inventory', InventoryViewSet)

# this line creates a new data type inside url patterns <date:str-date>
register_converter(DateParamConverter, 'date')


urlpatterns = [
    path('ping', PingView.as_view()),
    path('api/', include(router.urls)),
    path('availability/<str:code>/<date:checkin>/<date:checkout>/', AvailabilityView.as_view(), name='availability')
]
