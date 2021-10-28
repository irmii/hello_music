from django.db import models

from polls.consts import MAXLENGTH50, DEFAULT_LESSON_COUNT


class Students(models.Model):
    foreign_id = models.IntegerField('Внешнее айди в системе', primary_key=True)
    name = models.CharField('Имя', max_length=MAXLENGTH50, null=True)
    email = models.EmailField('Емаил', null=True)
    phone = models.CharField('Телефон', max_length=MAXLENGTH50, null=True)
    status_id = models.IntegerField('Статус клиента')

    def __str__(self):
        return self.name + ' ' + self.phone

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class SendMessagesLog(models.Model):
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
    )
    created_at = models.DateField('Дата создания записи', auto_now_add=True)
    is_message_send = models.BooleanField('Сообщение отправлено? Да,нет', default=False)
    lessons_passed = models.IntegerField('Количество пройденных уроков', default=DEFAULT_LESSON_COUNT)
    is_last_lesson_was_yesterday = models.BooleanField('Последний урок был вчера? Да,нет', default=False)

    class Meta:
        verbose_name = 'Лог отправки сообщений'
        verbose_name_plural = 'Лог отправки сообщений'
