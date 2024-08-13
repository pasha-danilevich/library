import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

def get_access_token(request):
    return request.session.get('access')

def get_user_from_token(access_token):
    if not access_token:
        return None
    try:
        # Декодируем токен
        token_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = token_payload.get('user_id')

        # Получаем пользователя
        user = User.objects.get(id=user_id)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None