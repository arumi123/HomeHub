"""
デバイス管理クラス

デバイスの登録、取得、操作を管理するクラス
"""

from typing import Dict, Any, Optional, List
from devices.ir_system import IRSystem
from devices.controllers import DeviceControllerFactory, BaseDeviceController
from core.state_manager import StateManager
from utils.logger import get_logger

logger = get_logger(__name__)

class DeviceManager:
    """デバイス管理クラス"""
    
    def __init__(self, state_manager: StateManager, ir_system: IRSystem):
        self.state_manager = state_manager
        self.ir_system = ir_system
        self.devices: Dict[str, BaseDeviceController] = {}
        self.device_configs: Dict[str, Dict[str, Any]] = {}
    
    async def register_device(
        self,
        device_id: str,
        device_type: str,
        device_config: Dict[str, Any]
    ) -> bool:
        """
        デバイスを登録
        
        Args:
            device_id: デバイスID
            device_type: デバイスタイプ
            device_config: デバイス設定
            
        Returns:
            bool: 登録成功時True
        """
        try:
            # デバイス制御クラスを作成
            controller = DeviceControllerFactory.create_controller(
                device_type=device_type,
                device_config=device_config,
                ir_system=self.ir_system
            )
            
            # デバイスを登録
            self.devices[device_id] = controller
            self.device_configs[device_id] = device_config
            
            logger.info(f"Device {device_id} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error registering device {device_id}: {e}")
            return False
    
    async def get_device(self, device_id: str) -> Optional[BaseDeviceController]:
        """
        デバイスを取得
        
        Args:
            device_id: デバイスID
            
        Returns:
            Optional[BaseDeviceController]: デバイス制御クラス
        """
        return self.devices.get(device_id)
    
    async def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """
        デバイスの状態を取得
        
        Args:
            device_id: デバイスID
            
        Returns:
            Optional[Dict[str, Any]]: デバイスの状態
        """
        device = await self.get_device(device_id)
        if device:
            return await device.get_status()
        return None
    
    async def set_device_status(
        self,
        device_id: str,
        status: Dict[str, Any]
    ) -> bool:
        """
        デバイスの状態を設定
        
        Args:
            device_id: デバイスID
            status: 設定する状態
            
        Returns:
            bool: 設定成功時True
        """
        device = await self.get_device(device_id)
        if device:
            success = await device.set_status(status)
            if success:
                # 状態を永続化
                await self.state_manager.update_device_state(device_id, status)
            return success
        return False
    
    async def execute_command(
        self,
        device_id: str,
        command: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        デバイスコマンドを実行
        
        Args:
            device_id: デバイスID
            command: 実行するコマンド
            
        Returns:
            Dict[str, Any]: 実行結果
        """
        device = await self.get_device(device_id)
        if not device:
            return {
                "success": False,
                "error": f"Device {device_id} not found"
            }
        
        try:
            # コマンドの種類に応じて処理
            command_type = command.get("type")
            
            if command_type == "set_status":
                success = await device.set_status(command.get("status", {}))
                return {"success": success}
            
            elif command_type == "get_status":
                status = await device.get_status()
                return {"success": True, "status": status}
            
            elif command_type == "send_ir_code":
                code = command.get("code")
                if code:
                    success = await device.send_ir_code(code)
                    return {"success": success}
                else:
                    return {"success": False, "error": "IR code not specified"}
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown command type: {command_type}"
                }
                
        except Exception as e:
            logger.error(f"Error executing command on device {device_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_all_devices(self) -> List[Dict[str, Any]]:
        """
        全デバイスの情報を取得
        
        Returns:
            List[Dict[str, Any]]: デバイス情報のリスト
        """
        devices_info = []
        for device_id, device in self.devices.items():
            device_info = device.get_device_info()
            device_info["status"] = await device.get_status()
            devices_info.append(device_info)
        return devices_info
    
    async def remove_device(self, device_id: str) -> bool:
        """
        デバイスを削除
        
        Args:
            device_id: デバイスID
            
        Returns:
            bool: 削除成功時True
        """
        if device_id in self.devices:
            del self.devices[device_id]
            del self.device_configs[device_id]
            await self.state_manager.remove_device_state(device_id)
            logger.info(f"Device {device_id} removed successfully")
            return True
        return False 