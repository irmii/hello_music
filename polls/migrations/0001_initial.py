# Generated by Django 3.2.7 on 2021-09-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('foreign_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Внешнее айди в системе')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Емаил')),
                ('phone', models.CharField(max_length=50, verbose_name='Телефон')),
                ('status_id', models.IntegerField(verbose_name='Статус клиента')),
            ],
        ),
    ]
