from .models import Teacher, Student
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.role == 'teacher':
        Teacher.objects.update_or_create(user=instance, id=instance.id)
    elif instance.role == 'student':
        Student.objects.update_or_create(user=instance, id=instance.id)

#     def create_profile(sender, **kwargs):
#     if kwargs["created"]:
#         p = Profile(user=kwargs["instance"], ...)
#         p.save()
# django.db.models.signals.post_save.connect(create_profile, sender=User)
    # if created:
    #     print(instance.role)
    #     if instance.role == 'teacher':
    #         Teacher.objects.create(user=instance)
    #     elif instance.role == 'student':
    #         Student.objects.create(user=instance)
        # Student.objects.create(user=instance)



# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     if instance.role == 'teacher':
#         if Student.objects.filter(user_id=instance.id).exists():
#             Student.objects.filter(user_id=instance.id).delete()
#         Teacher.objects.update_or_create(user=instance)
#     elif instance.role == 'student':
#         if Teacher.objects.filter(user_id=instance.id).exists():
#             Teacher.objects.filter(user_id=instance.id).delete()
#         Student.objects.update_or_create(user=instance)


    
# @receiver(pre_save, sender=Teacher)
# def pre_save_create_profile(sender, instance, **kwargs):
#     if Student.objects.filter(user_id=instance.user.id).exists():
#         raise ValueError ("This user is a student, please select another user")
