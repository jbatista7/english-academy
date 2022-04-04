from django import template

register = template.Library()

@register.simple_tag
def get_full_name(user):
    print(user.full_name())