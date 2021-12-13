# Generated by Django 3.2.8 on 2021-11-21 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthBg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_the_week', models.CharField(max_length=5)),
                ('photo', models.ImageField(upload_to='photos')),
            ],
            options={
                'verbose_name': 'Auth Photos',
                'verbose_name_plural': 'Auth Photos',
            },
        ),
    ]