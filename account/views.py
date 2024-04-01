from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import UserRegisterationForm

class RegisterView(View):
    def get(self, request):
        form = UserRegisterationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterationForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password'],
                )
            messages.success(
                request,
                'You registered successfully.',
                'success',
                )
            return redirect('home:home_page')            

