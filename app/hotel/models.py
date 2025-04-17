from django.db import models

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_number = models.IntegerField()
    hotel_id = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        db_column='hotel_id',
    )
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_column='room_id'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']


