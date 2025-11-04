from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """基础模型，所有模型继承此类"""
    
    create_time = models.DateTimeField(
        default=timezone.now, 
        editable=False, 
        verbose_name="创建时间"
    )
    update_time = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间"
    )

    class Meta:
        abstract = True
