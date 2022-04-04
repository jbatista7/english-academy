from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    success_url = reverse_lazy('accounts:password-change-done-view')

class MyPasswordChangeDoneView(LoginRequiredMixin, PasswordResetDoneView):
    template_name = 'accounts/password-change-done.html'

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password-reset.html'
    email_template_name='accounts/password-reset-email.html',
    subject_template_name='accounts/password-reset-subject.txt',
    success_url = reverse_lazy('accounts:password-reset-done-view')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    success_url = reverse_lazy('accounts:password-reset-complete-view')

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password-reset-complete.html'