from django.db import models
from .base import BaseModel


class NotificationTarget(BaseModel):
    """通知目标模型"""
    
    class TargetType(models.TextChoices):
        BARK_TOKEN = "bark_token", "Bark Token"
        EMAIL = "email", "Email地址"
        NTFY_TOPIC = "ntfy_topic", "Ntfy主题"
        FEISHU_WEBHOOK = "feishu_webhook", "飞书Webhook"
    
    alias = models.CharField(
        max_length=100,
        verbose_name="目标别名",
        help_text="通知目标的显示名称"
    )
    target_type = models.CharField(
        max_length=20,
        choices=TargetType.choices,
        verbose_name="目标类型",
        help_text="通知目标的类型"
    )
    target_value = models.CharField(
        max_length=500,
        verbose_name="目标值",
        help_text="具体的通知目标值（如邮箱、token等）"
    )
    
    class Meta:
        db_table = "chewy_notify_target"
        verbose_name = "通知目标"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
        unique_together = [["target_type", "target_value"]]
    
    def __str__(self):
        return f"{self.alias} ({self.get_target_type_display()})"
