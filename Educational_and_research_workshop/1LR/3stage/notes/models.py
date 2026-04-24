from django.db import models
from django.utils import timezone

class Note(models.Model):
    """Модель заметки - описывает, какие данные храним"""
    title = models.CharField(max_length=200)          # заголовок заметки
    text = models.TextField()                          # текст заметки
    created_date = models.DateTimeField(default=timezone.now)  # дата создания
    is_done = models.BooleanField(default=False)       # выполнено/нет
    
    def __str__(self):
        return self.title