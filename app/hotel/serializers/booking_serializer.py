from rest_framework import serializers

from hotel.models import Booking, Room


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    start_date = serializers.DateField(format='%Y-%m-%d')
    end_date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Booking
        fields = '__all__'