from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import HotelSerializer

# Create your views here.

class HotelViewSet(viewsets.ViewSet):
    """
    API ViewSet для работы с отелями
    """
    def list(self, request):
        hotels = [
            {
                'id': 1,
                'name': 'Гранд Отель',
                'rating': 4.5,
                'address': 'ул. Ленина, 10'
            },
            {
                'id': 2,
                'name': 'Морской Бриз',
                'rating': 4.2,
                'address': 'пр. Мира, 25'
            }
        ]
        
        serializer = HotelSerializer(hotels, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
