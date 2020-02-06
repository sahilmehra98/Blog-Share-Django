from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('profile', views.UserProfileViewSet)

urlpatterns=[
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('apilogin/', views.UserLoginApiView.as_view()),
    path('api/', include(router.urls)),
]
