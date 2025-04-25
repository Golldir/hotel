from typing import List

from hotel.models import Booking


class BookingRepository:
    """
    Репозиторий для работы с бронированиями номеров
    """

    def get_bookings_by_room(self, room_id: int) -> List[Booking]:
        """Получить все бронирования по room_id"""
        return Booking.objects.filter(room_id=room_id).order_by('start_date')

    def create_booking(self, room_id: int, start_date: str, end_date: str) -> Booking:
        """Создать новое бронирование"""
        return Booking.objects.create(
            room_id=room_id,
            start_date=start_date,
            end_date=end_date
        )

    def delete_booking(self, booking_id: int):
        """Удалить бронирование по booking_id"""
        return Booking.objects.filter(pk=booking_id).delete()