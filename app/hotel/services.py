from typing import Dict, Any, List

from rest_framework import status
from rest_framework.response import Response

from .models import HotelRoom, RoomBooking
from .repositories import HotelRoomRepository, RoomBookingRepository
from .serializers import HotelRoomSerializer, RoomBookingSerializer


class HotelRoomService:
    """
    Сервисный слой для работы с номерами отеля
    """

    def __init__(self):
        self.room_repository = HotelRoomRepository()

    def get_room(self, room_id: int) -> Response:
        """Получить номер по id"""
        room = self.room_repository.get_room(room_id)
        if not room:
            return Response({
                'status': 'error',
                'message': 'Номер не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = HotelRoomSerializer(room)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def get_all_rooms(self, data: Dict[str, Any]) -> Response:
        """Получить список всех номеров"""
        sort_column = data.get('sort_by', 'created_at')
        sort_direction = data.get('order', 'asc')

        sort_prefix = '-' if sort_direction == 'desc' else ''
        sort_expression = sort_prefix + sort_column

        rooms = self.room_repository.get_all_rooms(sort_expression)
        serializer = HotelRoomSerializer(rooms, many=True)
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
        serializer = HotelRoomSerializer(data=data)
        if serializer.is_valid():
            result = self.room_repository.create_room(
                description=serializer.validated_data['description'],
                price_per_night=serializer.validated_data['price_per_night']
            )
            return Response(
                {'id': result.id},
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

        if not deleted_count:
            return Response({
                'status': 'error',
                'message': 'Номер не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'message': f'Номер {room_id} успешно удален'},
            status=status.HTTP_204_NO_CONTENT
        )


class RoomBookingService:
    """
    Сервисный слой для работы с бронированиями номеров
    """

    def __init__(self):
        self.booking_repository = RoomBookingRepository()
        self.room_repository = HotelRoomRepository()

    def get_booking_by_id(self, booking_id: int) -> Response:
        """Получить бронирование по id"""
        booking = self.booking_repository.get_booking_by_id(booking_id)

        if not booking:
            return Response({
                'status': 'error',
                'message': 'Бронирование не найдено'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomBookingSerializer(booking)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def get_bookings_by_room(self, room_id: int) -> Response:
        """Получить список бронирований номера"""
        room = self.room_repository.get_room(room_id)

        if not room:
            return Response({
                'status': 'error',
                'message': 'Номер не найден'
            }, status=status.HTTP_404_NOT_FOUND)

        bookings = self.booking_repository.get_bookings_by_room(room_id)
        serializer = RoomBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_all_bookings(self) -> Response:
        """Получить список всех бронирований"""
        bookings = self.booking_repository.get_all_bookings()
        serializer = RoomBookingSerializer(bookings, many=True)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def create_booking(self, data: Dict[str, Any]) -> Response:
        """
        Создать новое бронирование
        Args:
            data: словарь с данными бронирования (room, start_date, end_date)
        """
        serializer = RoomBookingSerializer(data=data)
        if serializer.is_valid():
            result = self.booking_repository.create_booking(
                room_id=serializer.validated_data['room_id'],
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date']
            )
            return Response(
                {'id': result.id},
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
        """Удалить бронирование"""
        deleted_count = self.booking_repository.delete_booking(booking_id)

        if deleted_count == 0:
            return Response({
                'status': 'error',
                'message': 'Бронирование не найдено'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {'message': f'Бронирование {booking_id} успешно удалено'},
            status=status.HTTP_204_NO_CONTENT
        )
