from englishacademy.settings import ALLOWED_HOSTS
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, PurchasedPackage
from lessons.models import Pack
from profiles.models import Teacher, Student
import pytz
import datetime
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from .decorators import allowed_users

from django.db.models import Count
# from math import copysign


User = get_user_model()

# Create your views here.

@login_required
@allowed_users(allowed_roles=['teacher'])
def teacher_task_data_view(request):
    user_id = request.user.id
    full_name = request.user.full_name()
    task_qs = Task.objects.filter(teacher__user_id=user_id)
    data = []
    for task in task_qs:
        item = {
            'id': task.id,
            'pack': task.pack.name,
            'language': task.pack.language,
            'lesson': task.lesson.title,
            'teacher': task.teacher.user.full_name(),
            'duration': task.lesson.duration,
            'date': task.date.strftime('%d/%m/%y %H:%M'),
            'status': task.status,
        }
        data.append(item)
    return JsonResponse({'data': data})

@login_required
@allowed_users(allowed_roles=['student'])
def task_data_view(request):
    user_id = request.user.id
    full_name = request.user.full_name()
    task_qs = Task.objects.filter(student__user_id=user_id)    
    data = []
    for task in task_qs:
        item = {
            'id': task.id,
            'pack': task.pack.name,
            'language': task.pack.language,
            'lesson': task.lesson.title,
            'teacher': task.teacher.user.full_name(),
            'duration': task.lesson.duration,
            'date': task.date.strftime('%d/%m/%y %H:%M'),
            'status': task.status,
        }
        data.append(item)
    return JsonResponse({'data':data})

@login_required
@allowed_users(allowed_roles=['student'])
def get_task_view(request, *args, **kwargs):
    task_id = kwargs.get('task')
    user_id = request.user.id
    task_qs = Task.objects.filter(student__user_id=user_id, id=task_id)
    data = []
    for task in task_qs:
        item = {
            'id': task.id,
            'language': task.teacher.category,
            'lesson_link': task.lesson_link,
            'teacher': task.teacher.user.full_name(),
            'date': task.date.strftime('%d/%m/%y %H:%M'),
            'status': task.status,
        }
        data.append(item)
    return JsonResponse({'data': data})

@login_required
# @allowed_users(allowed_roles=['student', 'teacher'])
def task_view(request, *args, **kwargs):
    role = request.user.get_role()
    user_id = request.user.id
    if role == 'student':
        task_qs = Task.objects.filter(student__user_id=user_id)
        for obj in task_qs:
            status = obj.status
            old_date = obj.date.date()
            today = datetime.date.today()
            time_diference = (old_date - today).days
        
            if status == 'active':
                if time_diference < -1:
                    obj.delete()
        
        purchased_packs = PurchasedPackage.objects.filter(student__user_id=user_id)
        
        # pack_qs = None
        # for p in purchased_packs:
        #     pack_qs = p.packs.all()
        context = {
            'task_qs': task_qs, 
            'pack_qs': purchased_packs,
        }
        return render(request, 'schedules/task-list.html', context)
    elif role == 'teacher':
        task_qs = Task.objects.filter(teacher__user_id=user_id)

        # student_list = list(set(task_qs.values_list('student', flat=True)))
        # ts = task_qs.values('student').annotate(count=Count('id')).order_by()

        # duplicate_students = Task.objects.values('student').annotate(student_count=Count('student')).filter(student_count__gt=1)

        context = {
            'task_qs': task_qs, 
        }
        return render(request, 'schedules/teacher-task.html', context)
    return render(request, 'schedules/task-list.html')

@login_required
@allowed_users(allowed_roles=['student'])
def get_json_pack_data(request):
    user_id = request.user.id
    # task_qs = Task.objects.filter(student__user_id=user_id)
    purchased_packs = PurchasedPackage.objects.filter(student__user_id=user_id)
    data = []
    for p in purchased_packs:
        item = {
            'id': p.pack.id,
            'language': p.pack.language,
            'number_of_lessons': p.pack.number_of_lessons,
        }
        data.append(item)
        # qs_val = list(p.packs.values())
    return JsonResponse({'data': data})
    # return JsonResponse({'data':list(purchased_packs.values())})

@login_required
@allowed_users(allowed_roles=['student'])
def get_json_lessons_data(request, *args, **kwargs):
    selected_pack = kwargs.get('pack')
    obj_pack = Pack.objects.filter(name=selected_pack)
    obj_lessons = []
    for obj in obj_pack:
        obj_lessons = list(obj.lessons.all().values())
    return JsonResponse({'data':obj_lessons})

@login_required
@allowed_users(allowed_roles=['student'])
def get_json_teachers_data(request, *args, **kwargs):
    teacher_category = kwargs.get('category')

    teachers = Teacher.objects.filter(category=teacher_category)
    
    obj_teachers = []
    for person in teachers:
        obj_teachers.append({
            "user_id": person.user.id,
            "name": person.full_name(),
            "week_days": person.week_days,
            "hours": person.hours
            })
    return JsonResponse({'data':obj_teachers})

@login_required
@allowed_users(allowed_roles=['student'])
def update_task(request, pk):
    obj = Task.objects.get(pk=pk)
    if request.is_ajax():
        status = request.POST.get('status')
        old_date = obj.date.date()
        today = datetime.date.today()
        time_diference = (old_date - today).days
        if status == 'active':
            # taskTimezone = request.POST.get('timezone')
            # teacher_full_name = request.POST.get('teacher')
            teacher_user_id = request.POST.get('teacher_user_id')
            # language = request.POST.get('language')
            # teachers = Teacher.objects.filter(category=language)
            # for person in teachers:
            #     if teacher_full_name == person.full_name():
            #         teacher_user_id = person.user.id
            new_teacher = Teacher.objects.get(user_id=teacher_user_id)
            new_date = request.POST.get('date')
            # tzname = pytz.timezone(taskTimezone)
            new_date_aware = timezone.make_aware(parse_datetime(new_date), timezone=timezone.utc)
            task = Task.objects.filter(teacher=new_teacher, date=new_date_aware)
            if task:
                return JsonResponse({'updated': False, 'message': 'exists'}, safe=False)
            
            # one_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
            # time0 = datetime.timedelta(hours=0, minutes=0, seconds=0)
            if time_diference <= 1 and time_diference >= -1:
                return JsonResponse({
                    'msg':'Cannot change this booking, less than 24h'
                    })
            # elif old_date - now <= one_day:
            else:
                if time_diference < -1:
                    obj.delete()
                    # return JsonResponse({})
                    return JsonResponse({
                        'msg':'Booking expired'
                        })
                else:
                    obj.date = new_date_aware
                    obj.teacher = new_teacher
                    obj.save()
                    return JsonResponse({
                        'teacher': obj.teacher.full_name(),
                        'date': obj.date
                        })
        else:
            return JsonResponse({
                'msg':'This booking is finished'
            })

@login_required
@allowed_users(allowed_roles=['teacher'])
def finish_task(request, pk):
    obj = Task.objects.get(pk=pk)
    old_date = obj.date.date()
    today = datetime.date.today()
    time_diference = (old_date - today).days
    if request.is_ajax():
        if time_diference <= 0:
            obj.status = 'finished'
            obj.save()
            return JsonResponse({
                'status': obj.status,
                })
        else:
            return JsonResponse({
                'status': obj.status,
                })

@login_required
@allowed_users(allowed_roles=['student'])
def delete_task(request, pk):
    obj = Task.objects.get(pk=pk)
    old_date = obj.date.date()
    today = datetime.date.today()
    # now = timezone.now()
    if request.is_ajax():
        status = request.POST.get('status')
        time_diference = (old_date - today).days

        if status == 'active':
            # one_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
            # time0 = datetime.timedelta(hours=0, minutes=0, seconds=0)
            if time_diference <= 1 and time_diference >= -1: #can't delete task 24h before and 24h later
                return JsonResponse({ 
                    'msg':'Cannot delete this booking, less than 24h'
                    })
            else:
                obj.delete()
                return JsonResponse({})

        elif status == 'finished':
            if time_diference < -30: #can delete after 30 days
                return JsonResponse({
                    'msg':'Cannot delete this booking, less than 30 days.'
                    })
            else:
                obj.delete()
                return JsonResponse({})
        # else:
            # time0 = datetime.timedelta(hours=0)
            # one_day = datetime.timedelta(hours=23, minutes=59, seconds=59)
            # days30 = datetime.timedelta(days=30, hours=23, minutes=59, seconds=59)
        
            # obj.delete()

@login_required
@allowed_users(allowed_roles=['student'])
def create_task(request):
    if request.is_ajax():
        user_id = request.POST.get('user_id')
        # language = request.POST.get('language')
        student_obj = Student.objects.get(user_id=user_id)
        # teacher_full_name = request.POST.get('teacher')
        teacher_user_id = request.POST.get('teacher_user_id')
        # print(teacher_user_id)
        # teachers = Teacher.objects.filter(category=language)
        # for person in teachers:
        #     if teacher_full_name == person.full_name():
        #         teacher_user_id = person.user.id
        teacher_obj = Teacher.objects.get(user_id=teacher_user_id)        
        date_obj = request.POST.get('date')
        new_date_aware = timezone.make_aware(parse_datetime(date_obj), timezone=timezone.utc)
        task = Task.objects.filter(teacher=teacher_obj, date=new_date_aware)
        if task:
            return JsonResponse({'created': False, 'message': 'exists'}, safe=False)
        Task.objects.create(student=student_obj, teacher=teacher_obj, date=new_date_aware)
        return JsonResponse({'created': True})
    return JsonResponse({'created': False}, safe=False)

@login_required
@allowed_users(allowed_roles=['teacher'])
def task_link(request, pk):
    obj = Task.objects.get(pk=pk)    
    if request.is_ajax():
        link = request.POST.get('link')
        status = request.POST.get('status')
        old_date = obj.date.date()
        today = datetime.date.today()
        time_diference = (old_date - today).days

        if status == 'active':
            if time_diference <= -1:
                return JsonResponse({
                    'msg':'expired'
                    })
            else:
                print('save')
                obj.lesson_link = link
                obj.save()
                return JsonResponse({})
        else:
            return JsonResponse({
                'msg':'This booking is finished'
            })

