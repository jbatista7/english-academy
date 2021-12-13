from django import template
from authbg.models import AuthBg
from django.utils import timezone


register = template.Library()

@register.simple_tag
def get_photo():
    day = timezone.now().weekday()
    if AuthBg.objects.filter(week_day=day).exists():
        photo = AuthBg.objects.get(week_day=day)
        return photo
    else:
        return False