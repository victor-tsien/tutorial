# wlog/models/title.py
from django.db import models
from django.utils import timezone


class Title(models.Model):
    """日志标题模型"""
    title_text = models.CharField(max_length=200, verbose_name="title")
    created_at = models.DateField("created at", default=timezone.now)

    class Meta:
        ordering = ['created_at']
        verbose_name = "title"
        verbose_name_plural = "log title"

    def __str__(self):
        return self.title_text