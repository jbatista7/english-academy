from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


User = get_user_model()

class UserAdminChangeForm(forms.ModelForm):
    # if User.is_superuser:
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"./../password/\">this form</a>."))
                    

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['id', 'full_name', 'email', 'role', 'get_groups', 'staff', 'created', 'updated']
    list_filter = ['staff', 'role', 'groups']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('staff', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2', 'role')}
        ),
    )
    search_fields = ['id', 'first_name', 'last_name', 'email']
    ordering = ['email']
    filter_horizontal = ('groups',)

    def get_groups(self, obj):
        return list(obj.groups.values_list('name',flat=True))

    get_groups.short_description = 'Groups'

    def get_readonly_fields( self, request, obj=None):
        try:
            if not request.user.is_superuser:
                if obj.is_superuser:
                    return ["staff","groups", "admin", "superuser", "email", "first_name", "last_name", "password", "active"]
                return ["staff","groups", "admin", "superuser", "active"]
            elif not obj.is_superuser and request.user.is_superuser:
                return []
            else:
                return ["staff","groups", "admin", "superuser", "active"]
        except:
            return ["staff","groups", "admin", "superuser", "active"]


admin.site.register(User, UserAdmin)    