from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name='blog'

urlpatterns=[
    path('', login_required(views.PostListView.as_view()), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('add/', views.addPost, name='add_post')
]
