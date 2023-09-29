import hashlib
import os

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from client_api_app.models import Person
from client_api_app.serializers import UserSerializer
from dotenv import load_dotenv

load_dotenv()


@api_view(['GET', ])
def check_user_exists(request: Request, username: str) -> Response:
    """Функция проверяет наличие пользователя в базе"""
    user = User.objects.filter(username=username)
    if user:
        return Response({'status': True, 'user_id': user[0].id})
    return Response({'status': False})


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_data(request: Request) -> Response:
    """Функция возвращает данные юзера из базы"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST', ])
def create_person(request: Request, pk: int) -> Response:
    """Функция сохраняет объект Person"""
    user_obj = User.objects.filter(id=pk)
    if user_obj:
        obj, created = Person.objects.update_or_create(
            user=user_obj[0],
            defaults={
                'given': request.data.get('first_name'),
                'family': request.data.get('last_name'),
                'telegram_login': request.data.get('telegram_login'),
                'photo_link': request.data.get('photo_link'),
            }
        )
        if created:
            return Response(status=201)
        return Response(status=204)
    return Response(status=404)


@csrf_exempt
@api_view(['POST', ])
def get_password(request: Request) -> Response:
    """Функция генерирует локальный пароль пользователя"""
    if request.data.get('username'):
        user_id = request.data.get('username')
        salt = os.getenv('DJANGO_SECRET_KEY')[25:]
        hashed_password = hashlib.sha256(
            (user_id + salt).encode('utf-8')).hexdigest()
        return Response({'password': hashed_password})
    return Response({'password': None})
