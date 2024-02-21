from django.shortcuts import render
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
# from .tasks import send_confirmation_email_task
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView

# Create your views here.
class SignupView(SuccessMessageMixin,CreateView):
    form_class=SignUpForm
    success_url=reverse_lazy('login')
    success_message='account successfully created'
    template_name='accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # send_confirmation_email_task.delay(form.cleaned_data['email'])
        return response
   

class AccountLoginView(SuccessMessageMixin,LoginView):
    template_name = 'accounts/login.html'
    success_url=reverse_lazy('login')
    success_message='account logged in successfully'


class LogoutUserView(LogoutView):
    next_page = reverse_lazy('accounts:login')  

