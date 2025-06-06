# Generated by Django 5.1.7 on 2025-04-25 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_number', models.IntegerField()),
                ('description', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotel.hotel')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('room_id', models.ForeignKey(db_column='room_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='hotel.room')),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
    ]
