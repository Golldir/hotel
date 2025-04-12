from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='hotel_rooms')
router.register(r'bookings', BookingViewSet, basename='hotel_bookings')

urlpatterns = [
    path('', include(router.urls)),
] 