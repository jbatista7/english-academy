from telnetlib import STATUS
from django import template
from schedules.models import PurchasedPackage, Task


register = template.Library()

@register.simple_tag
def get_balance_percent(user_id):
    balance = 0
    finished = 0

    purchased_packs = PurchasedPackage.objects.filter(student__user_id=user_id)
    finished = Task.objects.filter(student__user_id=user_id, status='finished').count()

    for p in purchased_packs:
        balance += p.pack.number_of_lessons

    percent = (100 * finished) / balance

    if (balance - finished) <= 1 and percent < 90:
        percent = 90

    return percent