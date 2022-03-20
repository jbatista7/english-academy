from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# from django.contrib.auth import get_user_model
# User = get_user_model()

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
                last_login = user.last_login
                print(last_login)
                if last_login==None:
                    return redirect('accounts:password-reset-view')
                else:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('schedules:home')

                

            #     login(request, user)
            #     if request.GET.get('next'):
            #         return redirect(request.GET.get('next'))
            #     else:
            #         return redirect('schedules:home')
            # # elif user is not None and user.is_admin==True:
            # #     return redirect('admin:index')
        else:
            error_message = 'Ups ... something went wrong' 

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)