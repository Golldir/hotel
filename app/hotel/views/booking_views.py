from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets

from hotel.services import BookingService
from hotel.serializers import RoomSerializer, BookingSerializer


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