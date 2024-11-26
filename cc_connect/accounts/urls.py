from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signin/', views.signin, name='signin'),
    path('create-account/', views.create_account, name='create_account'),
    path('process-zip/', views.process_zip, name='process_zip'),

]