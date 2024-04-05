from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify

from .models import Post
from .forms import PostCreateAndUpdateForm

class HomePageView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):

    def get(self, request, post_id, slug):
        post = get_object_or_404(Post, pk=post_id, slug=slug)

        return render(request, 'home/post_detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        return render(request, 'home/post_delete.html')
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
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


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateAndUpdateForm
    template_name = 'home/post_update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(
                request,
                'You can not edit this post!',
                'danger'
                )
            return redirect('home:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.save()
            messages.success(
                request,
                f'\"{post.title}\" updated successfully.',
                'success'
                )
            return redirect('home:post_detail', post.id, post.slug)
        return render(request, self.template_name, {'form':form})


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateAndUpdateForm
    template_name = 'home/post_update.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(
                request,
                'Your post created successfully.',
                'success'
                )
            return redirect('home:post_detail', new_post.id, new_post.slug)