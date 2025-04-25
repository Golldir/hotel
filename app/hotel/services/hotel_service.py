from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from hotel.repositories import HotelRepository
from hotel.serializers import HotelSerializer


class HotelService:
    """
    Сервисный слой для работы с отелями
    """

    def __init__(self):
        self.hotel_repository = HotelRepository()
        self.hotel_serializer = HotelSerializer

    def get_hotels(self):
        """Получить список всех отелей"""

        hotels = self.hotel_repository.get_all_hotels()
        serializer = self.hotel_serializer(hotels, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create_hotel(self, data: Dict[str, Any]) -> Response:
        """Создать новый отель"""

        serializer = self.hotel_serializer(data=data)
        if serializer.is_valid():
            result = self.hotel_repository.create_hotel(
                name=serializer.validated_data['name']
            )
            return Response(
                {'hotel_id': result.id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'status': 'error',
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete_hotel(self, pk: int) -> Response:
        """Удалить отель"""

        deleted_count = self.hotel_repository.delete_hotel(pk)[0]
        if not deleted_count:
            return Response({
                'status': 'error',
                'message': 'Отель не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'message': f'Отель {pk} успешно удален'},
            status=status.HTTP_200_OK
        )