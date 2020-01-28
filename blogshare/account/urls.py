from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
]
