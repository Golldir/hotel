from typing import List

from hotel.models import Room


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