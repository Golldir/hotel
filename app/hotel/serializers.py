from rest_framework import serializers

class HotelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    rating = serializers.FloatField()
    address = serializers.CharField() 