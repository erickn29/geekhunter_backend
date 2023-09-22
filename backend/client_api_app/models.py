from django.db import models
from django.db.models import DO_NOTHING, CASCADE

from .model_managers import ActualVacancies


class BaseModel(models.Model):
    """Базовый класс для описания простых сущностей (город, язык...)"""

    name: str = models.CharField(max_length=128)
    count: int = models.PositiveBigIntegerField(null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class StackTool(BaseModel):
    """Класс, описывающий модель навыка"""

    class Meta:
        db_table = 'stack_tool'


class Language(BaseModel):
    """Класс, описывающий модель языка программирования"""

    class Meta:
        db_table = 'language'


class City(BaseModel):
    """Класс, описывающий модель города"""

    class Meta:
        db_table = 'city'


class Speciality(BaseModel):
    """Класс, описывающий модель специализации"""

    class Meta:
        db_table = 'speciality'


class Experience(BaseModel):
    """Класс, описывающий модель опыта"""

    class Meta:
        db_table = 'experience'


class Grade(BaseModel):
    """Класс, описывающий модель грейда"""

    class Meta:
        db_table = 'grade'


class Company(models.Model):
    """Класс, описывающий модель компании"""

    name = models.CharField(max_length=128, default='МИАЦ')
    city = models.ForeignKey(City, on_delete=DO_NOTHING, null=True)

    class Meta:
        db_table = 'company'

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

    objects = models.Manager()
    actual = ActualVacancies()

    class Meta:
        indexes = [
            models.Index(
                fields=['salary_from', 'salary_to', 'speciality', 'date']
            ),
        ]
        unique_together = ('title', 'salary_from', 'salary_to', 'company')
        db_table = 'vacancy'

    def __str__(self) -> str:
        return self.title
