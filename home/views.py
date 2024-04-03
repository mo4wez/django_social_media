from django.shortcuts import render
from django.views import View

from .models import Post

class HomePageView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, post_id, slug):
        post = Post.objects.get(pk=post_id, slug=slug)

        return render(request, 'home/post_detail.html', {'post': post})