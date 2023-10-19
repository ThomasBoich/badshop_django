from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login as auth_login
from users.forms import LoginForm, CustomUserCreationForm


# Create your views here.


def login(request):
    context = {'title': 'Авторизация',}
    return render(request, 'login.html', context)

class AppLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    def get_success_url(self):
        return reverse_lazy('index')

    redirect_authenticated_user = True

class AppRegistration(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('cabinet')


    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)  # Use auth_login instead of login
        return response

class AppLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login')