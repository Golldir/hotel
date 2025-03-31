from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import HotelRoomService

# Create your views here.

class HotelRoomViewSet(viewsets.ViewSet):
    """
    Ручки для работы с номерами отеля
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = HotelRoomService()

    def list(self, request):
        """Получить список номеров отеля"""
        sort_by = request.query_params.get('sort_by', 'created_at')
        order = request.query_params.get('order', 'asc')

        return self.service.get_room_list(sort_by, order)

    def retrieve(self, request, pk=1):
        return self.service.get_room(pk)

    def create(self, request):
        """Добавить номер отеля"""
        return self.service.create_room(request.data)

    def destroy(self, request, pk=None):
        """Удалить номер отеля"""
        return self.service.delete_room(pk)




