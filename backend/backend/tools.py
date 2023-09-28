from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from client_api_app.serializers import UserSerializer


@api_view(['GET', ])
def check_user_exists(request: Request, username: str) -> Response:
    """Функция проверяет наличие пользователя в базе"""
    user = User.objects.filter(username=username)
    if user:
        return Response({'status': True})
    return Response({'status': False})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_data(request: Request) -> Response:
    """Функция возвращает данные юзера из базы"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
