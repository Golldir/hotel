from typing import Dict, Any

from rest_framework import status
from rest_framework.response import Response

from hotel.repositories import BookingRepository, RoomRepository
from hotel.serializers import BookingSerializer

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