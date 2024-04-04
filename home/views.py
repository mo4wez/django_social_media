from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post

class HomePageView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, post_id, slug):
        post = Post.objects.get(pk=post_id, slug=slug)

        return render(request, 'home/post_detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        return render(request, 'home/post_delete.html')
    
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(
                request, 
                'Your was post deleted.',
                'success'
            )
            return redirect('home:home_page')
        
        messages.error(
            request,
            'You can not delete this post.',
            'danger'
        )
        
        return render(request, 'home/post_delete.html')
        