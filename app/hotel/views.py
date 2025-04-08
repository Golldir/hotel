from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import HotelRoomService, RoomBookingService

# Create your views here.

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

    def retrieve(self, request, pk=None):
        return self.room_service.get_room(pk)

    def create(self, request):
        """Добавить номер отеля"""
        return self.room_service.create_room(request.data)

    def destroy(self, request, pk=None):
        """Удалить номер отеля"""
        return self.room_service.delete_room(pk)

class RoomBookingViewSet(viewsets.ViewSet):
    """
    Ручки для работы с бронированиями номеров
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booking_service = RoomBookingService()

    @action(detail=False, methods=['get'], url_path='by_id/(?P<booking_id>[^/.]+)')
    def get_by_id(self, request, booking_id) -> Response:
        """Получить бронирование по id"""
        return self.booking_service.get_booking_by_id(booking_id)

    @action(detail=False, methods=['get'], url_path='by_room/(?P<room_id>[^/.]+)')
    def get_by_room(self, request, room_id) -> Response:
        """Получить список всех бронирований по room_id"""
        return self.booking_service.get_bookings_by_room(room_id)

    def list(self, request):
        """Получить список всех бронирований номера"""
        return self.booking_service.get_all_bookings()

    def create(self, request):
        """Создать новое бронирование"""
        return self.booking_service.create_booking(request.data)

    def destroy(self, request, pk=None):
        """Удалить бронирование"""
        return self.booking_service.delete_booking(pk)




