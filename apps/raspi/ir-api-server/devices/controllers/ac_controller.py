"""
エアコン制御クラス

既存のdevicedriver.pyのPanasonicACクラスを参考にしたエアコン制御
"""

from typing import Dict, Any, Optional
from .base_controller import BaseDeviceController
from utils.logger import get_logger

logger = get_logger(__name__)

class ACController(BaseDeviceController):
    """エアコン制御クラス"""
    
    def __init__(self, device_config: Dict[str, Any], ir_system):
        super().__init__(device_config, ir_system)
        self.current_temperature = 25
        self.target_temperature = 25
        self.current_mode = "auto"  # auto, cool, heat, fan
        self.current_power = False
        self.current_fan_speed = "auto"
        
        # デバイス固有の設定
        self.min_temperature = device_config.get("min_temperature", 16)
        self.max_temperature = device_config.get("max_temperature", 30)
        self.ir_codes = device_config.get("ir_codes", {})
    
    async def get_status(self) -> Dict[str, Any]:
        """
        エアコンの現在の状態を取得
        
        Returns:
            Dict[str, Any]: エアコンの状態
        """
        return {
            "current_temperature": self.current_temperature,
            "target_temperature": self.target_temperature,
            "mode": self.current_mode,
            "power": self.current_power,
            "fan_speed": self.current_fan_speed
        }
    
    async def set_status(self, status: Dict[str, Any]) -> bool:
        """
        エアコンの状態を設定
        
        Args:
            status: 設定する状態
            
        Returns:
            bool: 設定成功時True
        """
        try:
            # 電源の設定
            if "power" in status:
                if status["power"]:
                    await self.turn_on()
                else:
                    await self.turn_off()
            
            # モードの設定
            if "mode" in status:
                await self.set_mode(status["mode"])
            
            # 温度の設定
            if "target_temperature" in status:
                await self.set_temperature(status["target_temperature"])
            
            # ファン速度の設定
            if "fan_speed" in status:
                await self.set_fan_speed(status["fan_speed"])
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting AC status: {e}")
            return False
    
    async def turn_on(self) -> bool:
        """
        エアコンをオンにする
        
        Returns:
            bool: 成功時True
        """
        try:
            code = self.ir_codes.get("power_on", "ac:power_on")
            success = await self.send_ir_code(code)
            if success:
                self.current_power = True
                logger.info("AC turned on")
            return success
        except Exception as e:
            logger.error(f"Error turning on AC: {e}")
            return False
    
    async def turn_off(self) -> bool:
        """
        エアコンをオフにする
        
        Returns:
            bool: 成功時True
        """
        try:
            code = self.ir_codes.get("power_off", "ac:power_off")
            success = await self.send_ir_code(code)
            if success:
                self.current_power = False
                logger.info("AC turned off")
            return success
        except Exception as e:
            logger.error(f"Error turning off AC: {e}")
            return False
    
    async def set_mode(self, mode: str) -> bool:
        """
        エアコンモードを設定
        
        Args:
            mode: モード (auto, cool, heat, fan)
            
        Returns:
            bool: 成功時True
        """
        try:
            if mode not in ["auto", "cool", "heat", "fan"]:
                raise ValueError("Invalid mode. Must be auto, cool, heat, or fan")
            
            # 現在のモードから目標モードまで段階的に変更
            mode_sequence = ["auto", "cool", "heat", "fan"]
            current_index = mode_sequence.index(self.current_mode)
            target_index = mode_sequence.index(mode)
            
            while current_index != target_index:
                # 次のモードに進む
                current_index = (current_index + 1) % len(mode_sequence)
                next_mode = mode_sequence[current_index]
                
                code = self.ir_codes.get(f"mode_{next_mode}", f"ac:mode_{next_mode}")
                success = await self.send_ir_code(code)
                if not success:
                    return False
                
                self.current_mode = next_mode
            
            logger.info(f"AC mode set to {mode}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting AC mode: {e}")
            return False
    
    async def set_temperature(self, temperature: int) -> bool:
        """
        エアコンの温度を設定
        
        Args:
            temperature: 設定温度 (16-30)
            
        Returns:
            bool: 成功時True
        """
        try:
            if not (self.min_temperature <= temperature <= self.max_temperature):
                raise ValueError(f"Temperature must be between {self.min_temperature} and {self.max_temperature}")
            
            # 現在の温度から目標温度まで段階的に調整
            while self.target_temperature != temperature:
                if self.target_temperature < temperature:
                    code = self.ir_codes.get("temp_up", "ac:temp_up")
                    self.target_temperature += 1
                else:
                    code = self.ir_codes.get("temp_down", "ac:temp_down")
                    self.target_temperature -= 1
                
                success = await self.send_ir_code(code)
                if not success:
                    return False
            
            logger.info(f"AC temperature set to {temperature}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting AC temperature: {e}")
            return False
    
    async def set_fan_speed(self, fan_speed: str) -> bool:
        """
        ファン速度を設定
        
        Args:
            fan_speed: ファン速度 (auto, low, medium, high)
            
        Returns:
            bool: 成功時True
        """
        try:
            if fan_speed not in ["auto", "low", "medium", "high"]:
                raise ValueError("Invalid fan speed. Must be auto, low, medium, or high")
            
            code = self.ir_codes.get(f"fan_{fan_speed}", f"ac:fan_{fan_speed}")
            success = await self.send_ir_code(code)
            if success:
                self.current_fan_speed = fan_speed
                logger.info(f"AC fan speed set to {fan_speed}")
            return success
            
        except Exception as e:
            logger.error(f"Error setting AC fan speed: {e}")
            return False
    
    async def set_current_temperature(self, temperature: float) -> bool:
        """
        現在の室温を設定（センサーからの値）
        
        Args:
            temperature: 現在の室温
            
        Returns:
            bool: 成功時True
        """
        self.current_temperature = temperature
        logger.info(f"Current temperature updated to {temperature}")
        return True 