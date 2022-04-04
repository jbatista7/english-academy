from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import get_user_model
User = get_user_model()

from profiles.models import Teacher, Student

def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    error_message = None
    form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin==False: 
                if user.role:
                    if user.role == 'student':
                        user_profile = Student.objects.get(user_id=user.id)
                    elif user.role == 'teacher':
                        user_profile = Teacher.objects.get(user_id=user.id)

                    if user_profile.email_confirmed == True:               
                        last_login = user.last_login
                        login(request, user)
                        if request.GET.get('next'):
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('schedules:home')
                    else:
                        error_message = 'Ups ... something went wrong'
                else:
                    error_message = 'Ups ... something went wrong'
        else:
            error_message = 'Ups ... something went wrong' 

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

