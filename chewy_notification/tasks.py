from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# 尝试导入 Celery
try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    # 如果没有 Celery，创建一个装饰器占位符
    def shared_task(func):
        return func


@shared_task
def send_notification_task(record_id, context=None):
    """
    异步发送通知任务
    
    Args:
        record_id: 通知记录ID
        context: 模板变量上下文
    """
    from chewy_notification.models import NotificationRecord
    from chewy_notification.services import get_service_for_channel
    
    context = context or {}
    
    try:
        record = NotificationRecord.objects.select_related(
            "template", "channel", "target"
        ).get(id=record_id)
        
        # 渲染模板
        title = _render_template(record.template.title, context)
        content = _render_template(record.template.content, context)
        
        # 获取服务并发送
        service = get_service_for_channel(record.channel)
        result = service.send(record.target.target_value, title, content)
        
        # 更新记录状态
        record.status = NotificationRecord.Status.SUCCESS
        record.response = result
        record.send_time = timezone.now()
        record.save()
        
        logger.info(f"通知发送成功: record_id={record_id}")
        return {"success": True, "record_id": record_id}
    
    except NotificationRecord.DoesNotExist:
        logger.error(f"通知记录不存在: record_id={record_id}")
        return {"success": False, "error": "记录不存在"}
    
    except Exception as e:
        logger.error(f"通知发送失败: record_id={record_id}, error={str(e)}")
        
        try:
            record = NotificationRecord.objects.get(id=record_id)
            record.status = NotificationRecord.Status.FAILED
            record.error_message = str(e)
            record.send_time = timezone.now()
            record.save()
        except Exception:
            pass
        
        return {"success": False, "error": str(e)}


def _render_template(template_str, context):
    """简单的模板变量替换"""
    for key, value in context.items():
        template_str = template_str.replace(f"{{{{{key}}}}}", str(value))
    return template_str
