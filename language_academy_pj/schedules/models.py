from django.db import models
from profiles.models import Teacher, Student
from lessons.models import Pack
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
    lesson_link = models.URLField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['date']
        unique_together = [['teacher', 'date'], ['student', 'date']]

    def __str__(self):
        return str(self.student.user)
