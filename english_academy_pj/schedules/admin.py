from django.contrib import admin
from .models import Task, PurchasedPackage

from import_export import fields, resources
from import_export.admin import ExportActionMixin
from import_export.widgets import ForeignKeyWidget


# Register your models here.

class TaskResource(resources.ModelResource):

    full_name = fields.Field()

    # teacher = fields.Field(
    #     column_name='teacher',
    #     attribute='teacher',
    #     widget=ForeignKeyWidget(Task, 'user__first_name'))
    # teacher = fields.Field(
    #     column_name='teacher',
    #     attribute='teacher',
    #     widget=ForeignKeyWidget(Task, 'user__first_name'))

    class Meta:
        model = Task
        fields = ('teacher', 'status', 'student', 'date')
        export_order = ('teacher' , 'full_name', 'status', 'student', 'date')

    def dehydrate_full_name(self, Task):
        return f'{Task.teacher.user.first_name} {Task.teacher.user.last_name}'


class TaskAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = TaskResource
    list_display = ['student', 'student_full_name', 'teacher_full_name', 'status', 'date']
    readonly_fields = ['student_full_name', 'status', 'created', 'updated', 'lesson_link']
    list_filter = ['status']
    search_fields = ['student_id', 'student__user__first_name', 'student__user__last_name', 'student__user__email', 'teacher__user__first_name', 'teacher__user__last_name', 'teacher__user__email']
    # readonly_fields = ['full_name', 'student', 'lesson', 'teacher', 'date', 'status', 'created', 'updated']
    raw_id_fields = ['student']
    # fields = ['student', 'student_full_name', 'lesson_link', 'teacher', 'date', 'status', 'created', 'updated']

    # def full_name(self, obj):
    #     return obj.student.user.full_name()

    # full_name.admin_order_field = "student"


    # get_view_count.admin_order_field = "post_stats__view_count"
    # get_view_count.short_description = "View count"

    @admin.display(ordering='student', description='Student')
    def student_full_name(self, obj):
        return obj.student.user.full_name()

    @admin.display(ordering='teacher', description='Teacher')
    def teacher_full_name(self, obj):
        return obj.teacher.user.full_name()


class PurchasedPackageResource(resources.ModelResource):

    full_name = fields.Field()

    class Meta:
        model = PurchasedPackage
        fields = ('student', 'pack__name', 'pack__language__name', 'pack__number_of_lessons', 'pack__package_price', 'created', 'updated')
        export_order = ('student' , 'full_name', 'pack__name', 'pack__language__name', 'pack__number_of_lessons', 'pack__package_price', 'created', 'updated')

    def dehydrate_full_name(self, PurchasedPackage):
        return f'{PurchasedPackage.student.user.first_name} {PurchasedPackage.student.user.last_name}'



class PurchasedPackageAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PurchasedPackageResource
    # actions = None
    list_display = ['student_id', 'full_name', 'pack', 'created', 'updated']
    # filter_horizontal = ['student_id']
    list_filter = ['pack']
    readonly_fields = ['full_name']
    fields = ['student', 'pack']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__user__email']
    raw_id_fields = ['student']

    # @admin.display()
    # def user_id(self, obj):
    #     return obj.student.user.id

    def has_change_permission(self, request, obj =None):
        return False

    @admin.display(ordering='student')
    def full_name(self, obj):
        return obj.student.user.full_name()

    # @admin.display()
    # def number_of_packs(self, obj):
    #     return obj.packs.all().count()

    # def get_products(self, obj):
    #     return "\n".join([p.name for p in obj.packs.all()])
        
admin.site.register(PurchasedPackage, PurchasedPackageAdmin)
admin.site.register(Task, TaskAdmin)