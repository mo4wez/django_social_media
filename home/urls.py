from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_page'),
    path('posts/<int:post_id>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
