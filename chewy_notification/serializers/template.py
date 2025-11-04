from rest_framework import serializers
from chewy_notification.models import NotificationTemplate, NotificationChannel


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """通知模板序列化器"""
    
    channel_name = serializers.CharField(source="channel.name", read_only=True)
    channel_type = serializers.CharField(source="channel.type", read_only=True)
    
    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "name",
            "title",
            "content",
            "channel",
            "channel_name",
            "channel_type",
            "create_time",
            "update_time",
        ]
        read_only_fields = ["id", "create_time", "update_time"]
    
    def validate_channel(self, value):
        """验证渠道是否启用"""
        if not value.enabled:
            raise serializers.ValidationError("所选渠道未启用")
        return value
