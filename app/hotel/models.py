from django.db import models

# Create your models here.

class HotelRoom(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
