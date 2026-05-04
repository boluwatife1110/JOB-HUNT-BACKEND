from django.urls import path
from users import views



urlpatterns = [
    path('users/register/', views.register, name='register'),
    path('users/signin/', views.signin, name='signin'),
    path('users/profile/', views.profile, name='profile'),
    path('users/profile/update/', views.update_profile, name='update_profile'),
]