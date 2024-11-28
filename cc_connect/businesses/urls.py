from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='businesses_home'),
    path('map/', views.map, name='map'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_businesses, name='search_businesses')
]