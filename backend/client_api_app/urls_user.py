from django.urls import path
from . import views_user as views


urlpatterns = [
    path('check/user/exists/<username>/', views.check_user_exists),
    path('get/user/', views.get_user_data),
    path('create/person/<int:pk>/', views.create_person)
]
