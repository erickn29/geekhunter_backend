from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', ])
def test(request: HttpRequest) -> Response:
    """Тестовая"""
    from parser.test_parsers import main
    data = main(True)
    return Response({'test': data})
