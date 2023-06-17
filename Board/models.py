from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    content = RichTextUploadingField(blank=True, null=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    not_accepted_yet = 'not accepted yet'
    response_accepted = 'response accepted'
    choice = (('not accepted yet', 'Отклик ещё не принят'),
              ('response accepted', 'Отклик принят'))
    status = models.CharField(choices=choice, default=not_accepted_yet, max_length=20)
    deleted = models.BooleanField(default=False)


class Category(models.Model):

    CATEGORIES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    ]
    name = models.CharField('Категория', max_length=30, choices=CATEGORIES, default='Танки')

    def __str__(self):
        return f'{self.name}'
