from rest_framework import status
from rest_framework.response import Response

from hotel.models import Room, Booking
from tests.hotel.booking_service.booking_test_data import BOOKING_DATA

class TestBookingService:
    def test_get_bookings_by_room_id_success(self, booking_service):
        # Arrange
        data = {'room_id': 1}
        booking_service.room_repository.get_room.return_value = Room(id=1)
        booking_service.booking_repository.get_bookings_by_room.return_value = BOOKING_DATA['get_all_bookings']
        booking_service.booking_serializer.return_value.data = BOOKING_DATA['get_all_bookings']

        # Act
        response = booking_service.get_bookings_by_room_id(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == BOOKING_DATA['get_all_bookings']
        booking_service.room_repository.get_room.assert_called_once_with(1)
        booking_service.booking_repository.get_bookings_by_room.assert_called_once_with(1)

    def test_get_bookings_room_not_found(self, booking_service):
        # Arrange
        data = {'room_id': 999}
        booking_service.room_repository.get_room.return_value = None

        # Act
        response = booking_service.get_bookings_by_room_id(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Номер не существует'

    def test_get_bookings_missing_room_id(self, booking_service):
        # Arrange
        data = {}

        # Act
        response = booking_service.get_bookings_by_room_id(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'Введите room_id' in response.data['message']

    def test_create_booking_success(self, booking_service):
        # Arrange
        data = {
            'room_id': 1,
            'guest_name': 'John Doe',
            'start_date': '2024-04-16',
            'end_date': '2024-04-20'
        }
        booking_service.booking_serializer.return_value.is_valid.return_value = True
        booking_service.booking_serializer.return_value.validated_data = data
        booking_service.booking_repository.create_booking.return_value = Booking(id=1)

        # Act
        response = booking_service.create_booking(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['booking_id'] == BOOKING_DATA['create_booking']['id']
        booking_service.booking_repository.create_booking.assert_called_once_with(
            room_id=data['room_id'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )

    def test_create_booking_validation_error(self, booking_service):
        # Arrange
        data = {'invalid': 'data'}
        booking_service.booking_serializer.return_value.is_valid.return_value = False
        booking_service.booking_serializer.errors = {'field': ['error']}

        # Act
        response = booking_service.create_booking(data)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'

    def test_delete_booking_success(self, booking_service):
        # Arrange
        booking_id = BOOKING_DATA['delete_booking']
        booking_service.booking_repository.delete_booking.return_value = (1,)

        # Act
        response = booking_service.delete_booking(booking_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_200_OK
        assert f'Бронирование {booking_id} успешно удалено' in response.data['message']
        booking_service.booking_repository.delete_booking.assert_called_once_with(booking_id)

    def test_delete_booking_not_found(self, booking_service):
        # Arrange
        booking_id = BOOKING_DATA['delete_booking']
        booking_service.booking_repository.delete_booking.return_value = (0,)

        # Act
        response = booking_service.delete_booking(booking_id)

        # Assert
        assert isinstance(response, Response)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['message'] == 'Бронирование не найдено' 