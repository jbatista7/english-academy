from django.db import models

# Create your models here.

class AuthBg(models.Model):
    WEEK_DAY_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )

    week_day = models.CharField(max_length=5, choices=WEEK_DAY_CHOICES, unique=True)
    photo = models.ImageField(upload_to='photos')

    class Meta:
        verbose_name = 'Auth Photos'
        verbose_name_plural = 'Auth Photos'
        ordering = ['week_day']

    def __str__(self):
        return str(self.week_day)
    