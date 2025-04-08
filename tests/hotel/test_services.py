import pytest
from rest_framework import status


class TestHotelRoomService:
    """Тесты для сервиса номеров отеля"""

    def test_get_all_rooms(self, room_service):
        """Тест получения списка всех номеров"""
        # Вызываем метод с параметрами сортировки
        response = room_service.get_all_rooms({'sort_by': 'created_at', 'order': 'asc'})
        
        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == 1
        assert response.data[0]['price_per_night'] == '1000.00'
        assert response.data[1]['id'] == 2
        
    def test_get_room_success(self, room_service):
        """Тест успешного получения номера по id"""
        # Вызываем метод
        response = room_service.get_room(1)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == 1
        assert response.data['description'] == 'Тестовый номер 1'
        assert response.data['price_per_night'] == '1000.00'
        
    def test_get_room_not_found(self, room_service, mocker):
        """Тест получения несуществующего номера"""
        # Настраиваем мок для возврата None
        room_service.room_repository.get_room.return_value = None
        
        # Вызываем метод
        response = room_service.get_room(999)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Номер не найден'
        
    def test_create_room_success(self, room_service):
        """Тест успешного создания номера"""
        # Данные для создания номера
        room_data = {
            'description': 'Новый тестовый номер',
            'price_per_night': 1500.00
        }
        
        # Вызываем метод
        response = room_service.create_room(room_data)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == 3
        
        # Проверяем, что метод репозитория был вызван с правильными параметрами
        room_service.room_repository.create_room.assert_called_once_with(
            description=room_data['description'],
            price_per_night=room_data['price_per_night']
        )
        
    def test_create_room_validation_error(self, room_service):
        """Тест создания номера с невалидными данными"""
        # Невалидные данные (отсутствует обязательное поле)
        invalid_data = {
            'description': 'Новый тестовый номер'
            # Отсутствует price_per_night
        }
        
        # Вызываем метод
        response = room_service.create_room(invalid_data)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert 'price_per_night' in response.data['message']
        
    def test_delete_room_success(self, room_service):
        """Тест успешного удаления номера"""
        # Вызываем метод
        response = room_service.delete_room(1)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['message'] == 'Номер 1 успешно удален'
        
        # Проверяем, что метод репозитория был вызван с правильным параметром
        room_service.room_repository.delete_room.assert_called_once_with(1)
        
    def test_delete_room_not_found(self, room_service, mocker):
        """Тест удаления несуществующего номера"""
        # Настраиваем мок для возврата неуспешного удаления
        room_service.room_repository.delete_room.return_value = 0
        
        # Вызываем метод
        response = room_service.delete_room(999)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Номер не найден'


class TestRoomBookingService:
    """Тесты для сервиса бронирований номеров"""

    def test_get_booking_by_id_success(self, booking_service):
        """Тест успешного получения бронирования по id"""
        # Вызываем метод
        response = booking_service.get_booking_by_id(1)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['id'] == 1
        assert response.data['data']['room_id']['id'] == 1
        assert response.data['data']['start_date'] == '2023-01-01'
        assert response.data['data']['end_date'] == '2023-01-05'
        
    def test_get_booking_by_id_not_found(self, booking_service, mocker):
        """Тест получения несуществующего бронирования"""
        # Настраиваем мок для возврата None
        booking_service.booking_repository.get_booking_by_id.return_value = None
        
        # Вызываем метод
        response = booking_service.get_booking_by_id(999)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Бронирование не найдено'
        
    def test_get_bookings_by_room_success(self, booking_service):
        """Тест успешного получения бронирований номера"""
        # Вызываем метод
        response = booking_service.get_bookings_by_room(1)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == 1
        assert response.data[0]['room_id']['id'] == 1
        assert response.data[0]['start_date'] == '2023-01-01'
        assert response.data[0]['end_date'] == '2023-01-05'
        assert response.data[1]['id'] == 2
        assert response.data[1]['room_id']['id'] == 2
        assert response.data[1]['start_date'] == '2023-02-01'
        assert response.data[1]['end_date'] == '2023-02-05'
        
    def test_get_bookings_by_room_not_found(self, booking_service, mocker):
        """Тест получения бронирований несуществующего номера"""
        # Настраиваем мок для возврата None
        booking_service.room_repository.get_room.return_value = None
        
        # Вызываем метод
        response = booking_service.get_bookings_by_room(999)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Номер не найден'
        
    def test_get_all_bookings(self, booking_service):
        """Тест получения всех бронирований"""
        # Вызываем метод
        response = booking_service.get_all_bookings()
        
        # Проверяем результат
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['data']) == 3
        assert response.data['data'][0]['id'] == 1
        assert response.data['data'][0]['room_id'] == 1
        assert response.data['data'][1]['id'] == 2
        assert response.data['data'][1]['room_id'] == 1
        assert response.data['data'][2]['id'] == 3
        assert response.data['data'][2]['room_id'] == 2
        
    def test_create_booking_success(self, booking_service):
        """Тест успешного создания бронирования"""
        # Данные для создания бронирования
        booking_data = {
            'room_id': 1,
            'start_date': '2023-04-01',
            'end_date': '2023-04-05'
        }
        
        # Вызываем метод
        response = booking_service.create_booking(booking_data)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == 4
        
        # Проверяем, что метод репозитория был вызван с правильными параметрами
        booking_service.booking_repository.create_booking.assert_called_once_with(
            room_id=booking_data['room_id'],
            start_date=booking_data['start_date'],
            end_date=booking_data['end_date']
        )
        
    def test_create_booking_validation_error(self, booking_service):
        """Тест создания бронирования с невалидными данными"""
        # Невалидные данные (отсутствует обязательное поле)
        invalid_data = {
            'room_id': 1,
            'start_date': '2023-04-01'
            # Отсутствует end_date
        }
        
        # Вызываем метод
        response = booking_service.create_booking(invalid_data)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['status'] == 'error'
        assert 'end_date' in response.data['message']
        
    def test_delete_booking_success(self, booking_service):
        """Тест успешного удаления бронирования"""
        # Вызываем метод
        response = booking_service.delete_booking(1)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data['message'] == 'Бронирование 1 успешно удалено'
        
        # Проверяем, что метод репозитория был вызван с правильным параметром
        booking_service.booking_repository.delete_booking.assert_called_once_with(1)
        
    def test_delete_booking_not_found(self, booking_service, mocker):
        """Тест удаления несуществующего бронирования"""
        # Настраиваем мок для возврата неуспешного удаления
        booking_service.booking_repository.delete_booking.return_value = 0
        
        # Вызываем метод
        response = booking_service.delete_booking(999)
        
        # Проверяем результат
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['status'] == 'error'
        assert response.data['message'] == 'Бронирование не найдено'
    