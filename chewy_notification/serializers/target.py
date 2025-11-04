from rest_framework import serializers
from chewy_notification.models import NotificationTarget
import re


class NotificationTargetSerializer(serializers.ModelSerializer):
    """通知目标序列化器"""
    
    target_type_display = serializers.CharField(source="get_target_type_display", read_only=True)
    
    class Meta:
        model = NotificationTarget
        fields = [
            "id",
            "alias",
            "target_type",
            "target_type_display",
            "target_value",
            "create_time",
            "update_time",
        ]
        read_only_fields = ["id", "create_time", "update_time"]
    
    def validate(self, attrs):
        """验证目标值格式"""
        target_type = attrs.get("target_type")
        target_value = attrs.get("target_value")
        
        if target_type == NotificationTarget.TargetType.EMAIL:
            # 验证邮箱格式
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, target_value):
                raise serializers.ValidationError({"target_value": "邮箱格式不正确"})
        
        elif target_type == NotificationTarget.TargetType.FEISHU_WEBHOOK:
            # 验证webhook URL格式
            if not target_value.startswith("https://"):
                raise serializers.ValidationError({"target_value": "飞书Webhook必须以https://开头"})
        
        return attrs
