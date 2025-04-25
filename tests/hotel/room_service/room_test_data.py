from hotel.models import Hotel

ROOM_DATA = {
    'get_all_rooms': [
        {
            'id': 1,
            'room_number': 101,
            'hotel_id': 1,
            'description': 'Стандартный номер',
            'price_per_night': '150.00',
            'created_at': '2024-04-16'
        },
        {
            'id': 2,
            'room_number': 102,
            'hotel_id': 1,
            'description': 'Люкс',
            'price_per_night': '300.00',
            'created_at': '2024-04-16'
        }
    ],
    'create_room': {
        'id': 1,
        'room_number': 101,
        'hotel_id': Hotel(id=1),
        'description': 'Стандартный номер',
        'price_per_night': '150.00',
        'created_at': '2024-04-16'
    },
    'delete_room': 1
}

# Константы для тестовых данных
TEST_ROOM_DATA = {
    'hotel_id': 1,
    'room_number': 101,
    'description': 'Стандартный номер',
    'price_per_night': '150.00'
}

TEST_ROOM_DATA_INVALID = {
    'invalid': 'data'
}