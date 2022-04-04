from .models import Teacher, Student
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator


User = get_user_model()

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if instance.role:
        if instance.role == 'teacher':
            Teacher.objects.update_or_create(user=instance, id=instance.id)
            if created:
                if Teacher.objects.get(id=instance.id).email_confirmed == False:
                    # Email Address Confirmation Email
                    site = settings.DEFAULT_DOMAIN
                    token_maker = PasswordResetTokenGenerator()
                    protocol = site.split('://')[0]
                    current_site = site.split('://')[1]#get_current_site(request)
                    email_subject = "Confirm your MOKKA Account"
                    body = render_to_string('profiles/email_confirmation.html',{
                        'protocol': protocol,
                        'domain': current_site,#current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                        'token': token_maker.make_token(instance)
                    })

                    email = EmailMessage(
                        email_subject,
                        body,
                        settings.EMAIL_HOST_USER,
                        [instance.email],
                        )
                    # email.fail_silently = False #True
                    email.send()
        elif instance.role == 'student':
            Student.objects.update_or_create(user=instance, id=instance.id)
            if created:
                if Student.objects.get(id=instance.id).email_confirmed == False: 
                    # Email Address Confirmation Email
                    site = settings.DEFAULT_DOMAIN
                    token_maker = PasswordResetTokenGenerator()
                    protocol = site.split('://')[0]
                    current_site = site.split('://')[1]#get_current_site(request)
                    email_subject = "Confirm your MOKKA Account"
                    body = render_to_string('profiles/email_confirmation.html',{
                        'protocol': protocol,
                        'domain': current_site,#current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                        'token': token_maker.make_token(instance)
                    })

                    email = EmailMessage(
                        email_subject,
                        body,
                        settings.EMAIL_HOST_USER,
                        # settings.DEFAULT_FROM_EMAIL,
                        [instance.email],
                        )
                    # email.fail_silently = False #True
                    email.send()