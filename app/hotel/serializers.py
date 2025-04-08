from rest_framework import serializers
from .models import HotelRoom, RoomBooking

class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ['id', 'description', 'price_per_night', 'created_at']

class RoomBookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RoomBooking
        fields = ['id', 'room_id', 'start_date', 'end_date', 'created_at']
