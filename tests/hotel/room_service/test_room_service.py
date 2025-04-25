from rest_framework import status
from rest_framework.response import Response

from hotel.models import Room, Hotel
from tests.hotel.room_service.room_test_data import ROOM_DATA

class TestRoomService:
    def test_get_rooms_success(self, room_service):
        # Arrange
        data = {'hotel_id': 1}
        room_service.hotel_repository.hotel_exists.return_value = True
        room_service.room_repository.get_all_rooms.return_value = ROOM_DATA['get_all_rooms']
        room_service.room_serializer.return_value.data = ROOM_DATA['get_all_rooms']

        # Act
        response = room_service.get_rooms(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == ROOM_DATA['get_all_rooms']
        room_service.hotel_repository.hotel_exists.assert_called_once_with(1)
        room_service.room_repository.get_all_rooms.assert_called_once()

    def test_get_rooms_hotel_not_found(self, room_service):
        # Arrange
        data = {'hotel_id': 999}
        room_service.hotel_repository.hotel_exists.return_value = False

        # Act
        response = room_service.get_rooms(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Такого отеля не существует'

    def test_get_rooms_missing_hotel_id(self, room_service):
        # Arrange
        data = {}

        # Act
        response = room_service.get_rooms(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Введите hotel_id' in response.data['message']

    def test_create_room_success(self, room_service):
        # Arrange
        data = {
            'hotel_id': Hotel(id=1),
            'room_number': 101,
            'description': 'Стандартный номер',
            'price_per_night': '150.00'
        }
        room_service.room_serializer.is_valid.return_value = True
        room_service.room_serializer.return_value.validated_data = data
        room_service.room_repository.room_exists.return_value = False
        room_service.room_repository.create_room.return_value = Room(id=1)


        # Act
        response = room_service.create_room(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == ROOM_DATA['create_room']['id']


    def test_create_room_validation_error(self, room_service):
        # Arrange
        data = {
            'hotel_id': Hotel(id=1),
            'room_number': 101,
            'description': 'Стандартный номер',
            'price_per_night': '150.00'
        }
        room_service.room_serializer.return_value.is_valid.return_value = False
        room_service.room_serializer.return_value.validated_data = data
        room_service.room_serializer.errors = {'field': ['error']}

        # Act
        response = room_service.create_room(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'

    def test_create_room_already_exists(self, room_service):
        # Arrange
        data = {
            'hotel_id': Hotel(id=1),
            'room_number': 101,
            'description': 'Стандартный номер',
            'price_per_night': '150.00'
        }
        room_service.room_serializer.is_valid.return_value = True
        room_service.room_serializer.return_value.validated_data = data
        room_service.room_repository.room_exists.return_value = True

        # Act
        response = room_service.create_room(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'существует' in response.data['message']

    def test_delete_room_success(self, room_service):
        # Arrange
        room_id = ROOM_DATA['delete_room']
        room_service.room_repository.delete_room.return_value = (1,)

        # Act
        response = room_service.delete_room(room_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert f'Номер {room_id} успешно удален' in response.data['message']
        room_service.room_repository.delete_room.assert_called_once_with(room_id)

    def test_delete_room_not_found(self, room_service):
        # Arrange
        room_id = ROOM_DATA['delete_room']
        room_service.room_repository.delete_room.return_value = (0,)

        # Act
        response = room_service.delete_room(room_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Номер не найден'

