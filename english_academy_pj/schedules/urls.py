from django.urls import path
from .views import (
    task_view, 
    get_json_pack_data, 
    get_json_lessons_data, 
    get_json_teachers_data, 
    create_task,
    task_data_view,
    get_task_view,
    update_task,
    task_link,
    delete_task, 
    teacher_task_data_view,
    finish_task
)

app_name = 'schedules'

urlpatterns = [
    path('', task_view, name='home'),
    path('packs-json/', get_json_pack_data, name='packs-json'),
    path('lessons-json/<str:pack>/', get_json_lessons_data, name='lessons-json'),
    path('teachers-json/<str:category>/', get_json_teachers_data, name='teachers-json'), 
    path('create-task/', create_task, name='create-task'),
    path('task-data/', task_data_view, name='task-data'),
    path('get-task/<int:task>/', get_task_view, name='get-task'),
    path('<pk>/update/', update_task, name='task-update'),
    path('<pk>/link/', task_link, name='task-link'),
    path('<pk>/finish/', finish_task, name='task-finish'),
    path('<pk>/delete/', delete_task, name='task-delete'),
    path('teacher-task/', teacher_task_data_view, name='teacher-task'),
] 