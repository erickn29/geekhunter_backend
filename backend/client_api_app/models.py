from django.contrib.auth.models import User
from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

from .model_managers import CustomVacancyManager


class BaseModel(models.Model):
    """Базовый класс для описания простых сущностей (город, язык...)"""

    name: str = models.CharField(max_length=128)
    count: int = models.PositiveBigIntegerField(default=0)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name

    # def save(self, *args, **kwargs) -> NoReturn:
    #     """Метод увеличивает счетчик при сохранении записи в БД"""
    #     self.count += 1
    #     print(f'Save method called! {self.name, self.count}')
    #     super(BaseModel, self).save(*args, **kwargs)


class StackTool(BaseModel):
    """Класс, описывающий модель навыка"""

    class Meta:
        db_table = 'vacancy_stack_tool'
        ordering = ['-count', ]


class Language(BaseModel):
    """Класс, описывающий модель языка программирования"""

    class Meta:
        db_table = 'vacancy_language'
        ordering = ['-count', ]


class City(BaseModel):
    """Класс, описывающий модель города"""

    class Meta:
        db_table = 'vacancy_city'
        ordering = ['-count', ]


class Speciality(BaseModel):
    """Класс, описывающий модель специализации"""

    class Meta:
        db_table = 'vacancy_speciality'
        ordering = ['-count', ]


class Experience(BaseModel):
    """Класс, описывающий модель опыта"""

    class Meta:
        db_table = 'vacancy_experience'
        ordering = ['-count', ]


class Grade(BaseModel):
    """Класс, описывающий модель грейда"""

    class Meta:
        db_table = 'vacancy_grade'
        ordering = ['-count', ]


class Company(models.Model):
    """Класс, описывающий модель компании"""

    name = models.CharField(max_length=128, default='МИАЦ')
    city = models.ForeignKey(City, on_delete=DO_NOTHING, null=True)

    class Meta:
        db_table = 'vacancy_company'

    def __str__(self) -> str:
        return f'{self.name} / Город: {self.city.name}'


class Vacancy(models.Model):
    """Класс, описывающий модель вакансии"""

    title: str = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_remote = models.BooleanField(default=False)
    salary_from = models.PositiveIntegerField(null=True)
    salary_to = models.PositiveIntegerField(null=True)
    speciality = models.ForeignKey(Speciality, on_delete=CASCADE)
    experience = models.ForeignKey(Experience, on_delete=CASCADE)
    grade = models.ForeignKey(Grade, on_delete=CASCADE)
    stack = models.ManyToManyField(StackTool)
    link = models.URLField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)

    objects = CustomVacancyManager()

    class Meta:
        indexes = [
            models.Index(
                fields=['salary_from', 'salary_to', 'speciality', 'date']
            ),
        ]
        unique_together = ('title', 'salary_from', 'salary_to', 'company')
        db_table = 'vacancy_vacancy'
        ordering = ['-date', ]

    def __str__(self) -> str:
        return self.title


class Profession(models.Model):
    """Класс, описывающий профессию"""

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    stack = models.ManyToManyField(StackTool)

    class Meta:
        db_table = 'vacancy_profession'

    def __str__(self) -> str:
        return self.speciality.name


class Person(models.Model):
    """Класс, описывающий человека"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.ForeignKey(
        Profession, on_delete=models.CASCADE, null=True
    )
    given = models.CharField(max_length=32, default='Anonymous')
    family: str = models.CharField(max_length=32, default='Anonymous')
    patronymic = models.CharField(max_length=32, null=True, blank=True)
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(14)],
        null=True, blank=True
    )
    telegram_login = models.CharField(max_length=255, null=True, blank=True)
    photo_link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'vacancy_person'

    def __str__(self) -> str:
        return self.family
