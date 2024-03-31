from django.shortcuts import render
from django.views import View

from .forms import UserRegisterationForm

class RegisterView(View):
    def get(self, request):
        form = UserRegisterationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        pass
