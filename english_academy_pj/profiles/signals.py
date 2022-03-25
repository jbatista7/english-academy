from .models import Teacher, Student
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import generate_token


User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.role:
        if instance.role == 'teacher':
            Teacher.objects.update_or_create(user=instance, id=instance.id)
            if Teacher.objects.get(id=instance.id).email_confirmed == False:
                site = settings.DEFAULT_DOMAIN
                # Email Address Confirmation Email
                protocol = site.split('://')[0]
                current_site = site.split('://')[1]#get_current_site(request)
                email_subject = "Confirm your MOKKA Account"
                body = render_to_string('profiles/email_confirmation.html',{
                    'protocol': protocol,
                    'domain': current_site,#current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                    'token': generate_token.make_token(instance)
                })

                email = EmailMessage(
                    email_subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [instance.email],
                    )
                email.fail_silently = False #True
                email.send()
        elif instance.role == 'student':
            Student.objects.update_or_create(user=instance, id=instance.id)
            if Student.objects.get(id=instance.id).email_confirmed == False:
                site = settings.DEFAULT_DOMAIN
                # Email Address Confirmation Email
                protocol = site.split('://')[0]
                current_site = site.split('://')[1]#get_current_site(request)
                email_subject = "Confirm your MOKKA Account"
                body = render_to_string('profiles/email_confirmation.html',{
                    'protocol': protocol,
                    'domain': current_site,#current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                    'token': generate_token.make_token(instance)
                })

                email = EmailMessage(
                    email_subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    # settings.DEFAULT_FROM_EMAIL,
                    [instance.email],
                    )
                email.fail_silently = False #True
                email.send()

        # myuser = User.objects.get(id=instance.id)

        

# @receiver(pre_save, sender=User)
# def user_updated(sender, **kwargs):
#     user = kwargs.get('instance', None)
#     if user:
#         new_password = user.password
#         try:
#             old_password = User.objects.get(pk=user.pk).password
#             print(old_password)
#         except User.DoesNotExist:
#             old_password = None
#         if new_password != old_password:
#             pass
#             # user.last_login = timezone.now()
#         # do what you need here
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
