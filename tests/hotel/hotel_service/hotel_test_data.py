from hotel.models import Hotel

HOTEL_DATA = {
    'get_all_hotels': [
        {
            'id': 1,
            'name': 'Grand Hotel',
            'created_at': '2024-04-16'
        },
        {
            'id': 2,
            'name': 'Luxury Hotel',
            'created_at': '2024-04-16'
        }
    ],
    'create_hotel': {
        'id': 1,
        'name': 'Grand Hotel',
        'created_at': '2024-04-16'
    },
    'delete_hotel': 1
}

# Константы для тестовых данных
TEST_HOTEL_DATA = {
    'name': 'Grand Hotel'
}

TEST_HOTEL_DATA_INVALID = {
    'invalid': 'data'
}