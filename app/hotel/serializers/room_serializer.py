from rest_framework import serializers

from hotel.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def validate_room_id(self, value):
        if not Room.objects.filter(id=value).exists():
            raise serializers.ValidationError("Номер не существует")
        return value