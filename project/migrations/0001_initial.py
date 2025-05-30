# Generated by Django 5.2.1 on 2025-05-31 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('details', models.TextField()),
                ('target', models.CharField(max_length=50)),
                ('S_time', models.DateTimeField(auto_now_add=True)),
                ('E_time', models.DateField()),
                ('is_featured', models.BooleanField(default=False)),
                ('is_cancle', models.BooleanField(default=False)),
                ('category_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
