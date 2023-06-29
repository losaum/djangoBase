from django.urls import path
from base.views import index, home, dashboard




urlpatterns = [
    path('', index, name='base_index'),
    path('home/', home, name='base_home'),
    path('dashboard/', dashboard, name='dashboard'),  # noqa E501
]