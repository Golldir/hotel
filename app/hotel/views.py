from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from hotel.serializers import RoomBookingSerializer, HotelRoomSerializer
from .services import HotelRoomService, RoomBookingService

# Create your views here.

@extend_schema(
    tags=["Номера отеля"]
)
class HotelRoomViewSet(viewsets.ViewSet):
    """
    Ручки для работы с номерами отеля
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_service = HotelRoomService()

    def list(self, request):
        """Получить список номеров отеля"""
        return self.room_service.get_all_rooms(request.data)

    def retrieve(self, request, pk=1):
        return self.room_service.get_room(pk)

    @extend_schema(request=HotelRoomSerializer, methods=["POST"])
    def create(self, request):
        """Добавить номер отеля"""
        return self.room_service.create_room(request.data)

    def destroy(self, request, pk=None):
        """Удалить номер отеля"""
        return self.room_service.delete_room(pk)

@extend_schema(
    tags=['Бронирование номеров']
)
class RoomBookingViewSet(viewsets.ViewSet):
    """
    Ручки для работы с бронированиями номеров
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booking_service = RoomBookingService()

    @action(detail=False, methods=['get'], url_path='by_id/(?P<booking_id>[^/.]+)')
    def get_by_id(self, request, booking_id: int) -> Response:
        """Получить бронирование по id"""
        return self.booking_service.get_booking_by_id(booking_id)

    @action(detail=False, methods=['get'], url_path='by_room/(?P<room_id>[^/.]+)')
    def get_by_room(self, request, room_id: int) -> Response:
        """Получить список всех бронирований по room_id"""
        return self.booking_service.get_bookings_by_room(room_id)

    def list(self, request):
        """Получить список всех бронирований номера"""
        return self.booking_service.get_all_bookings()

    @extend_schema(request=RoomBookingSerializer, methods=["POST"])
    def create(self, request, *args, **kwargs):
        """Создать новое бронирование"""
        return self.booking_service.create_booking(request.data)

    def destroy(self, request, pk=None):
        """Удалить бронирование"""
        return self.booking_service.delete_booking(pk)




