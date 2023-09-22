from datetime import timedelta, datetime

from django.db import models
from django.db.models import Q, QuerySet


class ActualVacancies(models.Manager):
    """Менеджер для модели вакансий"""

    def get_queryset(self) -> QuerySet:
        """Метод возвращает вакансии, опубликованные за последние 30 дней"""
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date()
        return self.filter(
            Q(date__range=[start_date, end_date]) &
            Q(
                Q(salary_from__isnull=False) | Q(salary_to__isnull=False)
            )
        )
