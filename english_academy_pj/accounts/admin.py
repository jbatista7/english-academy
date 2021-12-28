from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField



User = get_user_model()
 
# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group) 

class UserAdminChangeForm(forms.ModelForm):

    # if User.is_superuser:
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"./../password/\">this form</a>."))
                    # "using <a href=\"/admin/password_change/\">this form</a>."))


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    # print(User.get_full_name)
    list_display = ['id', 'full_name', 'email', 'role', 'staff', 'created', 'updated']
    list_filter = ['staff', 'role']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2', 'role')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


    def has_change_permission(self, request, obj=None):
        try:
            if obj.is_superuser and not request.user.is_superuser :
                return False
            else:
                return True
        except:
            return True

    def get_readonly_fields( self, request, obj=None):
        try:
            if not request.user.is_superuser:
                return ["staff"]
            elif not obj.is_superuser and request.user.is_superuser:
                return []
            else:
                return ["staff"]
        except:
            return ["staff"]

    def has_delete_permission(self, request, obj=None):
        try:
            if obj.is_superuser:
                return False
            else:
                return True
        except:
            return True

    # def save_model(self, request, obj, form, change):
    # # Override this to set the password to the value in the field if it's
    # # changed.
    #     if obj.pk:
    #         orig_obj = User.objects.get(pk=obj.pk)
    #         if obj.password != orig_obj.password:
    #             obj.set_password(obj.password)
    #     else:
    #         obj.set_password(obj.password)
    #     obj.save()

    # def has_delete_permission(self, request, obj=None):
    #     print(obj)
    #     if obj.is_admin:
    #         pass
    #     if request.user.is_admin:
    #         return False
    #     return True
        # if '/admin/accounts/user/' in request.path:
        #     return True



admin.site.register(User, UserAdmin)