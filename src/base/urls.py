from django.urls import path
from base.views import index, home, homeOuro, homePrata, homeBronze




urlpatterns = [
    path('', index, name='base_index'),
    path('home/', home, name='base_home'),
    path('homeOuro/', homeOuro, name='base_homeOuro'),
    path('homePrata/', homePrata, name='base_homePrata'),
    path('homeBronze/', homeBronze, name='base_homeBronze'),
    

    #path('dashboard/', dashboard, name='dashboard'),  # noqa E501
]