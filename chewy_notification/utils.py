"""工具函数模块"""
from typing import Dict, Any


def render_notification_content(template: str, context: Dict[str, Any]) -> str:
    """
    渲染通知内容
    
    Args:
        template: 模板字符串，使用 {{variable}} 语法
        context: 变量字典
    
    Returns:
        渲染后的字符串
    
    Example:
        >>> render_notification_content("Hello {{name}}!", {"name": "World"})
        'Hello World!'
    """
    result = template
    for key, value in context.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


def validate_channel_config(channel_type: str, config: Dict[str, Any]) -> tuple[bool, str]:
    """
    验证渠道配置
    
    Args:
        channel_type: 渠道类型
        config: 配置字典
    
    Returns:
        (是否有效, 错误信息)
    """
    from chewy_notification.models import NotificationChannel
    
    validations = {
        NotificationChannel.ChannelType.BARK: ["server_url"],
        NotificationChannel.ChannelType.NTFY: ["server_url"],
        NotificationChannel.ChannelType.EMAIL: ["host", "port", "username", "password", "from_email"],
        NotificationChannel.ChannelType.FEISHU: ["webhook_url"],
    }
    
    required_fields = validations.get(channel_type)
    if not required_fields:
        return False, f"未知的渠道类型: {channel_type}"
    
    missing_fields = [field for field in required_fields if field not in config]
    
    if missing_fields:
        return False, f"缺少必要配置项: {', '.join(missing_fields)}"
    
    return True, ""


def format_notification_record(record) -> Dict[str, Any]:
    """
    格式化通知记录为字典
    
    Args:
        record: NotificationRecord 实例
    
    Returns:
        格式化后的字典
    """
    return {
        "id": record.id,
        "template": record.template.name if record.template else None,
        "channel": record.channel.name if record.channel else None,
        "target": record.target.alias if record.target else None,
        "status": record.get_status_display(),
        "send_time": record.send_time.isoformat() if record.send_time else None,
        "create_time": record.create_time.isoformat(),
        "error_message": record.error_message,
    }
