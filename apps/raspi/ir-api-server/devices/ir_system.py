"""
赤外線送受信システム

既存のirrp.pyを活用した赤外線制御システム
"""

import asyncio
import subprocess
import os
from typing import List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class IRSystem:
    """赤外線送受信システム"""
    
    def __init__(self, gpio_pin: int = 17, frequency: float = 38.0):
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        self.codes_file = "data/codes"
        
        # codesファイルのディレクトリを作成
        os.makedirs(os.path.dirname(self.codes_file), exist_ok=True)
    
    async def send_code(self, code: str) -> bool:
        """
        赤外線コードを送信
        
        Args:
            code: 送信するコード名
            
        Returns:
            bool: 送信成功時True
        """
        try:
            # 既存のirrp.pyを使用してコードを送信
            cmd = [
                "python3", "irrp.py",
                "-p",  # playback mode
                "-g", str(self.gpio_pin),
                "-f", self.codes_file,
                "--freq", str(self.frequency),
                code
            ]
            
            # 非同期でコマンドを実行
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"IR code '{code}' sent successfully")
                return True
            else:
                logger.error(f"Failed to send IR code '{code}': {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending IR code '{code}': {e}")
            return False
    
    async def record_code(self, code_name: str) -> bool:
        """
        赤外線コードを記録
        
        Args:
            code_name: 記録するコード名
            
        Returns:
            bool: 記録成功時True
        """
        try:
            # 既存のirrp.pyを使用してコードを記録
            cmd = [
                "python3", "irrp.py",
                "-r",  # record mode
                "-g", "4",  # GPIO 4 for receiver
                "-f", self.codes_file,
                code_name
            ]
            
            # 非同期でコマンドを実行
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"IR code '{code_name}' recorded successfully")
                return True
            else:
                logger.error(f"Failed to record IR code '{code_name}': {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Error recording IR code '{code_name}': {e}")
            return False
    
    def get_available_codes(self) -> List[str]:
        """
        利用可能なコード一覧を取得
        
        Returns:
            List[str]: コード名のリスト
        """
        try:
            if not os.path.exists(self.codes_file):
                return []
            
            with open(self.codes_file, 'r') as f:
                # 既存のcodesファイルの形式に応じて解析
                # 実際の形式に合わせて調整が必要
                codes = []
                for line in f:
                    if line.strip():
                        codes.append(line.strip())
                return codes
        except Exception as e:
            logger.error(f"Error reading available codes: {e}")
            return [] 