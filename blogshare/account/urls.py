from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    #API urls
    path('apilogin/', views.UserLoginApiView.as_view()),
    path('users/', views.CreateUser.as_view(), name='create-user'),
    path('users/<int:pk>/', views.EditUser.as_view(), name='edit-user'),
]
