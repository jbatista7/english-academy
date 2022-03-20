from tabnanny import verbose
from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)
    


class Pack(models.Model):
    LANGUAGE_CHOICES = (
        ('english_adults', 'English_Adults'),
        ('english_children', 'English_Children'),
        ('español_adults', 'Español_Adults'),
        ('español_children', 'Español_Children'),
    )
    # LANGUAGE_CHOICES = [
    #     ('english', 'English'),
    #     ('spanish', 'Spanish'),
    # ]

    # LEVEL_CHOICES = [
    #     ('a1', 'A1'),
    #     ('a2', 'A2'),
    #     ('b1', 'B1'),
    #     ('b2', 'B2'),
    #     ('c1', 'C1'),
    #     ('c2', 'C2'),
    #     ('d1', 'D1'),
    #     ('d2', 'D2'),
    # ]

    name = models.CharField(max_length=200)
    language = models.ForeignKey(Category, on_delete=models.CASCADE)
    number_of_lessons = models.PositiveSmallIntegerField()
    package_price = models.DecimalField(help_text='in US dollars $', max_digits=6, default=0.0, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class SupportAndSales(models.Model):
    name = models.CharField(max_length=100)
    supportUrl = models.URLField(verbose_name='link')

    class Meta:
        verbose_name_plural = 'Support and sales'

    def __str__(self):
        return str(self.name)


class Magazines(models.Model):
    name = models.CharField(max_length=100)
    magazineUrl = models.URLField(verbose_name='link')

    class Meta:
        verbose_name_plural = 'Magazines'

    def __str__(self):
        return str(self.name)

    
