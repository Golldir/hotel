from typing import List
from hotel.models import Room, Booking


class RoomRepository:
    """
    Репозиторий для работы с номерами отеля
    """
    def get_room(self, room_id: int) -> Room:
        """Получить все номера с сортировкой"""
        return Room.objects.filter(room_id=room_id).first()

    def get_all_rooms(self, sort_expression: str) -> List[Room]:
        """Получить все номера с сортировкой"""
        return Room.objects.all().order_by(f'{sort_expression}')

    def create_room(self, room_id: int, description: str, price_per_night: float) -> Room:
        """Создать новый номер отеля"""
        return Room.objects.create(
            room_id=room_id,
            description=description,
            price_per_night=price_per_night
        )

    def delete_room(self, room_id: int):
        """Удалить номер отеля"""
        return Room.objects.filter(pk=room_id).delete()


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





