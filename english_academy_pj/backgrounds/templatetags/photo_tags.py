from django import template
from backgrounds.models import Background
from django.utils import timezone


register = template.Library()

@register.simple_tag
def get_photo():
    day = timezone.now().weekday()
    if Background.objects.filter(week_day=day).exists():
        photo = Background.objects.get(week_day=day)
        return photo
    else:
        return False