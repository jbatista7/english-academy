from unicodedata import name
from django.urls import path
from .views import support_and_sales_view, magazine_view

app_name = 'lessons'

urlpatterns = [
    path('support-and-sales/', support_and_sales_view, name='support-and-sales'),
    path('magazines/', magazine_view, name='magazines'),
]