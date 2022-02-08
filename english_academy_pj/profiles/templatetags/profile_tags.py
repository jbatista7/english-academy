from django import template
from profiles.models import Student, Teacher

register = template.Library()

@register.simple_tag
def get_profile(request):
    if request.user.is_authenticated:
        if Student.objects.filter(user_id=request.user.id).exists():
            return Student.objects.get(user_id=request.user.id)
        elif Teacher.objects.filter(user_id=request.user.id).exists():
            return Teacher.objects.get(user_id=request.user.id)
    else:
        return None


