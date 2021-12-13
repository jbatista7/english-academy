from django.urls import path
from .views import profile_view, edit_view, EmailUpdate

app_name = 'profiles'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', edit_view, name='edit'),
    path('edit/email/', EmailUpdate.as_view(), name='email'),
]