from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('posts/<int:post_id>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/create/<int:post_id>/', views.PostCreateView.as_view(), name='post_create'),
]
