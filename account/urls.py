from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('logout/', views.UserLogOutView.as_view(), name='logout_user'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
]
