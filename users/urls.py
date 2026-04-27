from django.urls import path
from users import views



urlpatterns =[
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
    path("profile/update/", views.update_profile, name="update_profile"),
]