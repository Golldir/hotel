from typing import List, Optional
from hotel.models import HotelRoom, RoomBooking
from rest_framework.decorators import action

class HotelRoomRepository:
    """
    Репозиторий для работы с номерами отеля
    """
    def get_room(self, room_id: int) -> HotelRoom:
        """Получить все номера с сортировкой"""
        return HotelRoom.objects.filter(id=room_id)

    def get_all_rooms(self, sort_expression: str) -> List[HotelRoom]:
        """Получить все номера с сортировкой"""
        return HotelRoom.objects.all().order_by(f'{sort_expression}')

    def create_room(self, description: str, price_per_night: float) -> HotelRoom:
        """Создать новый номер отеля"""
        return HotelRoom.objects.create(
            description=description,
            price_per_night=price_per_night
        )
    
    def delete_room(self, room_id: int):
        """Удалить номер отеля"""
        return HotelRoom.objects.filter(pk=room_id).delete()


class RoomBookingRepository:
    """
    Репозиторий для работы с бронированиями номеров
    """
    def get_booking_by_id(self, booking_id: int) -> RoomBooking:
        """Получить бронирование по id"""
        return RoomBooking.objects.filter(id=booking_id).first()

    def get_bookings_by_room(self, room_id: int) -> List[RoomBooking]:
        """Получить все бронирования по room_id"""
        return RoomBooking.objects.filter(room_id=room_id).order_by('start_date')

    def get_all_bookings(self):
        """Получить все бронирования"""
        return RoomBooking.objects.all()

    def create_booking(self, room_id: int, start_date: str, end_date: str) -> RoomBooking:
        """Создать новое бронирование"""
        return RoomBooking.objects.create(
            room_id=room_id,
            start_date=start_date,
            end_date=end_date
        )

    def delete_booking(self, booking_id: int):
        """Удалить бронирование"""
        return RoomBooking.objects.filter(pk=booking_id).delete()


    


