# Generated by Django 3.2 on 2021-04-14 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=256)),
                ('room_places', models.ImageField(default=0, upload_to='')),
                ('project_available', models.BooleanField(default=False)),
            ],
        ),
    ]
