from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.test),
    path('vacancy/', views.VacancyList.as_view()),
    path('language/', views.LanguageList.as_view()),
    path('speciality/', views.SpecialityList.as_view()),
    path('experience/', views.ExperienceList.as_view()),
    path('grade/', views.GradeList.as_view()),
    path('stack/', views.StackToolList.as_view()),
    path('city/', views.CityList.as_view()),
]
