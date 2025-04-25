from hotel.models import Hotel


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