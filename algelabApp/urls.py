from django.urls import path
from . import views

urlpatterns = [
    path('auth/github/', views.github_login, name='github_login'),
    path('auth/github/callback/', views.github_callback, name='github_callback'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/validate-token/', views.validate_token, name='validate_token'),
    path('user/', views.get_user_info, name='get_user_info'),
]