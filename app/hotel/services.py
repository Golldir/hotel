from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from .repositories import RoomRepository, BookingRepository, HotelRepository
from .serializers import RoomSerializer, BookingSerializer, HotelSerializer
from .validators import validate_sort_params


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

        serializer = self.booking_serializer(bookings, many=True)
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
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        room_id = serializer.validated_data['room_id']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        result = self.booking_repository.create_booking(
            room_id=room_id,
            start_date=start_date,
            end_date=end_date
        )
        return Response(
            {'booking_id': result.id},
            status=status.HTTP_201_CREATED
        )

    def delete_booking(self, booking_id: int) -> Response:
        """Удалить бронирование по booking_id"""
        deleted_count = self.booking_repository.delete_booking(booking_id)[0]
        if deleted_count == 0:
            return Response({
                'status': 'error',
                'message': 'Бронирование не найдено'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': f'Бронирование {booking_id} успешно удалено'},
            status=status.HTTP_200_OK
        )
