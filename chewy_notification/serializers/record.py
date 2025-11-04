from rest_framework import serializers
from chewy_notification.models import NotificationRecord


class NotificationRecordSerializer(serializers.ModelSerializer):
    """通知记录序列化器"""
    
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    template_name = serializers.CharField(source="template.name", read_only=True, allow_null=True)
    channel_name = serializers.CharField(source="channel.name", read_only=True, allow_null=True)
    target_alias = serializers.CharField(source="target.alias", read_only=True, allow_null=True)
    
    class Meta:
        model = NotificationRecord
        fields = [
            "id",
            "template",
            "template_name",
            "channel",
            "channel_name",
            "target",
            "target_alias",
            "status",
            "status_display",
            "response",
            "send_time",
            "error_message",
            "create_time",
            "update_time",
        ]
        read_only_fields = [
            "id",
            "status",
            "response",
            "send_time",
            "error_message",
            "create_time",
            "update_time",
        ]
