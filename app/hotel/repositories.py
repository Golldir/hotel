from typing import List
from hotel.models import Room, Booking, Hotel


class HotelRepository:
    """
    Репозиторий для работы с отелями
    """

    def hotel_exists(self, hotel_id: int) -> bool:
        """Существует ли отель"""
        return Hotel.objects.filter(id=hotel_id).exists()

    def get_all_hotels(self) -> Hotel:
        """Получить все отели"""
        return Hotel.objects.all()

    def create_hotel(self, name: str) -> Hotel:
        """Создать отель"""
        return Hotel.objects.create(
            name=name
        )

    def delete_hotel(self, pk: int) -> None:
        """Удалить отель"""
        return Hotel.objects.filter(pk=pk).delete()


class RoomRepository:
    """
    Репозиторий для работы с номерами отеля
    """

    def room_exists(self, room_number: int, hotel_id: int) -> bool:
        """Проверить существование номера в отеле"""
        return Room.objects.filter(room_number=room_number, hotel_id=hotel_id).exists()

    def get_room(self, room_id: int) -> Room:
        """Получить все номера с сортировкой"""
        return Room.objects.filter(id=room_id)

    def get_all_rooms(self, sort_expression: str, hotel_id: int) -> List[Room]:
        """Получить все номера с сортировкой"""
        return Room.objects.filter(hotel_id=hotel_id).order_by(f'{sort_expression}')

    def create_room(
            self,
            room_number: int,
            hotel_id: int,
            description: str,
            price_per_night: float
    ) -> Room:
        """Создать новый номер отеля"""
        return Room.objects.create(
            hotel_id=hotel_id,
            room_number=room_number,
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
