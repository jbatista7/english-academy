from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SupportAndSales, Magazines

# Create your views here.

@login_required
def support_and_sales_view(request):
    qs_support = SupportAndSales.objects.all()
    context = {
        'supportandsales':qs_support,
    }
    return render(request, 'lessons/support-and-sales.html', context)

@login_required
def magazine_view(request):
    qs_magazine = Magazines.objects.all()
    context = {
        'magazines': qs_magazine
    }
    return render(request, 'lessons/magazines.html', context)