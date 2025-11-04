from django.db import models
from .base import BaseModel
from .channel import NotificationChannel
from .template import NotificationTemplate
from .target import NotificationTarget


class NotificationRecord(BaseModel):
    """通知发送记录模型"""
    
    class Status(models.TextChoices):
        PENDING = "pending", "待发送"
        SUCCESS = "success", "发送成功"
        FAILED = "failed", "发送失败"
        RETRY = "retry", "重试中"
    
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="records",
        verbose_name="使用模板",
        help_text="发送时使用的模板"
    )
    channel = models.ForeignKey(
        NotificationChannel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="records",
        verbose_name="发送渠道",
        help_text="使用的发送渠道"
    )
    target = models.ForeignKey(
        NotificationTarget,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="records",
        verbose_name="通知目标",
        help_text="接收通知的目标"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="发送状态"
    )
    response = models.JSONField(
        default=dict,
        verbose_name="响应信息",
        help_text="发送后的响应数据"
    )
    send_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="发送时间",
        help_text="实际发送的时间"
    )
    error_message = models.TextField(
        blank=True,
        default="",
        verbose_name="错误信息",
        help_text="发送失败时的错误信息"
    )
    
    class Meta:
        db_table = "chewy_notify_record"
        verbose_name = "通知记录"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["-create_time"]),
            models.Index(fields=["status"]),
        ]
    
    def __str__(self):
        return f"{self.channel} -> {self.target} ({self.get_status_display()})"
