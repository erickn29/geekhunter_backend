from django.contrib import admin
from django.urls import path, include, re_path
from . import tools

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('client_api_app.urls')),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/check/user/exists/<username>/', tools.check_user_exists),
    path('auth/get/user/', tools.get_user_data)
]
