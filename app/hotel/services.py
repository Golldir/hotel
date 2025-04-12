from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from .repositories import RoomRepository, BookingRepository
from .serializers import RoomSerializer, BookingSerializer
from .validators import validate_sort_params


class RoomService:
    """
    Сервисный слой для работы с номерами отеля
    """

    def __init__(self):
        self.room_repository = RoomRepository()

    def get_rooms(self, data):
        sort_column, sort_direction = validate_sort_params(data)

        sort_prefix = '-' if sort_direction == 'desc' else ''
        sort_expression = sort_prefix + sort_column

        rooms = self.room_repository.get_all_rooms(sort_expression)
        print('rooms', rooms)

        serializer = RoomSerializer(rooms, many=True)
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
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            result = self.room_repository.create_room(
                room_id=serializer.validated_data['room_id'],
                description=serializer.validated_data['description'],
                price_per_night=serializer.validated_data['price_per_night']
            )
            return Response(
                {'room_id': result.room_id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'status': 'error',
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete_room(self, room_id: int) -> Response:
        """Удалить номер отеля"""
        deleted_count = self.room_repository.delete_room(room_id)
        print('deleted_count', deleted_count[0])
        if not deleted_count[0]:
            return Response({
                'status': 'error',
                'message': 'Номер не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'message': f'Номер {room_id} успешно удален'},
            status=status.HTTP_200_OK
        )


class BookingService:
    """
    Сервисный слой для работы с бронированиями номеров
    """

    def __init__(self):
        self.booking_repository = BookingRepository()
        self.room_repository = RoomRepository()
        self.booking_serializer = BookingSerializer

    def get_bookings_by_room_id(self, data) -> Response:
        """Получить список всех бронирований"""
        room_id = data.get('room_id', None)
        if not room_id:
            return Response({
                'status': 'error',
                'message': 'Введите room_id /?room_id={room_id}'
            }, status=status.HTTP_404_NOT_FOUND)

        room = self.room_repository.get_room(room_id)
        if not room:
            return Response({
                'status': 'error',
                'message': 'Номер не существует'
            }, status=status.HTTP_404_NOT_FOUND)

        bookings = self.booking_repository.get_bookings_by_room(room_id)
        if not bookings:
            return Response({
                    'status': 'error',
                    "message": "У данной комнаты нет бронирований"
                },
                status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create_booking(self, data: Dict[str, Any]) -> Response:
        """
        Создать новое бронирование
        Args:
            data: словарь с данными бронирования (room, start_date, end_date)
        """
        serializer = self.booking_serializer(data=data)
        if serializer.is_valid():
            result = self.booking_repository.create_booking(
                room_id=serializer.validated_data['room_id'],
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date']
            )
            return Response(
                {'booking_id': result.booking_id},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'status': 'error',
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete_booking(self, booking_id: int) -> Response:
        """Удалить бронирование по booking_id"""
        deleted_count = self.booking_repository.delete_booking(booking_id)[0]
        print('deleted_count', deleted_count)
        if deleted_count == 0:
            return Response({
                'status': 'error',
                'message': 'Бронирование не найдено'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': f'Бронирование {booking_id} успешно удалено'},
            status=status.HTTP_200_OK
        )
