from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import viewsets

from hotel.services import RoomService
from hotel.serializers import RoomSerializer


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