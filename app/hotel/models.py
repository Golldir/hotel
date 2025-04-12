from django.db import models


class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
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


