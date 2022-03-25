from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# from django.contrib.contenttypes.models import ContentType


User = get_user_model()

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
    # filter_horizontal = ()
    filter_horizontal = ('groups',)
    # filter_horizontal = ['groups']

    def get_groups(self, obj):
        return list(obj.groups.values_list('name',flat=True))

    get_groups.short_description = 'Groups'

    # def has_change_permission(self, request, obj=None):
    #     try:
    #         if obj.is_superuser and not request.user.is_superuser :
    #             return False
    #         else:
    #             return True
    #     except:
    #         return True

    def get_readonly_fields( self, request, obj=None):
        try:
            if not request.user.is_superuser:
                if obj.is_superuser:
                    return ["staff","groups", "admin", "superuser", "email", "first_name", "last_name", "password", "active"]
                return ["staff","groups", "admin", "superuser", "active"]
            # elif not obj.is_superuser and request.user.is_superuser:
            #     return []
            # elif not request.user.is_superuser and obj.is_superuser:
            #     return ["staff","groups", "first_name", "last_name"]
            elif not obj.is_superuser and request.user.is_superuser:
                return []
            else:
                return ["staff","groups", "admin", "superuser", "active"]
        except:
            return ["staff","groups", "admin", "superuser", "active"]

    # def has_delete_permission(self, request, obj=None):
    #     try:
    #         if obj.is_superuser:
    #             return False
    #         else:
    #             return True
    #     except:
    #         return True

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


# new_group, created = Group.objects.get_or_create(name ='new_group')
 
# # Code to add permission to group
# ct = ContentType.objects.get_for_model(User)
 
# # If I want to add 'Can go Haridwar' permission to level0 ?
# permission = Permission.objects.create(codename ='can_add_user',
#                                         name ='Can add user',
#                                                 content_type = ct)
# new_group.permissions.add(permission)

admin.site.register(User, UserAdmin)    

# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group) 

# admin.site.register(Permission)