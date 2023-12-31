from django.contrib.auth.models import User
from rest_framework import serializers

from client_api_app.models import Language, Grade, Experience, City, \
    Speciality, Company, StackTool, Vacancy, Person


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Language"""

    class Meta:
        model = Language
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Grade"""

    class Meta:
        model = Grade
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Experience"""

    class Meta:
        model = Experience
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для модели City"""

    class Meta:
        model = City
        fields = '__all__'


class SpecialitySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Speciality"""

    class Meta:
        model = Speciality
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Company"""

    city = serializers.SerializerMethodField()

    def get_city(self, obj: Company) -> dict | None:
        """F"""
        try:
            data = obj.city
            if data:
                serializer = CitySerializer(data)
                return serializer.data
            return None
        except AttributeError as e:
            print(e)
            return None

    class Meta:
        model = Company
        fields = '__all__'


class StackToolSerializer(serializers.ModelSerializer):
    """Сериализатор для модели StackTool"""

    class Meta:
        model = StackTool
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Vacancy"""

    speciality = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    stack = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_speciality(self, obj: Vacancy) -> dict | None:
        """F"""
        try:
            data = obj.speciality
            if data:
                serializer = SpecialitySerializer(data)
                return serializer.data.get('name')
            return None
        except AttributeError as e:
            print(e)
            return None

    def get_experience(self, obj: Vacancy) -> dict | None:
        """F"""
        try:
            data = obj.experience
            if data:
                serializer = ExperienceSerializer(data)
                return serializer.data.get('name')
            return None
        except AttributeError as e:
            print(e)
            return None

    def get_stack(self, obj: Vacancy) -> list | None:
        """F"""
        try:
            data = StackTool.objects.filter(vacancy=obj)
            stack_list = []
            if data:
                for obj in data:
                    stack_list.append(obj.name)
                return stack_list
            return None
        except AttributeError as e:
            print(e)
            return None

    def get_language(self, obj: Vacancy) -> dict | None:
        """F"""
        try:
            data = obj.language
            if data:
                serializer = LanguageSerializer(data)
                return serializer.data.get('name')
            return None
        except AttributeError as e:
            print(e)
            return None

    def get_grade(self, obj: Vacancy) -> dict | None:
        """F"""
        try:
            data = obj.grade
            if data:
                serializer = GradeSerializer(data)
                return serializer.data.get('name')
            return None
        except AttributeError as e:
            print(e)
            return None

    def get_company(self, obj: Vacancy) -> dict | None:
        """F"""
        try:
            data = obj.company
            if data:
                serializer = CompanySerializer(data)
                return serializer.data
            return None
        except AttributeError as e:
            print(e)
            return None

    class Meta:
        model = Vacancy
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Person"""

    class Meta:
        model = Person
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User"""

    person = serializers.SerializerMethodField()

    def get_person(self, obj: User) -> dict | None:
        """Метод возвращает персональные данные пользователя"""
        try:
            data = Person.objects.filter(user=obj)
            if data:
                serializer = PersonSerializer(data[0])
                return serializer.data
            return {'id': None}
        except AttributeError as e:
            print(e)
            return None

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'person'
        )
