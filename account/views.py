from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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


class UserLogOutView(View):
    
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