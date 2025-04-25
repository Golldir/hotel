import pytest
from hotel.services import RoomService
from hotel.repositories import RoomRepository, HotelRepository
from hotel.serializers import RoomSerializer

@pytest.fixture
def room_service(mocker):
    # Создаем моки для репозиториев
    mock_room_repository = mocker.Mock(spec=RoomRepository)
    mock_hotel_repository = mocker.Mock(spec=HotelRepository)
    mock_room_serializer = mocker.Mock(spec=RoomSerializer)
    
    # Репозиторий
    mocker.patch('hotel.repositories.RoomRepository', return_value=mock_room_repository)
    mocker.patch('hotel.repositories.HotelRepository', return_value=mock_hotel_repository)

    # Сериализатор
    mocker.patch('hotel.serializers.RoomSerializer', return_value=mock_room_serializer)


    service = RoomService()
    service.room_repository = mock_room_repository
    service.hotel_repository = mock_hotel_repository
    service.room_serializer = mock_room_serializer
    
    return service 