from django.urls import path
from .views import (
    MyPasswordChangeView, 
    MyPasswordChangeDoneView, 
    MyPasswordResetView,
    MyPasswordResetDoneView, 
    MyPasswordResetConfirmView,
    MyPasswordResetCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    path('change-password/', MyPasswordChangeView.as_view(), name='password-change-view'),
    path('change-password/done/', MyPasswordChangeDoneView.as_view(), name='password-change-done-view'),
    path('reset-password/', MyPasswordResetView.as_view(), name='password-reset-view'),
    path('reset-password/done/', MyPasswordResetDoneView.as_view(), name='password-reset-done-view'),
    path('reset-password/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password-reset-confirm-view'),
    path('reset-password/complete/', MyPasswordResetCompleteView.as_view(), name='password-reset-complete-view'),
]
