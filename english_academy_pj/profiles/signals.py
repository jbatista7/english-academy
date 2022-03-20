from .models import Teacher, Student
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.role:
        if instance.role == 'teacher':
            Teacher.objects.update_or_create(user=instance, id=instance.id)
        elif instance.role == 'student':
            Student.objects.update_or_create(user=instance, id=instance.id)

#         print(instance)
#         print(instance.email)
#         print(User)
#         # 
#         # 
#         # 
#         token_generator = PasswordResetTokenGenerator()
#         token = token_generator.make_token(instance)
#         print(instance.reque)
#         current_site = 'http://127.0.0.1:8000' #get_current_site(request)
#         print(token)
#         email_subject = 'mokka confirmation link'
#         template = render_to_string('profiles/activate_email.html',{
#             'domain': current_site.domain, 
#             'uid': urlsafe_base64_encode(force_bytes(instance)),
#             'token': token
#         })
 
#         email = EmailMessage(
#             email_subject,
#             template,
#             settings.EMAIL_BACKEND,
#             [instance.email]
#         )
#         email.fail_silently=False
#         email.send()
# #         # email_body = render_to_string('authentication/activate.html', {
# #         #     'user': user,
# #         #     'domain': current_site,
# #         #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# #         #     'token': generate_token.make_token(user)
# #         # })

# #         # email = EmailMessage(subject=email_subject, body=email_body,
# #         #                  from_email=settings.EMAIL_FROM_USER,
# #         #                  to=[User.get.email]
# #         #                  )

# #         # subject = "Password Reset Requested"
# #         # email_template_name = "main/password/password_reset_email.txt"
# #         # c = {
# #         # "email":user.email,
# #         # 'domain':'127.0.0.1:8000',
# #         # 'site_name': 'Website',
# #         # "uid": urlsafe_base64_encode(force_bytes(user.pk)),
# #         # "user": user,
# #         # 'token': default_token_generator.make_token(user),
# #         # 'protocol': 'http',
# #         # }
# #         # email = render_to_string(email_template_name, c)
# #         # try:
# #         #     send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False) 



# #         # 
# #         # 
# #         # 
# #         # 
# #         # 
# #         # 






# # #     def create_profile(sender, **kwargs):
# # #     if kwargs["created"]:
# # #         p = Profile(user=kwargs["instance"], ...)
# # #         p.save()
# # # django.db.models.signals.post_save.connect(create_profile, sender=User)
# #     # if created:
# #     #     print(instance.role)
# #     #     if instance.role == 'teacher':
# #     #         Teacher.objects.create(user=instance)
# #     #     elif instance.role == 'student':
# #     #         Student.objects.create(user=instance)
# #         # Student.objects.create(user=instance)



# # # @receiver(post_save, sender=User)
# # # def save_profile(sender, instance, **kwargs):
# # #     if instance.role == 'teacher':
# # #         if Student.objects.filter(user_id=instance.id).exists():
# # #             Student.objects.filter(user_id=instance.id).delete()
# # #         Teacher.objects.update_or_create(user=instance)
# # #     elif instance.role == 'student':
# # #         if Teacher.objects.filter(user_id=instance.id).exists():
# # #             Teacher.objects.filter(user_id=instance.id).delete()
# # #         Student.objects.update_or_create(user=instance)


    
# # # @receiver(pre_save, sender=Teacher)
# # # def pre_save_create_profile(sender, instance, **kwargs):
# # #     if Student.objects.filter(user_id=instance.user.id).exists():
# # #         raise ValueError ("This user is a student, please select another user")
