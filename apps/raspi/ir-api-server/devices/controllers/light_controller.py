"""
照明制御クラス

既存のdevicedriver.pyのRe0207とClRs2クラスを参考にした照明制御
"""

from typing import Dict, Any, Optional
from .base_controller import BaseDeviceController
from utils.logger import get_logger

logger = get_logger(__name__)

class LightController(BaseDeviceController):
    """照明制御クラス"""
    
    def __init__(self, device_config: Dict[str, Any], ir_system):
        super().__init__(device_config, ir_system)
        self.current_brightness = 0
        self.current_mode = "off"
        self.current_color_temp = 0
        
        # デバイス固有の設定
        self.brightness_steps = device_config.get("brightness_steps", 10)
        self.color_temp_steps = device_config.get("color_temp_steps", 5)
        self.ir_codes = device_config.get("ir_codes", {})
    
    async def get_status(self) -> Dict[str, Any]:
        """
        照明の現在の状態を取得
        
        Returns:
            Dict[str, Any]: 照明の状態
        """
        return {
            "brightness": self.current_brightness,
            "mode": self.current_mode,
            "color_temperature": self.current_color_temp,
            "power": self.current_mode != "off"
        }
    
    async def set_status(self, status: Dict[str, Any]) -> bool:
        """
        照明の状態を設定
        
        Args:
            status: 設定する状態
            
        Returns:
            bool: 設定成功時True
        """
        try:
            # 明度の設定
            if "brightness" in status:
                await self.set_brightness(status["brightness"])
            
            # 電源の設定
            if "power" in status:
                if status["power"]:
                    await self.turn_on()
                else:
                    await self.turn_off()
            
            # 色温度の設定
            if "color_temperature" in status:
                await self.set_color_temperature(status["color_temperature"])
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting light status: {e}")
            return False
    
    async def set_brightness(self, brightness: int) -> bool:
        """
        明度を設定
        
        Args:
            brightness: 明度 (0-100)
            
        Returns:
            bool: 設定成功時True
        """
        try:
            # 明度の範囲チェック
            if not (0 <= brightness <= 100):
                raise ValueError("Brightness must be between 0 and 100")
            
            # 既存のdevicedriver.pyのロジックを参考に実装
            if brightness == 0:
                await self.turn_off()
            elif 1 <= brightness <= 9:
                await self.set_night_mode()
            else:
                await self.turn_on()
                await self._adjust_brightness(brightness)
            
            self.current_brightness = brightness
            return True
            
        except Exception as e:
            logger.error(f"Error setting brightness: {e}")
            return False
    
    async def turn_on(self) -> bool:
        """
        照明をオンにする
        
        Returns:
            bool: 成功時True
        """
        try:
            code = self.ir_codes.get("on", "light:on")
            success = await self.send_ir_code(code)
            if success:
                self.current_mode = "on"
                logger.info("Light turned on")
            return success
        except Exception as e:
            logger.error(f"Error turning on light: {e}")
            return False
    
    async def turn_off(self) -> bool:
        """
        照明をオフにする
        
        Returns:
            bool: 成功時True
        """
        try:
            code = self.ir_codes.get("off", "light:off")
            success = await self.send_ir_code(code)
            if success:
                self.current_mode = "off"
                self.current_brightness = 0
                logger.info("Light turned off")
            return success
        except Exception as e:
            logger.error(f"Error turning off light: {e}")
            return False
    
    async def set_night_mode(self) -> bool:
        """
        常夜灯モードに設定
        
        Returns:
            bool: 成功時True
        """
        try:
            code = self.ir_codes.get("night", "light:night")
            success = await self.send_ir_code(code)
            if success:
                self.current_mode = "night"
                logger.info("Light set to night mode")
            return success
        except Exception as e:
            logger.error(f"Error setting night mode: {e}")
            return False
    
    async def set_color_temperature(self, color_temp: int) -> bool:
        """
        色温度を設定
        
        Args:
            color_temp: 色温度 (0-5)
            
        Returns:
            bool: 成功時True
        """
        try:
            if not (0 <= color_temp <= 5):
                raise ValueError("Color temperature must be between 0 and 5")
            
            # 色温度の段階的な調整
            current_temp = self.current_color_temp
            while current_temp != color_temp:
                if current_temp < color_temp:
                    code = self.ir_codes.get("color_temp_up", "light:color_temp_up")
                    current_temp += 1
                else:
                    code = self.ir_codes.get("color_temp_down", "light:color_temp_down")
                    current_temp -= 1
                
                success = await self.send_ir_code(code)
                if not success:
                    return False
            
            self.current_color_temp = color_temp
            logger.info(f"Color temperature set to {color_temp}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting color temperature: {e}")
            return False
    
    async def _adjust_brightness(self, target_brightness: int) -> bool:
        """
        明度を段階的に調整
        
        Args:
            target_brightness: 目標明度
            
        Returns:
            bool: 成功時True
        """
        try:
            current_brightness = self.current_brightness
            brightness_step = target_brightness // 10
            
            while current_brightness != target_brightness:
                if current_brightness < target_brightness:
                    code = self.ir_codes.get("brightness_up", "light:brightness_up")
                    current_brightness += 10
                else:
                    code = self.ir_codes.get("brightness_down", "light:brightness_down")
                    current_brightness -= 10
                
                success = await self.send_ir_code(code)
                if not success:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error adjusting brightness: {e}")
            return False 