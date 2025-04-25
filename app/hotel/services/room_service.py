from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from hotel.repositories import RoomRepository, HotelRepository
from hotel.serializers import RoomSerializer
from hotel.validators import validate_sort_params


class RoomService:
    """
    Сервисный слой для работы с номерами отеля
    """

    def __init__(self):
        self.room_repository = RoomRepository()
        self.room_serializer = RoomSerializer
        self.hotel_repository = HotelRepository()

    def get_rooms(self, data):
        """Получить комнаты отеля"""

        hotel_id = data.get('hotel_id', None)
        if not hotel_id:
            return Response({
                'status': 'error',
                'message': 'Введите hotel_id /?hotel_id={hotel_id}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        hotel_exists = self.hotel_repository.hotel_exists(hotel_id)
        if not hotel_exists:
            return Response({
                'status': 'error',
                'message': 'Такого отеля не существует'},
                status=status.HTTP_404_NOT_FOUND
            )

        sort_column, sort_direction = validate_sort_params(data)

        sort_prefix = '-' if sort_direction == 'desc' else ''
        sort_expression = sort_prefix + sort_column

        rooms = self.room_repository.get_all_rooms(sort_expression, hotel_id)

        serializer = self.room_serializer(rooms, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create_room(self, data: Dict[str, Any]) -> Response:
        """
        Создать новый номер отеля
        Args:
            data: словарь с данными номера (description, price_per_night)
        """
        serializer = self.room_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        room_number = serializer.validated_data['room_number']
        hotel_id = serializer.validated_data['hotel_id']
        description = serializer.validated_data['description']
        price_per_night = serializer.validated_data['price_per_night']

        room_exists = self.room_repository.room_exists(room_number, hotel_id.id)
        if room_exists:
            return Response(
                {
                    'status': 'error',
                    'message': f'Номер с room_number = {room_number} в отеле c hotel_id = {hotel_id.id} существует'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        room = self.room_repository.create_room(
            room_number=room_number,
            hotel_id=hotel_id,
            description=description,
            price_per_night=price_per_night
        )

        return Response(
            {'id': room.id},
            status=status.HTTP_201_CREATED
        )

    def delete_room(self, room_id: int) -> Response:
        """Удалить номер отеля"""
        deleted_count = self.room_repository.delete_room(room_id)[0]
        if not deleted_count:
            return Response({
                'status': 'error',
                'message': 'Номер не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'message': f'Номер {room_id} успешно удален'},
            status=status.HTTP_200_OK
        )