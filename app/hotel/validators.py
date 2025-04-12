from rest_framework import serializers

ALLOWED_SORT_COLUMNS = {'created_at', 'price_per_night'}
ALLOWED_SORT_DIRECTIONS = {'asc', 'desc'}

def validate_room_id(data):
    room_id = data.get('room_id')
    if not room_id:
        raise serializers.ValidationError(
            {
                "status": "error",
                "message": "room_id является обязательным параметром"
            }
        )
    return room_id

def validate_sort_params(data):
    sort_column = data.get('sort_by', 'created_at')
    sort_direction = data.get('order', 'asc')
    
    if sort_column not in ALLOWED_SORT_COLUMNS:
        raise serializers.ValidationError(
            {
                "status": "error",
                "message": f'Недопустимое значение для сортировки sort_by. Допустимые значения: {", ".join(ALLOWED_SORT_COLUMNS)}'
            }
        )
    
    if sort_direction not in ALLOWED_SORT_DIRECTIONS:
        raise serializers.ValidationError(
            {
                "status": "error",
                "message": f'Недопустимое значение для направления сортировки order. Допустимые значения: {", ".join(ALLOWED_SORT_DIRECTIONS)}'
            }
        )
    
    return sort_column, sort_direction 