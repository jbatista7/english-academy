from django.contrib.sessions.models import Session
# from schedules.views import task_data_view
from django.contrib.auth.decorators import login_required
from schedules.decorators import allowed_users
from django.shortcuts import render
from .models import Student, Teacher
from .forms import TeacherUploadForm, StudentUploadForm, UserProfileUpdateForm, EmailForm
from schedules.models import PurchasedPackage, Task
from lessons.models import Pack
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django import forms
# Create your views here.
from django.contrib.auth.tokens import default_token_generator


from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout


@login_required
@allowed_users(allowed_roles=['student', 'teacher'])
def profile_view(request):
    profile = User.objects.get(id=request.user.id)
    if profile.role == 'student':
        qs_profile = Student.objects.get(user_id=request.user.id)
        purchased_packs = PurchasedPackage.objects.filter(student__user_id=request.user.id)
        task_amount = Task.objects.filter(student__user_id=request.user.id).count()
        qs_packs = None
        balance = 0
        for p in purchased_packs:
            qs_packs = p.pack
            balance += p.pack.number_of_lessons

        if balance < task_amount:
            balance = 0
        else:
            balance -= task_amount
        
        context = {
            'qs_profile': qs_profile,
            'qs_packs': purchased_packs,
            'task_amount': task_amount,
            'balance': balance,
        }
        return render(request, 'profiles/student-profile.html', context)
    elif profile.role == 'teacher':
        language = Teacher.objects.get(user_id=request.user.id).category
        qs_packs = Pack.objects.filter(language=language)
        qs_profile = Teacher.objects.get(user_id=request.user.id)
        task_amount = Task.objects.filter(teacher__user_id=request.user.id).count
        
        context = {
            'qs_profile': qs_profile,
            'qs_packs': qs_packs,
            'language': language,
            'task_amount': task_amount,
        }
        return render(request, 'profiles/teacher-profile.html', context)

@login_required
@allowed_users(allowed_roles=['student', 'teacher'])
def edit_view(request):
    profile = User.objects.get(id=request.user.id)
    userForm = UserProfileUpdateForm(instance=profile)
    if profile.role == 'student':
        qs_profile = Student.objects.get(user_id=request.user.id)
        form = StudentUploadForm(instance=qs_profile)
    elif profile.role == 'teacher':
        qs_profile = Teacher.objects.get(user_id=request.user.id)
        form = TeacherUploadForm(instance=qs_profile)

    if request.method == 'POST':
        form = StudentUploadForm(request.POST, request.FILES, instance=qs_profile)
        userForm = UserProfileUpdateForm(request.POST or None, instance=profile)
        if all([form.is_valid(), userForm.is_valid()]):
            form.save()
            userForm.save()
            return redirect('profiles:profile')

    context = {
        'qs_profile': qs_profile,
        'form':form,
        'user_form' : userForm,
    }
    return render(request, 'profiles/edit.html', context)


class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profiles:profile')
    template_name = 'profiles/profile-email-form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder':'Email'})
        return form


def activate_view(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = User.objects.get(id=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    token_maker = PasswordResetTokenGenerator()
    
    if myuser is not None and token_maker.check_token(myuser,token):

        if myuser.role:
            if myuser.role == 'student':
                user_profile = Student.objects.get(user_id=myuser.id)
            elif myuser.role == 'teacher':
                user_profile = Teacher.objects.get(user_id=myuser.id)

            user_profile.email_confirmed = True
            user_profile.save()

            new_password_token = token_maker.make_token(myuser)
            return redirect('accounts:password-reset-confirm-view', uidb64, new_password_token)
        return render(request,'profiles/activation_failed.html')
    else:
        return render(request,'profiles/activation_failed.html')