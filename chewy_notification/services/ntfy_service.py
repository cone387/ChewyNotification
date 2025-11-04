import requests
import logging

logger = logging.getLogger(__name__)


class NtfyService:
    """Ntfy 通知服务"""
    
    def __init__(self, config):
        """
        初始化 Ntfy 服务
        
        配置示例:
        {
            "server_url": "https://ntfy.sh",
            "token": "optional_token"
        }
        """
        self.server_url = config.get("server_url", "https://ntfy.sh")
        self.token = config.get("token")
    
    def send(self, topic, title, content):
        """
        发送 Ntfy 通知
        
        Args:
            topic: Ntfy 主题
            title: 通知标题
            content: 通知内容
        
        Returns:
            dict: 发送结果
        """
        url = f"{self.server_url}/{topic}"
        headers = {"Title": title}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = requests.post(
                url,
                data=content.encode("utf-8"),
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Ntfy通知发送成功: {topic}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.text else {}
            }
        
        except requests.RequestException as e:
            logger.error(f"Ntfy通知发送失败: {str(e)}")
            raise Exception(f"Ntfy发送失败: {str(e)}")
