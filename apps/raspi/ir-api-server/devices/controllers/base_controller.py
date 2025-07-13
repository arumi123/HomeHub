"""
デバイス制御の基底クラス

既存のdevicedriver.pyのDeviceクラスを参考にした基底クラス
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from devices.ir_system import IRSystem
from utils.logger import get_logger

logger = get_logger(__name__)

class BaseDeviceController(ABC):
    """デバイス制御の基底クラス"""
    
    def __init__(self, device_config: Dict[str, Any], ir_system: IRSystem):
        self.config = device_config
        self.ir_system = ir_system
        self.device_id = device_config.get("device_id")
        self.device_type = device_config.get("device_type")
        self.device_name = device_config.get("device_name", "Unknown Device")
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        デバイスの現在の状態を取得
        
        Returns:
            Dict[str, Any]: デバイスの状態
        """
        pass
    
    @abstractmethod
    async def set_status(self, status: Dict[str, Any]) -> bool:
        """
        デバイスの状態を設定
        
        Args:
            status: 設定する状態
            
        Returns:
            bool: 設定成功時True
        """
        pass
    
    async def send_ir_code(self, code: str) -> bool:
        """
        赤外線コードを送信
        
        Args:
            code: 送信するコード名
            
        Returns:
            bool: 送信成功時True
        """
        return await self.ir_system.send_code(code)
    
    def get_device_info(self) -> Dict[str, Any]:
        """
        デバイス情報を取得
        
        Returns:
            Dict[str, Any]: デバイス情報
        """
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_name": self.device_name,
            "config": self.config
        }
    
    def validate_status(self, status: Dict[str, Any]) -> bool:
        """
        状態の妥当性を検証
        
        Args:
            status: 検証する状態
            
        Returns:
            bool: 妥当な場合True
        """
        # サブクラスで実装
        return True 