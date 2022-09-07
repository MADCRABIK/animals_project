from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Dialog(models.Model):
    objects = models.Manager()

    members = models.ManyToManyField(User, verbose_name='Участник', max_length=2)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    def __str__(self):
        return f'Диалог №{self.pk}'


class Message(models.Model):
    objects = models.Manager()

    dialog = models.ForeignKey(Dialog, verbose_name='Диалог', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель', related_name='sender')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Получатель', related_name='recipient')
    sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'Сообщение №{self.pk} от {self.from_user} для {self.to_user}'

    def get_absolute_url(self):
        return self

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['sent']
