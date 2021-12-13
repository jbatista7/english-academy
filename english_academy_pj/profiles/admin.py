from django.contrib import admin
from django import forms
from .models import Teacher, Student

# # Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ['user', 'country', 'phone_number']
    list_display = ['user_id', 'user', 'full_name', 'category']
    search_fields = ['user__id', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['category']
    fieldsets = (
        (None, {
            'fields': ('user', 'category','avatar',('hours','week_days'), 'phone_number', 'country')
        }),
    )
    ordering = ['user_id']
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if '/admin/accounts/user/' in request.path:
            return True
        return False

    @admin.display(ordering='user__first_name')
    def full_name(self, obj):
        return obj.user.full_name()


class StudentAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ['user_id', 'user', 'full_name']
    list_display = ['user_id', 'user', 'full_name', 'balance']
    search_fields = ['user__id', 'user__email', 'user__first_name', 'user__last_name']
    ordering = ['user_id']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if '/admin/accounts/user/' in request.path:
            return True
        return False

    @admin.display(ordering='user__first_name')
    def full_name(self, obj):
        return obj.user.full_name() 

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)


    