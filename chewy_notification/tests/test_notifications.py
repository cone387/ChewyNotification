from django.test import TestCase
from django.utils import timezone
from chewy_notification.models import (
    NotificationChannel,
    NotificationTemplate,
    NotificationTarget,
    NotificationRecord,
)
from chewy_notification.services import get_service_for_channel
from chewy_notification.utils import render_notification_content


class NotificationChannelTestCase(TestCase):
    """通知渠道测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.bark_channel = NotificationChannel.objects.create(
            name="测试Bark渠道",
            type=NotificationChannel.ChannelType.BARK,
            config={"server_url": "https://api.day.app"},
            enabled=True
        )
    
    def test_create_channel(self):
        """测试创建渠道"""
        self.assertEqual(self.bark_channel.name, "测试Bark渠道")
        self.assertEqual(self.bark_channel.type, "bark")
        self.assertTrue(self.bark_channel.enabled)
    
    def test_channel_str(self):
        """测试渠道字符串表示"""
        self.assertIn("Bark", str(self.bark_channel))


class NotificationTemplateTestCase(TestCase):
    """通知模板测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.channel = NotificationChannel.objects.create(
            name="测试渠道",
            type=NotificationChannel.ChannelType.BARK,
            config={"server_url": "https://api.day.app"},
            enabled=True
        )
        
        self.template = NotificationTemplate.objects.create(
            name="测试模板",
            title="欢迎 {{name}}",
            content="你好，{{name}}！欢迎使用通知系统。",
            channel=self.channel
        )
    
    def test_create_template(self):
        """测试创建模板"""
        self.assertEqual(self.template.name, "测试模板")
        self.assertEqual(self.template.channel, self.channel)
    
    def test_template_rendering(self):
        """测试模板渲染"""
        context = {"name": "张三"}
        title = render_notification_content(self.template.title, context)
        content = render_notification_content(self.template.content, context)
        
        self.assertEqual(title, "欢迎 张三")
        self.assertIn("你好，张三", content)


class NotificationTargetTestCase(TestCase):
    """通知目标测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.target = NotificationTarget.objects.create(
            alias="测试邮箱",
            target_type=NotificationTarget.TargetType.EMAIL,
            target_value="test@example.com"
        )
    
    def test_create_target(self):
        """测试创建目标"""
        self.assertEqual(self.target.alias, "测试邮箱")
        self.assertEqual(self.target.target_type, "email")
    
    def test_unique_constraint(self):
        """测试唯一性约束"""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            NotificationTarget.objects.create(
                alias="重复邮箱",
                target_type=NotificationTarget.TargetType.EMAIL,
                target_value="test@example.com"  # 相同的类型和值
            )


class NotificationRecordTestCase(TestCase):
    """通知记录测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.channel = NotificationChannel.objects.create(
            name="测试渠道",
            type=NotificationChannel.ChannelType.BARK,
            config={"server_url": "https://api.day.app"},
            enabled=True
        )
        
        self.template = NotificationTemplate.objects.create(
            name="测试模板",
            title="测试标题",
            content="测试内容",
            channel=self.channel
        )
        
        self.target = NotificationTarget.objects.create(
            alias="测试目标",
            target_type=NotificationTarget.TargetType.BARK_TOKEN,
            target_value="test_token"
        )
        
        self.record = NotificationRecord.objects.create(
            template=self.template,
            channel=self.channel,
            target=self.target,
            status=NotificationRecord.Status.PENDING
        )
    
    def test_create_record(self):
        """测试创建记录"""
        self.assertEqual(self.record.status, "pending")
        self.assertIsNone(self.record.send_time)
    
    def test_update_record_status(self):
        """测试更新记录状态"""
        self.record.status = NotificationRecord.Status.SUCCESS
        self.record.send_time = timezone.now()
        self.record.save()
        
        self.assertEqual(self.record.status, "success")
        self.assertIsNotNone(self.record.send_time)


class ServiceTestCase(TestCase):
    """服务层测试"""
    
    def test_get_service_for_bark(self):
        """测试获取Bark服务"""
        channel = NotificationChannel.objects.create(
            name="Bark渠道",
            type=NotificationChannel.ChannelType.BARK,
            config={"server_url": "https://api.day.app"},
            enabled=True
        )
        
        service = get_service_for_channel(channel)
        self.assertIsNotNone(service)
    
    def test_get_service_for_invalid_type(self):
        """测试获取无效类型的服务"""
        # 创建一个渠道但设置无效类型（仅用于测试）
        channel = NotificationChannel()
        channel.type = "invalid_type"
        channel.config = {}
        
        with self.assertRaises(ValueError):
            get_service_for_channel(channel)


class UtilsTestCase(TestCase):
    """工具函数测试"""
    
    def test_render_notification_content(self):
        """测试内容渲染"""
        template = "Hello {{name}}, you have {{count}} messages."
        context = {"name": "Alice", "count": 5}
        
        result = render_notification_content(template, context)
        self.assertEqual(result, "Hello Alice, you have 5 messages.")
    
    def test_render_with_missing_variable(self):
        """测试缺少变量的渲染"""
        template = "Hello {{name}}, you have {{count}} messages."
        context = {"name": "Bob"}
        
        result = render_notification_content(template, context)
        # 未提供的变量保持原样
        self.assertIn("{{count}}", result)
