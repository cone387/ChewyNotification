from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """邮件通知服务"""
    
    def __init__(self, config):
        """
        初始化邮件服务
        
        配置示例:
        {
            "host": "smtp.gmail.com",
            "port": 587,
            "username": "your_email@gmail.com",
            "password": "your_password",
            "from_email": "your_email@gmail.com",
            "use_tls": true
        }
        """
        self.config = config
    
    def send(self, to_email, title, content):
        """
        发送邮件通知
        
        Args:
            to_email: 收件人邮箱
            title: 邮件标题
            content: 邮件内容
        
        Returns:
            dict: 发送结果
        """
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
            
            logger.info(f"邮件通知发送成功: {to_email}")
            return {
                "success": True,
                "to": to_email,
                "subject": title
            }
        
        except Exception as e:
            logger.error(f"邮件通知发送失败: {str(e)}")
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
