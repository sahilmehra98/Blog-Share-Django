from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_auth import views as rviews


urlpatterns=[
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    #API urls
    path('users/', views.CreateUser.as_view(), name='create-user'),
    path('users/<int:pk>/', views.EditUser.as_view(), name='edit-user'),
    path('api/change_password/', views.ChangePasswordView.as_view()),
    path('api/login/', rviews.LoginView.as_view(), name='rest_login'),
    path('api/logout/', rviews.LogoutView.as_view(), name='rest_logout'),
    path('api/password/reset/', rviews.PasswordResetView.as_view(), name='rest_password_reset'),
]
