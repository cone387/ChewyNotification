from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from chewy_notification.models import (
    NotificationChannel,
    NotificationTarget,
    NotificationRecord,
)
from chewy_notification.services import get_service_for_channel
from chewy_notification.tasks import send_notification_task
import logging

logger = logging.getLogger(__name__)


class QuickSendView(APIView):
    """快速发送通知接口（无需模板）"""
    
    def post(self, request):
        """
        快速发送通知
        
        请求参数：
        - channel_id: 渠道ID（必填）
        - target_ids: 目标ID列表（可选，不填则发送到所有目标）
        - title: 通知标题（必填）
        - content: 通知内容（必填）
        - async_send: 是否异步发送（可选，默认False）
        
        示例：
        {
            "channel_id": 1,
            "target_ids": [1, 2],  # 不填或填 "all" 表示全部设备
            "title": "测试通知",
            "content": "这是测试内容",
            "async_send": false
        }
        """
        channel_id = request.data.get("channel_id")
        target_ids = request.data.get("target_ids")  # 可以是列表或 "all"
        title = request.data.get("title")
        content = request.data.get("content")
        async_send = request.data.get("async_send", False)
        
        # 提取 Bark 扩展参数
        extra_params = {}
        bark_params = [
            "subtitle", "level", "badge", "sound", "icon", "group", "url",
            "copy", "auto_copy", "call", "is_archive"
        ]
        for param in bark_params:
            if param in request.data:
                extra_params[param] = request.data[param]
        
        # 验证必填参数
        if not channel_id or not title or not content:
            return Response(
                {"error": "channel_id、title 和 content 为必填项"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取渠道
        try:
            channel = NotificationChannel.objects.get(id=channel_id)
        except NotificationChannel.DoesNotExist:
            return Response(
                {"error": "渠道不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 检查渠道是否启用
        if not channel.enabled:
            return Response(
                {"error": "渠道未启用"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取目标列表
        if target_ids == "all" or target_ids is None:
            # 发送到该渠道类型的所有目标
            targets = self._get_targets_for_channel(channel)
        else:
            # 发送到指定目标
            try:
                targets = NotificationTarget.objects.filter(id__in=target_ids)
                if not targets.exists():
                    return Response(
                        {"error": "未找到有效的目标"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except Exception as e:
                return Response(
                    {"error": f"目标参数错误: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # 批量发送
        results = []
        for target in targets:
            if async_send:
                # 异步发送
                record = NotificationRecord.objects.create(
                    channel=channel,
                    target=target,
                    status=NotificationRecord.Status.PENDING
                )
                # 这里需要修改 task 以支持直接传入 title/content
                results.append({
                    "target_id": target.id,
                    "target_alias": target.alias,
                    "record_id": record.id,
                    "status": "queued"
                })
            else:
                # 同步发送
                result = self._send_to_target(channel, target, title, content, extra_params)
                results.append(result)
        
        return Response(
            {
                "message": f"已发送到 {len(results)} 个目标",
                "total": len(results),
                "results": results
            },
            status=status.HTTP_200_OK if all(r.get("status") == "success" for r in results) else status.HTTP_207_MULTI_STATUS
        )
    
    def _get_targets_for_channel(self, channel):
        """根据渠道类型获取匹配的目标"""
        # 渠道类型与目标类型的映射
        channel_target_map = {
            "bark": "bark_token",
            "email": "email",
            "ntfy": "ntfy_topic",
            "feishu": "feishu_webhook",
        }
        
        target_type = channel_target_map.get(channel.type)
        if target_type:
            return NotificationTarget.objects.filter(target_type=target_type)
        return NotificationTarget.objects.none()
    
    def _send_to_target(self, channel, target, title, content, extra_params=None):
        """发送到单个目标"""
        if extra_params is None:
            extra_params = {}
        
        # 创建发送记录
        record = NotificationRecord.objects.create(
            channel=channel,
            target=target,
            status=NotificationRecord.Status.PENDING
        )
        
        try:
            # 获取服务并发送（使用统一接口）
            service = get_service_for_channel(channel)
            result = service.send(
                target=target.target_value,
                title=title,
                content=content,
                **extra_params  # 传递所有扩展参数
            )
            
            # 更新记录
            record.status = NotificationRecord.Status.SUCCESS
            record.response = result
            record.send_time = timezone.now()
            record.save()
            
            return {
                "target_id": target.id,
                "target_alias": target.alias,
                "record_id": record.id,
                "status": "success",
                "response": result
            }
        
        except Exception as e:
            logger.error(f"发送到 {target.alias} 失败: {str(e)}")
            record.status = NotificationRecord.Status.FAILED
            record.error_message = str(e)
            record.send_time = timezone.now()
            record.save()
            
            return {
                "target_id": target.id,
                "target_alias": target.alias,
                "record_id": record.id,
                "status": "failed",
                "error": str(e)
            }
