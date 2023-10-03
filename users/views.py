from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(CreateView, SuccessMessageMixin):
    """Регистрация"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Для успешной регистрации подтвердите адрес электронной почты'

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class UserProfileView(UpdateView):
    """Профиль"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verification.html'

    def get_context_data(self, **kwargs):
        context = super(EmailVerificationView, self).get_context_data()
        context['title'] = 'Store - Подтверждение электронной почты'
        return context

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
