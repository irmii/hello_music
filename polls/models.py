from django.db import models

from polls.consts import MAXLENGTH50


class Students(models.Model):
    foreign_id = models.IntegerField('Внешнее айди в системе', primary_key=True)
    name = models.CharField('Имя', max_length=MAXLENGTH50, null=True)
    email = models.EmailField('Емаил', null=True)
    phone = models.CharField('Телефон', max_length=MAXLENGTH50, null=True)
    status_id = models.IntegerField('Статус клиента')
