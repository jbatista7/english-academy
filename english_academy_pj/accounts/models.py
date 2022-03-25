from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.dispatch import receiver
from django.template import context
from .utils import generate_custom_id

from django.contrib.auth.models import Group, Permission


from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password. 
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

        
    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        # user.id = generate_custom_id(user)
        user.superuser = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    # staff = models.BooleanField(default=False) # a admin user; non super-user
    staff = models.BooleanField(default=False, verbose_name='admin') # a admin user; non super-user
    superuser = models.BooleanField(default=False) # a superuser
    admin = models.BooleanField(default=False) # a superuser
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # date_joined = timezone.now().today() - datetime.timedelta(days=options['days'])

    
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_role(self):
        return str(self.role)
    
    def full_name(self):
        # The user is identified by their email address
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return f"ID: {self.id}"

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.pk = generate_custom_id(self)
        super().save(*args, **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_superuser(self):
        "Is the user a admin member?"
        return self.superuser

    objects = UserManager()

    

    # class Meta:
         
    #     permissions = (
    #         ("can_go_in_non_ac_bus", "To provide non-AC Bus facility"),
    #         ("can_go_in_ac_bus", "To provide AC-Bus facility"),
    #         ("can_stay_ac-room", "To provide staying at AC room"),
    #         # ("can_stay_ac-room", "To provide staying at Non-AC room"),
    #         ("can_go_dehradoon", "Trip to Dehradoon"),
    #         ("can_go_mussoorie", "Trip to Mussoorie"),
    #         ("can_go_haridwaar", "Trip to Haridwaar"),
    #         ("can_go_rishikesh", "Trip to Rishikesh"),)


# class EmailConfirmed(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
#     activation_key = models.CharField(max_length=200)
#     confirmed = models.BooleanField(default=False)

#     def __unicode__(self):
#         return str(self.confirmed)

#     def active_user_email(self):
#         #send email here and render string
#         activation_url = f"http://localhost:8000/accounts/activate/{self.activation_key}"
#         context = {
#             "activation_key": self.activation_key,
#             "activation_url": activation_url,
#         }
#         body = render_to_string("accounts/activation_message.txt")
#         subject = "Activate your Email"
#         self.email_user(subject, body, settings.DEFAULT_FROM_EMAIL)

#     def email_user(self, subject, body, from_email=None, **kwargs):
#         email = EmailMessage(subject, 
#             body,    
#             settings.DEFAULT_FROM_EMAIL,            
#             ['mokka@gmail.com'],        
#             )
#         email.fail_silently = False
#         email.send()