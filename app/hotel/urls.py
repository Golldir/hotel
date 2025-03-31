from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelRoomViewSet

router = DefaultRouter()
router.register(r'rooms', HotelRoomViewSet, basename='hotel_rooms')

urlpatterns = [
    path('', include(router.urls)),
] 