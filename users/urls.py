from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', login_required(views.UserProfileView.as_view()), name='profile'),
    path('logout', views.UserLoginView.as_view(), name='logout'),
]
