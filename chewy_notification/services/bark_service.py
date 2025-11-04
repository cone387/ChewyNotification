import requests
import logging

logger = logging.getLogger(__name__)


class BarkService:
    """Bark 通知服务"""
    
    def __init__(self, config):
        """
        初始化 Bark 服务
        
        配置示例:
        {
            "server_url": "https://api.day.app"
        }
        """
        self.server_url = config.get("server_url", "https://api.day.app")
    
    def send(self, device_key, title, content):
        """
        发送 Bark 通知
        
        Args:
            device_key: Bark 设备 key
            title: 通知标题
            content: 通知内容
        
        Returns:
            dict: 发送结果
        """
        url = f"{self.server_url}/{device_key}/{title}/{content}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Bark通知发送成功: {device_key}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.text else {}
            }
        
        except requests.RequestException as e:
            logger.error(f"Bark通知发送失败: {str(e)}")
            raise Exception(f"Bark发送失败: {str(e)}")
