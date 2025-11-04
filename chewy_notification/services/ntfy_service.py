import requests
import logging
from .base_service import BaseNotificationService

logger = logging.getLogger(__name__)


class NtfyService(BaseNotificationService):
    """Ntfy 通知服务"""
    
    def __init__(self, config):
        super().__init__(config)
        self.server_url = config.get("server_url", "https://ntfy.sh")
        self.token = config.get("token")
    
    def _send_implementation(self, payload):
        """
        Ntfy 的具体发送实现
        
        Ntfy 支持部分 Bark 参数：
        - title: 标题
        - content/body: 内容
        - url: 点击跳转
        - icon: 图标
        - priority: 优先级（类似 level）
        
        Args:
            payload: 参数字典
            
        Returns:
            dict: 发送结果
        """
        topic = payload["target"]
        url = f"{self.server_url}/{topic}"
        
        # Ntfy 支持在 Header 中使用 UTF-8，需要手动编码
        headers = {}
        
        # 将标题编码为 UTF-8 字节，然后用 latin-1 解码（HTTP Header 标准）
        title = payload["title"]
        if title:
            title_bytes = title.encode('utf-8')
            headers["Title"] = title_bytes.decode('latin-1')
        
        # 映射可选参数
        if "url" in payload:
            url_bytes = payload["url"].encode('utf-8')
            headers["Click"] = url_bytes.decode('latin-1')
        
        if "icon" in payload:
            icon_bytes = payload["icon"].encode('utf-8')
            headers["Icon"] = icon_bytes.decode('latin-1')
        
        # level 映射到 priority
        if "level" in payload:
            priority_map = {
                "critical": "5",
                "active": "4",
                "timeSensitive": "3",
                "passive": "1",
            }
            headers["Priority"] = priority_map.get(payload["level"], "3")
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            response = requests.post(
                url,
                data=payload["content"].encode("utf-8"),
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.text else {}
            }
        
        except requests.RequestException as e:
            raise Exception(f"Ntfy发送失败: {str(e)}")
