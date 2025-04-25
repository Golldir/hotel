from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets

from hotel.services import HotelService
from hotel.serializers import HotelSerializer

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