# Generated by Django 3.2.8 on 2022-02-02 10:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lessons', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchasedPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.pack')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.student')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_link', models.URLField(blank=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('finished', 'Finished')], default='active', max_length=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.teacher')),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
                'ordering': ['date'],
                'unique_together': {('teacher', 'date')},
            },
        ),
    ]
