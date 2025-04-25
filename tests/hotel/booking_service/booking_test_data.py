from datetime import datetime, timedelta
from hotel.models import Room, Booking

BOOKING_DATA = {
    'get_all_bookings': [
        {
            'id': 1,
            'room_id': 1,
            'guest_name': 'John Doe',
            'start_date': '2024-04-16',
            'end_date': '2024-04-20',
            'created_at': '2024-04-16'
        },
        {
            'id': 2,
            'room_id': 1,
            'guest_name': 'Jane Smith',
            'start_date': '2024-04-21',
            'end_date': '2024-04-25',
            'created_at': '2024-04-16'
        }
    ],
    'create_booking': {
        'id': 1,
        'room_id': 1,
        'guest_name': 'John Doe',
        'start_date': '2024-04-16',
        'end_date': '2024-04-20',
        'created_at': '2024-04-16'
    },
    'delete_booking': 1
}

# Константы для тестовых данных
TEST_BOOKING_DATA = {
    'room_id': 1,
    'guest_name': 'John Doe',
    'start_date': '2024-04-16',
    'end_date': '2024-04-20'
}

TEST_BOOKING_DATA_INVALID = {
    'invalid': 'data'
}