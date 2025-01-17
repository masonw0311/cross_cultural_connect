from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('create-account/', views.create_account, name='create_account'),
    path('process-zip/', views.process_zip, name='process_zip'),
    path('overview/', views.overview_view, name='overview'),
    path('welcome/', views.welcome_view, name='welcome'),
    path("translate/", views.translate_text, name="translate"),
    path('account_home/', views.account_home, name='account_home'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('account_management/', views.account_management, name='account_management'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]