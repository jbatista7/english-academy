from django.contrib import admin
from .models import Pack, SupportAndSales, Magazines
# Register your models here.

class PackAdmin(admin.ModelAdmin):
    list_filter = ['language']
    list_display = ['name', 'number_of_lessons', 'language', 'package_price', 'created']
    # filter_horizontal = ['lessons']

    @admin.display(ordering='name')
    def number_of_lessons(self, obj):
        return obj.lessons.count()

MAX_OBJECTS = 5
class SupportAndSalesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

class MagazineAdmin(admin.ModelAdmin):
     def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

admin.site.register(Pack, PackAdmin)
admin.site.register(SupportAndSales, SupportAndSalesAdmin)
admin.site.register(Magazines)
