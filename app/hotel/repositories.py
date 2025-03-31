from typing import List, Optional
from .models import HotelRoom

class HotelRoomRepository:
    """
    Репозиторий для работы с номерами отеля
    """
    def get_one(self, room_id: int) -> HotelRoom:
        """Получить все номера с сортировкой"""
        return HotelRoom.objects.get(pk=room_id)

    def get_all(self, sort_by: str = 'created_at', order: str = 'asc') -> List[HotelRoom]:
        """Получить все номера с сортировкой"""
        valid_sort_fields = {'price_per_night', 'created_at'}
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'

        order_prefix = '' if order == 'asc' else '-'
        return HotelRoom.objects.all().order_by(f'{order_prefix}{sort_by}')

    def create(self, description: str, price_per_night: float) -> HotelRoom:
        """Создать новый номер отеля"""
        return HotelRoom.objects.create(
            description=description,
            price_per_night=price_per_night
        )
    
    def delete(self, room_id: int):
        """Удалить номер отеля"""
        room = HotelRoom.objects.get(pk=room_id)
        room.delete()
        room.save()

    


