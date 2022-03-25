from django.urls import path
from .views import profile_view, edit_view, EmailUpdate, activate_view

app_name = 'profiles'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_view, name='edit'),
    path('edit/email/', EmailUpdate.as_view(), name='email'),
    path('activate/<uidb64>/<token>/', activate_view, name='activate'),
]