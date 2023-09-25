from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from client_api_app.models import Vacancy, Language, Experience, Grade, \
    Speciality, StackTool, City
from client_api_app.serializers import VacancySerializer, LanguageSerializer, \
    ExperienceSerializer, GradeSerializer, SpecialitySerializer, \
    StackToolSerializer, CitySerializer


@api_view(['GET', ])
def test(request: HttpRequest) -> Response:
    """Тестовая"""
    from parser.test_parsers import main
    data = main(True)
    return Response({'test': data})


class VacancyList(generics.ListAPIView):
    """Список актуальных вакансий (размещенных в течение 30 дней)"""

    queryset = Vacancy.objects.get_actual()
    serializer_class = VacancySerializer


class LanguageList(generics.ListAPIView):
    """Список языков программирования"""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ExperienceList(generics.ListAPIView):
    """Список градаций опыта"""

    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class GradeList(generics.ListAPIView):
    """Список грейдов"""

    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class SpecialityList(generics.ListAPIView):
    """Список специальностей"""

    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class CityList(generics.ListAPIView):
    """Список городов"""

    queryset = City.objects.all()
    serializer_class = CitySerializer


class StackToolList(generics.ListAPIView):
    """Список навыков"""

    queryset = StackTool.objects.all()
    serializer_class = StackToolSerializer

