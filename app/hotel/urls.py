from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelRoomViewSet, RoomBookingViewSet

router = DefaultRouter()
router.register(r'rooms', HotelRoomViewSet, basename='hotel_rooms')
router.register(r'bookings', RoomBookingViewSet, basename='hotel_bookings')

urlpatterns = [
    path('', include(router.urls)),
] 