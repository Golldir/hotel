from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet, HotelViewSet

router = DefaultRouter()
router.register(r'hotel', HotelViewSet, basename='hotels')
router.register(r'room', RoomViewSet, basename='rooms')
router.register(r'booking', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
