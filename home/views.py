from django.shortcuts import render
from django.views import View

from .models import Post

class HomePageView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})
