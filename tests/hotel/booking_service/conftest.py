import pytest
from hotel.services import BookingService
from hotel.repositories import BookingRepository, RoomRepository
from hotel.serializers import BookingSerializer

@pytest.fixture
def booking_service(mocker):
    # Создаем моки для репозиториев
    mock_booking_repository = mocker.Mock(spec=BookingRepository)
    mock_room_repository = mocker.Mock(spec=RoomRepository)
    mock_booking_serializer = mocker.Mock(spec=BookingSerializer)
    
    # Репозитории
    mocker.patch('hotel.repositories.BookingRepository', return_value=mock_booking_repository)
    mocker.patch('hotel.repositories.RoomRepository', return_value=mock_room_repository)

    # Сериализатор
    mocker.patch('hotel.serializers.BookingSerializer', return_value=mock_booking_serializer)

    service = BookingService()
    service.booking_repository = mock_booking_repository
    service.room_repository = mock_room_repository
    service.booking_serializer = mock_booking_serializer
    
    return service 