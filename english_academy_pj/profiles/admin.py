from django.contrib import admin
from django import forms
from .models import Teacher, Student

# # Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ['user', 'full_name', 'email_confirmed', 'country', 'phone_number']
    list_display = ['user_id', 'full_name', 'user_email', 'category']
    search_fields = ['user__id', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['category', 'email_confirmed']
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'email_confirmed', 'category','avatar', 'phone_number', 'country')
            # 'fields': ('user', 'category','avatar',('hours','week_days'), 'phone_number', 'country')
        }),
        ('weekly class schedule', {'fields': (('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'),)}),
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

    @admin.display(description='email')
    def user_email(self, obj):
        return obj.user.email


class StudentAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ['user', 'full_name', 'email_confirmed', 'country', 'phone_number', 'email']
    list_display = ['user_id', 'full_name', 'email', 'balance']
    search_fields = ['user__id', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['email_confirmed']
    ordering = ['user_id']
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'email_confirmed', 'email' ,'avatar', 'balance', 'phone_number', 'country')
            # 'fields': ('user', 'category','avatar',('hours','week_days'), 'phone_number', 'country')
        }),)

    def has_add_permission(self, request): 
        return False

    def has_delete_permission(self, request, obj=None):
        if '/admin/accounts/user/' in request.path:
            return True
        return False

    @admin.display(ordering='user__first_name')
    def full_name(self, obj):
        return obj.user.full_name() 

    @admin.display(description='email')
    def email(self, obj):
        return obj.user.email

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
