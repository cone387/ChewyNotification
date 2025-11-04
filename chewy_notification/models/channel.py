from django.db import models
from .base import BaseModel


class NotificationChannel(BaseModel):
    """通知渠道模型"""
    
    class ChannelType(models.TextChoices):
        BARK = "bark", "Bark"
        NTFY = "ntfy", "Ntfy"
        EMAIL = "email", "Email"
        FEISHU = "feishu", "飞书"
    
    name = models.CharField(
        max_length=100,
        verbose_name="渠道名称",
        help_text="渠道的显示名称"
    )
    type = models.CharField(
        max_length=20,
        choices=ChannelType.choices,
        verbose_name="渠道类型",
        help_text="选择通知渠道类型"
    )
    config = models.JSONField(
        default=dict,
        verbose_name="渠道配置",
        help_text="JSON格式的渠道配置信息"
    )
    enabled = models.BooleanField(
        default=True,
        verbose_name="是否启用",
        help_text="是否启用该渠道"
    )
    
    class Meta:
        db_table = "chewy_notify_channel"
        verbose_name = "通知渠道"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
