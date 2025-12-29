# wlog/models/log.py
from django.db import models
from .title import Title


class Log(models.Model):
    """日志条目模型"""
    title = models.ForeignKey(
        Title, 
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='title to which'
    )
    log_text = models.TextField(verbose_name="log content")
    created_at = models.DateField('created at', auto_now_add=True)
    updated_at = models.DateField('updated at', auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'log entry'
        verbose_name_plural = 'log entries'

    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y/%m/%d')}"