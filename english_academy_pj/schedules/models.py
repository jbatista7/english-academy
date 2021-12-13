from django.db import models
from django.db.models.fields import related
from profiles.models import Teacher, Student
from lessons.models import Pack
from django.shortcuts import reverse
from django.utils import timezone

# Create your models here.

class PurchasedPackage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.student)

class Task(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('finished', 'Finished'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # pack = models.ForeignKey(Pack, on_delete=models.CASCADE)
    # lesson = models.PositiveSmallIntegerField(help_text='lesson hours')
    lesson_link = models.URLField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['date']
        unique_together = ['teacher', 'date']

    def __str__(self):
        return str(self.student.user)

    # def get_absolute_url(self):
    #     return reverse('schedules:detail', kwargs={'pk': self.pk})