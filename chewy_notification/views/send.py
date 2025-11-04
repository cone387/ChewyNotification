from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from chewy_notification.models import (
    NotificationTemplate,
    NotificationTarget,
    NotificationRecord,
)
from chewy_notification.services import get_service_for_channel
from chewy_notification.tasks import send_notification_task
import logging

logger = logging.getLogger(__name__)


class NotificationSendView(APIView):
    """手动发送通知接口"""
    
    def post(self, request):
        """
        发送通知
        
        请求参数：
        - template_id: 模板ID
        - target_id: 目标ID
        - context: 变量上下文（可选）
        - async_send: 是否异步发送（可选，默认False）
        """
        template_id = request.data.get("template_id")
        target_id = request.data.get("target_id")
        context = request.data.get("context", {})
        async_send = request.data.get("async_send", False)
        
        # 验证参数
        if not template_id or not target_id:
            return Response(
                {"error": "template_id和target_id为必填项"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            template = NotificationTemplate.objects.select_related("channel").get(id=template_id)
            target = NotificationTarget.objects.get(id=target_id)
        except NotificationTemplate.DoesNotExist:
            return Response(
                {"error": "模板不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        except NotificationTarget.DoesNotExist:
            return Response(
                {"error": "目标不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查渠道是否启用
        if not template.channel.enabled:
            return Response(
                {"error": "渠道未启用"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建发送记录
        record = NotificationRecord.objects.create(
            template=template,
            channel=template.channel,
            target=target,
            status=NotificationRecord.Status.PENDING
        )
        
        # 异步或同步发送
        if async_send:
            # 使用 Celery 异步任务
            send_notification_task.delay(record.id, context)
            return Response(
                {
                    "message": "通知已加入发送队列",
                    "record_id": record.id,
                    "status": "pending"
                },
                status=status.HTTP_202_ACCEPTED
            )
        else:
            # 同步发送
            try:
                # 渲染模板
                title = self._render_template(template.title, context)
                content = self._render_template(template.content, context)
                
                # 获取服务并发送
                service = get_service_for_channel(template.channel)
                result = service.send(target.target_value, title, content)
                
                # 更新记录
                record.status = NotificationRecord.Status.SUCCESS
                record.response = result
                record.send_time = timezone.now()
                record.save()
                
                return Response(
                    {
                        "message": "发送成功",
                        "record_id": record.id,
                        "status": "success",
                        "response": result
                    },
                    status=status.HTTP_200_OK
                )
            
            except Exception as e:
                logger.error(f"发送通知失败: {str(e)}")
                record.status = NotificationRecord.Status.FAILED
                record.error_message = str(e)
                record.send_time = timezone.now()
                record.save()
                
                return Response(
                    {
                        "message": "发送失败",
                        "record_id": record.id,
                        "status": "failed",
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    
    def _render_template(self, template_str, context):
        """简单的模板变量替换"""
        for key, value in context.items():
            template_str = template_str.replace(f"{{{{{key}}}}}", str(value))
        return template_str
