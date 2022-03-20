from django.db import models
from multiselectfield import MultiSelectField
# from users.models import CustomUser
from lessons.models import Category
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email_confirmed = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ['user__username']
        abstract = True

    def __str__(self):
        return self.user

class Student(Profile):
    # id = models.field
    avatar = models.ImageField(upload_to='avatars/students', default='avatar.png')
    balance = models.FloatField(help_text='in US dollars $', default=0.0)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.avatar.path):
            os.remove(self.avatar.path)
        super(Student, self).delete(*args, **kwargs)

    def __str__(self):
        return str(f"{self.user.id} - {self.user.full_name()}")

    def full_name(self):
        return str(self.user.full_name())

class Teacher(Profile):
    
    HOURS_CHOICES = (
                    (0, '12:00 AM'),
                    (1, '01:00 AM'),
                    (2, '02:00 AM'),
                    (3, '03:00 AM'),
                    (4, '04:00 AM'),
                    (5, '05:00 AM'),
                    (6, '06:00 AM'),
                    (7, '07:00 AM'),
                    (8, '08:00 AM'),
                    (9, '09:00 AM'),
                    (10, '10:00 AM'),
                    (11, '11:00 AM'),
                    (12, '12:00 PM'),
                    (13, '01:00 PM'),
                    (14, '02:00 PM'),
                    (15, '03:00 PM'),
                    (16, '04:00 PM'),
                    (17, '05:00 PM'),
                    (18, '06:00 PM'),
                    (19, '07:00 PM'),
                    (20, '08:00 PM'),
                    (21, '09:00 PM'),
                    (22, '10:00 PM'),
                    (23, '11:00 PM'),
                )

    WEEK_DAYS_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
                    
    LANGUAGE_CHOICES = (
        ('english_adults', 'English_Adults'),
        ('english_children', 'English_Children'),
        ('español_adults', 'Español_Adults'),
        ('español_children', 'Español_Children'),
    )
    
    avatar = models.ImageField(upload_to='avatars/teachers', default='avatar.png')
    # category = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    sunday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Sunday', blank=True, null=True)
    monday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Monday', blank=True, null=True)
    tuesday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Tuesday', blank=True, null=True)
    wednesday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Wednesday', blank=True, null=True)
    thursday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Thursday', blank=True, null=True)
    friday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Friday', blank=True, null=True)
    saturday = MultiSelectField(choices=HOURS_CHOICES, verbose_name='Saturday', blank=True, null=True)
    # hours = MultiSelectField(choices=HOURS_CHOICES)
    # week_days = MultiSelectField(choices=WEEK_DAYS_CHOICES)

    def __str__(self):
        return str(self.user.full_name())

    def full_name(self):
        return str(self.user.full_name())
