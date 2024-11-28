from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('create-account/', views.create_account, name='create_account'),
    path('process-zip/', views.process_zip, name='process_zip'),
<<<<<<< HEAD
    path('overview/', views.overview_view, name='overview'),
    path('welcome/', views.welcome_view, name='welcome'),
    path("translate/", views.translate_text, name="translate"),
    
=======
    path('account_home/', views.account_home, name='account_home')
>>>>>>> c5f785a5e69f4be425f3830ac46b1120e1b9591e

]