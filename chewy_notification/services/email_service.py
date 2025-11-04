from django.core.mail import EmailMessage
from django.conf import settings
import logging
from .base_service import BaseNotificationService

logger = logging.getLogger(__name__)


class EmailService(BaseNotificationService):
    """邮件通知服务"""
    
    def __init__(self, config):
        super().__init__(config)
    
    def _send_implementation(self, payload):
        """
        邮件的具体发送实现
        
        邮件支持部分 Bark 参数：
        - title: 标题
        - content/body: 内容
        - subtitle: 可添加到内容中
        
        Args:
            payload: 参数字典
            
        Returns:
            dict: 发送结果
        """
        to_email = payload["target"]
        title = payload["title"]
        content = payload["content"]
        
        # 如果有 subtitle，添加到内容中
        if "subtitle" in payload:
            content = f"{payload['subtitle']}\n\n{content}"
        
        # 如果有 URL，添加到内容末尾
        if "url" in payload:
            content = f"{content}\n\n🔗 {payload['url']}"
        
        try:
            # 创建邮件
            email = EmailMessage(
                subject=title,
                body=content,
                from_email=self.config.get("from_email"),
                to=[to_email],
                connection=self._get_connection()
            )
            
            # 发送
            email.send(fail_silently=False)
            
            return {
                "success": True,
                "to": to_email,
                "subject": title
            }
        
        except Exception as e:
            raise Exception(f"邮件发送失败: {str(e)}")
    
    def _get_connection(self):
        """获取邮件连接"""
        from django.core.mail import get_connection
        
        return get_connection(
            backend="django.core.mail.backends.smtp.EmailBackend",
            host=self.config.get("host"),
            port=self.config.get("port", 587),
            username=self.config.get("username"),
            password=self.config.get("password"),
            use_tls=self.config.get("use_tls", True),
            fail_silently=False
        )
