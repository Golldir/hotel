from hotel.models import HotelRoom, RoomBooking

mock_room_repository_data = {
    'get_room': [
        HotelRoom(
            id=1,
            description='Тестовый номер 1',
            price_per_night=1500.00
        )
    ],
    'get_all_rooms': [
        HotelRoom(
            id=1,
            description='Тестовый номер 1',
            price_per_night=1500.00,
            created_at='2025-03-31 13:14:43.177140 +00:00'
        ),
        HotelRoom(
            id=2,
            description='Тестовый номер 2',
            price_per_night=2000.00,
            created_at='2025-03-31 13:14:43.177140 +00:00'
        )
    ],
    'create_room':
        HotelRoom(
            id=1,
            description='Тестовый номер 1',
            price_per_night=1500.00,
            created_at='2025-03-31 13:14:43.177140 +00:00'
        ),
    'delete_room': 1
}

mock_booking_repository_data = {
    'get_booking_by_id': 
        RoomBooking(
            id=1,
            room_id=HotelRoom(
                id=1,
                description='Тестовый номер 1',
                price_per_night=1500.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        )
    ,
    'get_bookings_by_room': [
        RoomBooking(
            id=1,
            room_id=HotelRoom(
                id=1,
                description='Тестовый номер 1',
                price_per_night=1500.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        ),
        RoomBooking(
            id=2,
            room_id=HotelRoom(
                id=1,
                description='Тестовый номер 2',
                price_per_night=2000.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        )
    ],
    'get_all_bookings': [
        RoomBooking(
            id=1,
            room_id=HotelRoom(
                id=1,
                description='Тестовый номер 1',
                price_per_night=1500.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        ),
        RoomBooking(
            id=2,
            room_id=HotelRoom(
                id=1,
                description='Тестовый номер 2',
                price_per_night=2000.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        ),
        RoomBooking(
            id=3,
            room_id=HotelRoom(
                id=2,
                description='Тестовый номер 2',
                price_per_night=2000.00,
                created_at='2025-03-31 13:14:43.177140 +00:00'
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        ),
    ],
    'create_booking':
        RoomBooking(
            id=5,
            room_id=HotelRoom(
                id=2
            ),
            start_date='2023-01-01',
            end_date='2023-01-05',
            created_at='2023-01-01T00:00:00Z'
        )
    ,
    'delete_booking': 1
}
