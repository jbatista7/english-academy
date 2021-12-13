from django.contrib import admin
from .models import AuthBg

# Register your models here.
MAX_OBJECTS = 7

class AuthBgAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

admin.site.register(AuthBg, AuthBgAdmin)