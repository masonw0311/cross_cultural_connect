from django.urls import path
from . import views

urlpatterns = [
    path('', views.business_home, name='businesses_home'),
    path('map/', views.map, name='map'),
    path('search_results/', views.search_businesses, name='search_results'),
    path('businesses/', views.business_home, name='business_home'),
]