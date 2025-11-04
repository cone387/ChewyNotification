from .bark_service import BarkService
from .ntfy_service import NtfyService
from .email_service import EmailService
from .feishu_service import FeishuService


def get_service_for_channel(channel):
    """根据渠道类型获取对应的服务实例"""
    from chewy_notification.models import NotificationChannel
    
    service_map = {
        NotificationChannel.ChannelType.BARK: BarkService,
        NotificationChannel.ChannelType.NTFY: NtfyService,
        NotificationChannel.ChannelType.EMAIL: EmailService,
        NotificationChannel.ChannelType.FEISHU: FeishuService,
    }
    
    service_class = service_map.get(channel.type)
    if not service_class:
        raise ValueError(f"不支持的渠道类型: {channel.type}")
    
    return service_class(channel.config)


__all__ = [
    "BarkService",
    "NtfyService",
    "EmailService",
    "FeishuService",
    "get_service_for_channel",
]
