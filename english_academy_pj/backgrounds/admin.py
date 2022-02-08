from django.contrib import admin
from .models import Background

# Register your models here.
MAX_OBJECTS = 7

class BackgroundAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)
   

admin.site.register(Background, BackgroundAdmin)