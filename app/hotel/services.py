from typing import Dict, Any, List

from rest_framework import status
from rest_framework.response import Response

from .models import HotelRoom
from .repositories import HotelRoomRepository
from .serializers import HotelRoomSerializer

class HotelRoomService:
    """
    Сервисный слой для работы с номерами отеля
    """
    def __init__(self):
        self.repository = HotelRoomRepository()

    def get_room(self, room_id: int) -> Response:
        """Получить номер по id"""
        try:
            result = self.repository.get_one(room_id)  # Вызывает .get()
            serializer = HotelRoomSerializer(result)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except HotelRoom.DoesNotExist:
            return Response({'error': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

    def get_room_list(self, sort_by:  str = 'created_at', order: str = 'asc') -> Response:
        """Получить список номеров"""
        rooms = self.repository.get_all(sort_by, order)
        serializer = HotelRoomSerializer(rooms, many=True)
        return Response({
            'data': serializer.data
        })


    def create_room(self, data: Dict[str, Any]) -> Response:
        """Создать новый номер отеля"""
        serializer = HotelRoomSerializer(data=data)  # Валидируем данные перед созданием
        if serializer.is_valid():
            try:
                result = self.repository.create(**serializer.validated_data)
                return Response({'id': result.id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': str(e)  # Логируем ошибку
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'error',
            'message': serializer.errors  # Возвращаем ошибки валидации
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete_room(self, room_id: int) -> Response:
        """Удалить номер отеля"""
        try:
            room = self.repository.get_one(room_id)
        except HotelRoom.DoesNotExist:
            return Response({'error': 'Номер не найден'}, status=status.HTTP_404_NOT_FOUND)

        room.delete()
        return Response({'message': f'Номер {room_id} успешно удален'}, status=status.HTTP_204_NO_CONTENT)



