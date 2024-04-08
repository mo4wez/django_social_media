from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .models import Relation
from .forms import UserRegisterationForm, UserLoginForm


class UserRegisterView(View):
    form_class = UserRegisterationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password1'],
            )
            messages.success(
                request,
                'You registered successfully.',
                'success',
            )
            return redirect('home:home_page')

        return render(request, 'account/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    'Login successfull.',
                    'success'
                )
                return redirect('home:home_page')
            messages.success(
                request,
                'Username or password Wrong!',
                'warning'
            )

        return render(request, self.template_name, {'form': form})


class UserLogOutView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'account/logout.html')
    
    def post(self, request):
        logout(request)
        messages.error(
            request,
            'You\'re logged out.',
            'danger',
        )

        return redirect('account:login_user')


class UserProfileView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.user_posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'account/profile.html', {'user_p': user, 'posts': posts, 'is_following':is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            messages.error(
                request,
                'You are already following this user.',
                'dager'
            )
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(
                request,
                'You followed this user.',
                'success'
            )
        return redirect('account:user_profile', user.id)

class UserUnfollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)

        if relation.exists():
            relation.delete()
            messages.success(
                request,
                'You Unfollowed this user.',
                'success',
            )
        else:
            messages.error(
                request,
                'you are not following this user.',
                'danger'
            )
        return redirect('account:user_profile', user.id)
