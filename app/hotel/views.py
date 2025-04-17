from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets

from .serializers import BookingSerializer, RoomSerializer, HotelSerializer
from .services import RoomService, BookingService, HotelService


@extend_schema(
    tags=['Отели']
)
class HotelViewSet(viewsets.ViewSet):
    """
    Ручки для работы с отелями
    """

    def __init__(self, **kwargs):
        self.hotel_service = HotelService()
        super().__init__(**kwargs)

    @extend_schema(
        request=HotelSerializer
    )
    def list(self, request):
        """Получить список всех отелей"""
        return self.hotel_service.get_hotels()

    @extend_schema(
        request=HotelSerializer,
        methods=["POST"],
        examples=[
            OpenApiExample(
                name="Пример бронирования",
                value={
                    "name": "Отель Гранд Будапешт",
                }
            )
        ]
    )
    def create(self, request):
        """Создать новое бронирование"""
        return self.hotel_service.create_hotel(request.data)

    def destroy(self, request, pk: int):
        """Удалить бронирование"""
        return self.hotel_service.delete_hotel(pk)


@extend_schema(
    tags=["Номера отеля"]
)
class RoomViewSet(viewsets.ViewSet):
    """
    Ручки для работы с номерами отеля
    """
    def __init__(self, **kwargs):
        self.room_service = RoomService()
        super().__init__(**kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='hotel_id', description='hotel_id',
                             required=True, type=str),
            OpenApiParameter(name='sort_by', description='Сортировать по колонке (price_per_night, created_at)',
                             required=False, type=str),
            OpenApiParameter(name='order', description='Направление сортировки (asc, desc)', required=False, type=str)
        ]
    )
    def list(self, request):
        """Получить список номеров отеля"""
        return self.room_service.get_rooms(request.query_params)

    @extend_schema(
        request=RoomSerializer,
        methods=["POST"],
        examples=[
            OpenApiExample(
                name="Пример создания номера отеля",
                value={
                    "hotel_id": 7,
                    "room_number" : 7,
                    "description": "Люксовый отель",
                    "price_per_night": "150.00"
                },
                request_only=True
            )
        ]
    )
    def create(self, request):
        """Добавить номер отеля"""
        return self.room_service.create_room(request.data)

    def destroy(self, request, pk):
        """Удалить номер отеля"""
        return self.room_service.delete_room(pk)


@extend_schema(
    tags=['Бронирование номеров']
)
class BookingViewSet(viewsets.ViewSet):
    """
    Ручки для работы с бронированиями номеров
    """

    def __init__(self, **kwargs):
        self.booking_service = BookingService()
        super().__init__(**kwargs)

    @extend_schema(
        request=RoomSerializer,
        parameters=[
            OpenApiParameter(name='room_id', description='ID номера отеля', required=False, type=str),
        ]
    )
    def list(self, request):
        """Получить список всех бронирований номера по room_id"""
        return self.booking_service.get_bookings_by_room_id(request.query_params)

    @extend_schema(
        request=BookingSerializer,
        methods=["POST"],
        examples=[
            OpenApiExample(
                name="Пример бронирования",
                value={
                    "room_id": 15,
                    "start_date": "2025-04-12",
                    "end_date": "2025-04-15"
                },
                request_only=True
            )
        ]
    )
    def create(self, request):
        """Создать новое бронирование"""
        return self.booking_service.create_booking(request.data)

    def destroy(self, request, pk):
        """Удалить бронирование"""
        return self.booking_service.delete_booking(pk)
