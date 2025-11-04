from django.db import models
from .base import BaseModel
from .channel import NotificationChannel


class NotificationTemplate(BaseModel):
    """通知模板模型"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="模板名称",
        help_text="模板的唯一标识名称"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="标题模板",
        help_text="通知标题，支持变量替换"
    )
    content = models.TextField(
        verbose_name="内容模板",
        help_text="通知内容，支持变量替换"
    )
    channel = models.ForeignKey(
        NotificationChannel,
        on_delete=models.CASCADE,
        related_name="templates",
        verbose_name="所属渠道",
        help_text="该模板使用的通知渠道"
    )
    
    class Meta:
        db_table = "chewy_notify_template"
        verbose_name = "通知模板"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
    
    def __str__(self):
        return f"{self.name} - {self.channel.name}"
