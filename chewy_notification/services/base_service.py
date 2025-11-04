import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BaseNotificationService(ABC):
    """通知服务基类，以 Bark 的参数为基准"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化通知服务
        
        Args:
            config: 渠道配置
        """
        self.config = config
    
    @abstractmethod
    def _send_implementation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        具体的发送实现（由子类实现）
        
        Args:
            payload: 已处理的参数字典
            
        Returns:
            dict: 发送结果
        """
        pass
    
    def send(
        self,
        target: str,
        title: str,
        content: str,
        # Bark 标准参数
        subtitle: Optional[str] = None,
        level: Optional[str] = None,  # critical/active/timeSensitive/passive
        badge: Optional[int] = None,
        sound: Optional[str] = None,
        icon: Optional[str] = None,
        group: Optional[str] = None,
        url: Optional[str] = None,
        # 高级功能
        copy: Optional[str] = None,
        auto_copy: Optional[str] = None,
        call: Optional[str] = None,
        is_archive: Optional[str] = None,
        # 其他参数
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送通知（统一接口）
        
        Args:
            target: 目标（device_key/topic/email/webhook等）
            title: 通知标题
            content: 通知内容
            subtitle: 副标题
            level: 中断级别（critical/active/timeSensitive/passive）
            badge: 角标数字
            sound: 铃声
            icon: 图标 URL
            group: 分组
            url: 点击跳转 URL
            copy: 复制的内容
            auto_copy: 是否自动复制（"1"）
            call: 是否重复播放铃声（"1"）
            is_archive: 是否保存（"1"）
            **kwargs: 其他扩展参数
            
        Returns:
            dict: 发送结果
        """
        # 构建参数字典
        params = {
            "target": target,
            "title": title,
            "content": content,
        }
        
        # 添加可选参数（只添加非 None 的）
        optional_params = {
            "subtitle": subtitle,
            "level": level,
            "badge": badge,
            "sound": sound,
            "icon": icon,
            "group": group,
            "url": url,
            "copy": copy,
            "auto_copy": auto_copy,
            "call": call,
            "is_archive": is_archive,
        }
        
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value
        
        # 添加额外的 kwargs
        params.update(kwargs)
        
        try:
            # 调用子类的具体实现
            result = self._send_implementation(params)
            logger.info(f"{self.__class__.__name__} 通知发送成功")
            return result
        
        except Exception as e:
            logger.error(f"{self.__class__.__name__} 通知发送失败: {str(e)}")
            raise
