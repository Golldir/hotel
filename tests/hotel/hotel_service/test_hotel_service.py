from rest_framework import status
from rest_framework.response import Response

from hotel.models import Hotel
from tests.hotel.hotel_service.hotel_test_data import HOTEL_DATA

class TestHotelService:
    def test_get_hotels_success(self, hotel_service):
        # Arrange
        hotel_service.hotel_repository.get_all_hotels.return_value = HOTEL_DATA['get_all_hotels']
        hotel_service.hotel_serializer.return_value.data = HOTEL_DATA['get_all_hotels']

        # Act
        response = hotel_service.get_hotels()

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == HOTEL_DATA['get_all_hotels']
        hotel_service.hotel_repository.get_all_hotels.assert_called_once()

    def test_create_hotel_success(self, hotel_service):
        # Arrange
        data = {'name': 'Grand Hotel'}
        hotel_service.hotel_serializer.return_value.is_valid.return_value = True
        hotel_service.hotel_serializer.return_value.validated_data = data
        hotel_service.hotel_repository.create_hotel.return_value = Hotel(id=1)

        # Act
        response = hotel_service.create_hotel(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['hotel_id'] == HOTEL_DATA['create_hotel']['id']
        hotel_service.hotel_repository.create_hotel.assert_called_once_with(name=data['name'])

    def test_create_hotel_validation_error(self, hotel_service):
        # Arrange
        data = {'invalid': 'data'}
        hotel_service.hotel_serializer.return_value.is_valid.return_value = False
        hotel_service.hotel_serializer.errors = {'field': ['error']}

        # Act
        response = hotel_service.create_hotel(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'

    def test_delete_hotel_success(self, hotel_service):
        # Arrange
        hotel_id = HOTEL_DATA['delete_hotel']
        hotel_service.hotel_repository.delete_hotel.return_value = (1,)

        # Act
        response = hotel_service.delete_hotel(hotel_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert f'Отель {hotel_id} успешно удален' in response.data['message']
        hotel_service.hotel_repository.delete_hotel.assert_called_once_with(hotel_id)

    def test_delete_hotel_not_found(self, hotel_service):
        # Arrange
        hotel_id = HOTEL_DATA['delete_hotel']
        hotel_service.hotel_repository.delete_hotel.return_value = (0,)

        # Act
        response = hotel_service.delete_hotel(hotel_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Отель не найден' 