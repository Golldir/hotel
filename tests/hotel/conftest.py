"""
Фикстуры для тестов сервисов отеля
"""
import pytest
from hotel.services import HotelRoomService, RoomBookingService
from unittest.mock import Mock, patch

from tests.hotel.test_data import mock_room_repository_data, mock_booking_repository_data


@pytest.fixture
def mock_booking_serializer(mocker):
    """Фикстура для подмены класса сериализатора бронирований"""
    # Создаем класс-заглушку
    mock_serializer = mocker.patch('hotel.serializers.RoomBookingSerializer')

    # Настраиваем конструктор для возврата объекта с is_valid=True
    mock_instance = mocker.Mock()
    mock_instance.is_valid.return_value = True
    mock_instance.validated_data = {
        'room_id': 1,
        'start_date': '2023-01-01',
        'end_date': '2023-01-05'
    }
    mock_serializer.return_value = mock_instance

    return mock_serializer


@pytest.fixture
def mock_room_repository(mocker):
    """Фикстура для мока репозитория номеров"""
    # Создаем мок-объект
    mock_repo = mocker.Mock()

    # Настраиваем поведение мока для get_all_rooms
    mock_repo.get_all_rooms.return_value = mock_room_repository_data['get_all_rooms']

    # Настраиваем поведение мока для get_room
    mock_repo.get_room.return_value = mock_room_repository_data['get_room']

    # Настраиваем поведение мока для create_room
    mock_repo.create_room.return_value = mock_room_repository_data['create_room']

    # Настраиваем поведение мока для delete_room
    mock_repo.delete_room.return_value = mock_room_repository_data['delete_room']

    return mock_repo


@pytest.fixture
def mock_booking_repository(mocker):
    """Фикстура для мока репозитория бронирований"""
    # Создаем мок-объект
    mock_repo = mocker.Mock()

    # Настраиваем поведение мока для get_booking_by_id
    mock_repo.get_booking_by_id.return_value = mock_booking_repository_data['get_booking_by_id']

    # Настраиваем поведение мока для get_bookings_by_room
    mock_repo.get_bookings_by_room.return_value = mock_booking_repository_data['get_bookings_by_room']

    # Настраиваем поведение мока для get_all_bookings
    mock_repo.get_all_bookings.return_value = mock_booking_repository_data['get_all_bookings']

    # Настраиваем поведение мока для create_booking
    mock_repo.create_booking.return_value = mock_booking_repository_data['create_booking']

    # Настраиваем поведение мока для delete_booking
    mock_repo.delete_booking.return_value = mock_booking_repository_data['delete_booking']

    return mock_repo


@pytest.fixture
def room_service_instance(mocker, mock_room_repository):
    """Фикстура для HotelRoomService с подмененным репозиторием"""
    # Создаем экземпляр сервиса
    service = HotelRoomService()

    # Подменяем репозиторий в экземпляре сервиса на наш мок
    service.room_repository = mock_room_repository

    # Возвращаем сервис
    return service


@pytest.fixture
def booking_service_instance(
        mocker,
        mock_booking_repository,
        mock_room_repository,
        mock_booking_serializer
):
    """Фикстура для RoomBookingService с подмененными репозиториями"""
    # Создаем экземпляр сервиса
    service = RoomBookingService()

    # Подменяем репозитории в экземпляре сервиса на наши моки
    service.booking_repository = mock_booking_repository
    service.room_repository = mock_room_repository

    # Подменяем класс сериализатора в сервисе
    # (это позволит перехватывать создание сериализатора в методе create_booking)
    service.booking_serializer = mock_booking_serializer

    # Возвращаем сервис
    return service
