from django.contrib import admin
from chewy_notification.models import (
    NotificationChannel,
    NotificationTemplate,
    NotificationTarget,
    NotificationRecord,
)


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    """通知渠道管理"""
    
    list_display = ["name", "type", "enabled", "create_time", "update_time"]
    list_filter = ["type", "enabled", "create_time"]
    search_fields = ["name"]
    ordering = ["-create_time"]
    readonly_fields = ["create_time", "update_time"]
    
    fieldsets = (
        ("基本信息", {
            "fields": ("name", "type", "enabled")
        }),
        ("渠道配置", {
            "fields": ("config",),
            "description": "JSON格式的渠道配置信息"
        }),
        ("时间信息", {
            "fields": ("create_time", "update_time"),
            "classes": ("collapse",)
        }),
    )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """通知模板管理"""
    
    list_display = ["name", "title", "channel", "create_time"]
    list_filter = ["channel", "channel__type", "create_time"]
    search_fields = ["name", "title", "content"]
    ordering = ["-create_time"]
    readonly_fields = ["create_time", "update_time"]
    
    fieldsets = (
        ("基本信息", {
            "fields": ("name", "channel")
        }),
        ("模板内容", {
            "fields": ("title", "content"),
            "description": "支持 {{variable}} 语法进行变量替换"
        }),
        ("时间信息", {
            "fields": ("create_time", "update_time"),
            "classes": ("collapse",)
        }),
    )


@admin.register(NotificationTarget)
class NotificationTargetAdmin(admin.ModelAdmin):
    """通知目标管理"""
    
    list_display = ["alias", "target_type", "target_value", "create_time"]
    list_filter = ["target_type", "create_time"]
    search_fields = ["alias", "target_value"]
    ordering = ["-create_time"]
    readonly_fields = ["create_time", "update_time"]
    
    fieldsets = (
        ("基本信息", {
            "fields": ("alias", "target_type", "target_value")
        }),
        ("时间信息", {
            "fields": ("create_time", "update_time"),
            "classes": ("collapse",)
        }),
    )


@admin.register(NotificationRecord)
class NotificationRecordAdmin(admin.ModelAdmin):
    """通知记录管理"""
    
    list_display = [
        "id",
        "get_template_name",
        "get_channel_name",
        "get_target_alias",
        "status",
        "send_time",
        "create_time"
    ]
    list_filter = ["status", "channel__type", "create_time", "send_time"]
    search_fields = ["template__name", "error_message"]
    ordering = ["-create_time"]
    readonly_fields = [
        "template",
        "channel",
        "target",
        "status",
        "response",
        "send_time",
        "error_message",
        "create_time",
        "update_time"
    ]
    
    fieldsets = (
        ("关联信息", {
            "fields": ("template", "channel", "target")
        }),
        ("发送状态", {
            "fields": ("status", "send_time", "error_message")
        }),
        ("响应信息", {
            "fields": ("response",),
            "classes": ("collapse",)
        }),
        ("时间信息", {
            "fields": ("create_time", "update_time"),
            "classes": ("collapse",)
        }),
    )
    
    def get_template_name(self, obj):
        return obj.template.name if obj.template else "-"
    get_template_name.short_description = "模板"
    
    def get_channel_name(self, obj):
        return obj.channel.name if obj.channel else "-"
    get_channel_name.short_description = "渠道"
    
    def get_target_alias(self, obj):
        return obj.target.alias if obj.target else "-"
    get_target_alias.short_description = "目标"
    
    def has_add_permission(self, request):
        """禁止手动添加记录"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改记录"""
        return False
