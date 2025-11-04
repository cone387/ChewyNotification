import requests
import logging
from .base_service import BaseNotificationService

logger = logging.getLogger(__name__)


class BarkService(BaseNotificationService):
    """Bark 通知服务"""
    
    def __init__(self, config):
        """
        初始化 Bark 服务
        
        配置示例:
        {
            "server_url": "https://api.day.app"
        }
        """
        super().__init__(config)
        self.server_url = config.get("server_url", "https://api.day.app")
    
    def _send_implementation(self, payload):
        """
        Bark 的具体发送实现
        
        支持所有 Bark 参数：
        - 基础：device_key, title, body, subtitle
        - 提醒：level, badge, sound, call
        - 交互：url, copy, auto_copy
        - 展示：icon, group
        - 存储：is_archive
        
        Args:
            params: 参数字典
            
        Returns:
            dict: 发送结果
        """
        url = f"{self.server_url}/push"
        
        # 构建 Bark API payload
        bark_payload = {
            "device_key": payload["target"],
            "title": payload["title"],
            "body": payload["content"],
        }
        
        # 映射参数到 Bark API 格式
        param_mapping = {
            "subtitle": "subtitle",
            "level": "level",
            "badge": "badge",
            "sound": "sound",
            "icon": "icon",
            "group": "group",
            "url": "url",
            "copy": "copy",
            "auto_copy": "autoCopy",
            "call": "call",
            "is_archive": "isArchive",
        }
        
        # 添加可选参数
        for param_key, bark_key in param_mapping.items():
            if param_key in payload:
                bark_payload[bark_key] = payload[param_key]
        
        try:
            response = requests.post(
                url, 
                json=bark_payload,
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=10
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.text else {}
            }
        
        except requests.RequestException as e:
            raise Exception(f"Bark发送失败: {str(e)}")
