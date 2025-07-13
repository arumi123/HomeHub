"""
デバイス制御パッケージ

既存のdevicedriver.pyのDevicefactoryを参考にしたデバイス制御ファクトリー
"""

from typing import Dict, Any
from .base_controller import BaseDeviceController
from .light_controller import LightController
from .ac_controller import ACController
from devices.ir_system import IRSystem

class DeviceControllerFactory:
    """デバイス制御ファクトリー"""
    
    @staticmethod
    def create_controller(
        device_type: str,
        device_config: Dict[str, Any],
        ir_system: IRSystem
    ) -> BaseDeviceController:
        """
        デバイス制御クラスを作成
        
        Args:
            device_type: デバイスタイプ
            device_config: デバイス設定
            ir_system: 赤外線システム
            
        Returns:
            BaseDeviceController: デバイス制御クラス
            
        Raises:
            ValueError: サポートされていないデバイスタイプの場合
        """
        if device_type == "light":
            return LightController(device_config, ir_system)
        elif device_type == "ac":
            return ACController(device_config, ir_system)
        else:
            raise ValueError(f"Unsupported device type: {device_type}")

# エクスポート
__all__ = [
    "BaseDeviceController",
    "LightController", 
    "ACController",
    "DeviceControllerFactory"
] 