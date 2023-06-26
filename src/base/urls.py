from django.urls import path
from base.views import index, dashboard




urlpatterns = [
    path('', index, name='base_index'),
    path('dashboard/', dashboard, name='dashboard'),  # noqa E501
]