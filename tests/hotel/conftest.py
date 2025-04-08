import pytest
from rest_framework import status
from hotel.services import HotelRoomService, RoomBookingService


@pytest.fixture
def mock_room_repository(mocker):
    """Фикстура для мока репозитория номеров"""
    # Создаем мок-объект
    mock_repo = mocker.Mock()
    
    # Настраиваем поведение мока для get_all_rooms
    mock_repo.get_all_rooms.return_value = [
        {'id': 1, 'description': 'Тестовый номер 1', 'price_per_night': 1000.00},
        {'id': 2, 'description': 'Тестовый номер 2', 'price_per_night': 2000.00}
    ]
    
    # Настраиваем поведение мока для get_room
    mock_repo.get_room.return_value = {'id': 1, 'description': 'Тестовый номер 1', 'price_per_night': 1000.00}
    
    # Настраиваем поведение мока для create_room
    mock_repo.create_room.return_value = {'id': 3}
    
    # Настраиваем поведение мока для delete_room
    mock_repo.delete_room.return_value = 1
    
    return mock_repo


@pytest.fixture
def mock_booking_repository(mocker):
    """Фикстура для мока репозитория бронирований"""
    # Создаем словарь с данными
    mock_data = {
        'get_booking_by_id': {
            'id': 1,
            'room_id': mocker.Mock(pk=1),  # Создаем мок-объект с атрибутом pk
            'start_date': '2023-01-01',
            'end_date': '2023-01-05',
            'created_at': '2023-01-01T00:00:00Z'
        },
        'get_bookings_by_room': [
            {
                'id': 1,
                'room_id': mocker.Mock(pk=1),  # Просто ID номера
                'start_date': '2023-01-01',
                'end_date': '2023-01-05',
                'created_at': '2023-01-01T00:00:00Z'
            },
            {
                'id': 2,
                'room_id': mocker.Mock(pk=1),  # Просто ID номера
                'start_date': '2023-02-01',
                'end_date': '2023-02-05',
                'created_at': '2023-02-01T00:00:00Z'
            }
        ],
        'get_all_bookings': [
            {
                'id': 1,
                'room_id': mocker.Mock(pk=1),  # Просто ID номера
                'start_date': '2023-01-01',
                'end_date': '2023-01-05',
                'created_at': '2023-01-01T00:00:00Z'
            },
            {
                'id': 2,
                'room_id': mocker.Mock(pk=1),  # Просто ID номера
                'start_date': '2023-02-01',
                'end_date': '2023-02-05',
                'created_at': '2023-02-01T00:00:00Z'
            },
            {
                'id': 3,
                'room_id': mocker.Mock(pk=2),  # Просто ID номера
                'start_date': '2023-03-01',
                'end_date': '2023-03-05',
                'created_at': '2023-03-01T00:00:00Z'
            }
        ],
        'create_booking': {
            'id': 4,
            'created_at': '2023-04-01T00:00:00Z'
        },
        'delete_booking': 1
    }
    
    # Создаем мок-объект
    mock_repo = mocker.Mock()
    
    # Настраиваем поведение мока для get_booking_by_id
    mock_repo.get_booking_by_id.return_value = mock_data['get_booking_by_id']
    
    # Настраиваем поведение мока для get_bookings_by_room
    mock_repo.get_bookings_by_room.return_value = mock_data['get_bookings_by_room']
    
    # Настраиваем поведение мока для get_all_bookings
    mock_repo.get_all_bookings.return_value = mock_data['get_all_bookings']
    
    # Настраиваем поведение мока для create_booking
    mock_repo.create_booking.return_value = mock_data['create_booking']
    
    # Настраиваем поведение мока для delete_booking
    mock_repo.delete_booking.return_value = mock_data['delete_booking']
    
    return mock_repo


@pytest.fixture
def room_service(mocker, mock_room_repository):
    """Фикстура для HotelRoomService с подмененным репозиторием"""
    # Создаем экземпляр сервиса
    service = HotelRoomService()
    
    # Подменяем репозиторий в экземпляре сервиса на наш мок
    service.room_repository = mock_room_repository
    
    # Возвращаем сервис
    return service


@pytest.fixture
def booking_service(mocker, mock_booking_repository, mock_room_repository):
    """Фикстура для RoomBookingService с подмененными репозиториями"""
    # Создаем экземпляр сервиса
    service = RoomBookingService()
    
    # Подменяем репозитории в экземпляре сервиса на наши моки
    service.booking_repository = mock_booking_repository
    service.room_repository = mock_room_repository
    
    # Возвращаем сервис
    return service

