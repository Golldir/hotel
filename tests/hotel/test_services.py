import pytest
from rest_framework import status

from hotel.models import RoomBooking, HotelRoom



class TestHotelRoomService:
    """Тесты для сервиса номеров отеля"""

    def test_get_room(self, room_service_instance):
        """Тест получения номера по id"""
        # Вызываем метод
        response = room_service_instance.get_room(1)

        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == 1
        assert response.data[0]['price_per_night'] == '1500.00'

    def test_get_all_rooms(self, room_service_instance):
        """Тест получения списка всех номеров"""
        # Вызываем метод с параметрами сортировки
        response = room_service_instance.get_all_rooms({'sort_by': 'created_at', 'order': 'asc'})

        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == 1
        assert response.data[0]['price_per_night'] == '1500.00'
        assert response.data[1]['id'] == 2
        assert response.data[1]['price_per_night'] == '2000.00'

    def test_get_room_not_found(self, room_service_instance, mocker):
        """Тест получения несуществующего номера"""
        # Настраиваем мок для возврата None
        room_service_instance.room_repository.get_room.return_value = []

        # Вызываем метод
        response = room_service_instance.get_room(999)

        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Номер не найден'

    def test_create_room_success(self, room_service_instance):
        """Тест успешного создания номера"""
        # Данные для создания номера
        room_data = {
            'description': 'Тестовый номер',
            'price_per_night': 1500.00
        }

        # Вызываем метод
        response = room_service_instance.create_room(room_data)

        # Проверяем результат
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == 1

    def test_create_room_validation_error(self, room_service_instance):
        """Тест создания номера с невалидными данными"""
        # Невалидные данные (отсутствует обязательное поле)
        invalid_data = {
            'description': 'Новый тестовый номер'
            # Отсутствует price_per_night
        }

        # Вызываем метод
        response = room_service_instance.create_room(invalid_data)

        # Проверяем результат
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert 'price_per_night' in response.data['message']

    def test_delete_room_success(self, room_service_instance):
        """Тест успешного удаления номера"""
        # Вызываем метод
        response = room_service_instance.delete_room(1)

        # Проверяем результат
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['message'] == 'Номер 1 успешно удален'

    def test_delete_room_not_found(self, room_service_instance):
        """Тест удаления несуществующего номера"""
        # Настраиваем мок для возврата неуспешного удаления
        room_service_instance.room_repository.delete_room.return_value = 0

        # Вызываем метод
        response = room_service_instance.delete_room(999)

        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Номер не найден'


class TestRoomBookingService:
    """Тесты для сервиса бронирований номеров"""

    def test_get_booking_by_id_success(self, booking_service_instance):
        """Тест успешного получения бронирования по id"""
        # Вызываем метод
        response = booking_service_instance.get_booking_by_id(1)

        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 1,
            'room_id': 1,
            'start_date': '2023-01-01'
        }

    def test_get_booking_by_id_not_found(self, booking_service_instance, mocker):
        """Тест получения несуществующего бронирования"""
        # Настраиваем мок для возврата None
        booking_service_instance.booking_repository.get_booking_by_id.return_value = None

        # Вызываем метод
        response = booking_service_instance.get_booking_by_id(999)

        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Бронирование не найдено'

    def test_get_bookings_by_room_success(self, booking_service_instance):
        """Тест успешного получения бронирований номера"""
        # Вызываем метод
        response = booking_service_instance.get_bookings_by_room(1)

        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0] == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 1, ''
            'room_id': 1,
            'start_date': '2023-01-01'
        }
        assert response.data[1] == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 2, 'room_id': 1,
            'start_date': '2023-01-01'
        }

    def test_get_bookings_by_room_not_found(self, booking_service_instance, mocker):
        """Тест получения бронирований несуществующего номера"""
        # Настраиваем мок для возврата None
        booking_service_instance.room_repository.get_room.return_value = None

        # Вызываем метод
        response = booking_service_instance.get_bookings_by_room(999)

        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            'message': 'Номер не найден',
            'status': 'error'
        }

    def test_get_all_bookings(self, booking_service_instance):
        """Тест получения всех бронирований"""
        # Вызываем метод
        response = booking_service_instance.get_all_bookings()

        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert response.data[0] == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 1,
            'room_id': 1,
            'start_date': '2023-01-01'
        }
        assert response.data[1] == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 2,
            'room_id': 1,
            'start_date': '2023-01-01'
        }
        assert response.data[2] == {
            'created_at': '2023-01-01T00:00:00Z',
            'end_date': '2023-01-05',
            'id': 3,
            'room_id': 2,
            'start_date': '2023-01-01'
        }


    def test_create_booking_success(self, booking_service_instance):
        """Тест успешного создания бронирования"""
        # Данные для создания бронирования
        booking_data = {
            'room_id': 1,
            'start_date': '2023-04-01',
            'end_date': '2023-04-05',
        }

        # Вызываем метод
        response = booking_service_instance.create_booking(booking_data)

        # Проверяем результат
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == 5

    def test_create_booking_validation_error(self, mocker, booking_service_instance):
        """Тест создания бронирования с невалидными данными"""
        # Невалидные данные (отсутствует обязательное поле)
        invalid_data = {
            'room_id': 1,
            'start_date': '2023-04-01'
            # Отсутствует end_date
        }
        
        # Создаем мок для невалидного сериализатора
        invalid_serializer_mock = mocker.Mock()
        invalid_serializer_mock.is_valid.return_value = False
        invalid_serializer_mock.errors = {'end_date': ['Обязательное поле.']}
        
        # Создаем фабрику, которая будет возвращать наш невалидный сериализатор
        mock_serializer_class = mocker.Mock(return_value=invalid_serializer_mock)
        
        # Заменяем класс сериализатора в сервисе на нашу фабрику
        booking_service_instance.booking_serializer = mock_serializer_class
        
        # Вызываем метод
        response = booking_service_instance.create_booking(invalid_data)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert 'end_date' in str(response.data['message'])

    def test_delete_booking_success(self, booking_service_instance):
        """Тест успешного удаления бронирования"""
        # Вызываем метод
        response = booking_service_instance.delete_booking(1)

        # Проверяем результат
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['message'] == 'Бронирование 1 успешно удалено'

        # Проверяем, что метод репозитория был вызван с правильным параметром
        booking_service_instance.booking_repository.delete_booking.assert_called_once_with(1)

    def test_delete_booking_not_found(self, booking_service_instance, mocker):
        """Тест удаления несуществующего бронирования"""
        # Настраиваем мок для возврата неуспешного удаления
        booking_service_instance.booking_repository.delete_booking.return_value = 0

        # Вызываем метод
        response = booking_service_instance.delete_booking(999)

        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Бронирование не найдено'
