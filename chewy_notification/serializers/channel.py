from rest_framework import serializers
from chewy_notification.models import NotificationChannel


class NotificationChannelSerializer(serializers.ModelSerializer):
    """通知渠道序列化器"""
    
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    
    class Meta:
        model = NotificationChannel
        fields = [
            "id",
            "name",
            "type",
            "type_display",
            "config",
            "enabled",
            "create_time",
            "update_time",
        ]
        read_only_fields = ["id", "create_time", "update_time"]
    
    def validate_config(self, value):
        """验证渠道配置"""
        channel_type = self.initial_data.get("type")
        
        if channel_type == NotificationChannel.ChannelType.BARK:
            if "server_url" not in value:
                raise serializers.ValidationError("Bark渠道需要配置server_url")
        
        elif channel_type == NotificationChannel.ChannelType.NTFY:
            if "server_url" not in value:
                raise serializers.ValidationError("Ntfy渠道需要配置server_url")
        
        elif channel_type == NotificationChannel.ChannelType.EMAIL:
            required_fields = ["host", "port", "username", "password", "from_email"]
            for field in required_fields:
                if field not in value:
                    raise serializers.ValidationError(f"Email渠道需要配置{field}")
        
        elif channel_type == NotificationChannel.ChannelType.FEISHU:
            if "webhook_url" not in value:
                raise serializers.ValidationError("飞书渠道需要配置webhook_url")
        
        return value
