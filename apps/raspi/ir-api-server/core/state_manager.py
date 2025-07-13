"""
状態管理クラス

既存のdevicedriver.pyの状態管理機能を参考にした状態管理
"""

import json
import os
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class StateManager:
    """状態管理クラス"""
    
    def __init__(self, state_file_path: str = "data/device_state.json"):
        self.state_file_path = state_file_path
        self._ensure_state_file()
    
    def _ensure_state_file(self):
        """状態ファイルの存在確認と作成"""
        os.makedirs(os.path.dirname(self.state_file_path), exist_ok=True)
        
        if not os.path.exists(self.state_file_path):
            # 初期状態ファイルを作成
            initial_state = {
                "devices": {},
                "last_updated": None
            }
            self._write_state(initial_state)
    
    def _read_state(self) -> Dict[str, Any]:
        """
        状態ファイルを読み込み
        
        Returns:
            Dict[str, Any]: 状態データ
        """
        try:
            with open(self.state_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Failed to load state from {self.state_file_path}: {e}")
            return {"devices": {}, "last_updated": None}
    
    def _write_state(self, state: Dict[str, Any]):
        """
        状態ファイルに書き込み
        
        Args:
            state: 書き込む状態データ
        """
        try:
            with open(self.state_file_path, 'w', encoding='utf-8') as file:
                json.dump(state, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Failed to write state to {self.state_file_path}: {e}")
    
    async def get_device_state(self, device_id: str) -> Optional[Dict[str, Any]]:
        """
        デバイスの状態を取得
        
        Args:
            device_id: デバイスID
            
        Returns:
            Optional[Dict[str, Any]]: デバイスの状態
        """
        state = self._read_state()
        return state.get("devices", {}).get(device_id)
    
    async def update_device_state(
        self,
        device_id: str,
        new_state: Dict[str, Any]
    ) -> bool:
        """
        デバイスの状態を更新
        
        Args:
            device_id: デバイスID
            new_state: 新しい状態
            
        Returns:
            bool: 更新成功時True
        """
        try:
            state = self._read_state()
            
            # デバイス状態を更新
            if "devices" not in state:
                state["devices"] = {}
            
            state["devices"][device_id] = new_state
            state["last_updated"] = self._get_current_timestamp()
            
            # 状態を保存
            self._write_state(state)
            
            logger.info(f"Device state updated for {device_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating device state for {device_id}: {e}")
            return False
    
    async def remove_device_state(self, device_id: str) -> bool:
        """
        デバイスの状態を削除
        
        Args:
            device_id: デバイスID
            
        Returns:
            bool: 削除成功時True
        """
        try:
            state = self._read_state()
            
            if "devices" in state and device_id in state["devices"]:
                del state["devices"][device_id]
                state["last_updated"] = self._get_current_timestamp()
                
                self._write_state(state)
                logger.info(f"Device state removed for {device_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error removing device state for {device_id}: {e}")
            return False
    
    async def get_all_device_states(self) -> Dict[str, Any]:
        """
        全デバイスの状態を取得
        
        Returns:
            Dict[str, Any]: 全デバイスの状態
        """
        state = self._read_state()
        return state.get("devices", {})
    
    async def clear_all_states(self) -> bool:
        """
        全デバイスの状態をクリア
        
        Returns:
            bool: クリア成功時True
        """
        try:
            initial_state = {
                "devices": {},
                "last_updated": self._get_current_timestamp()
            }
            self._write_state(initial_state)
            logger.info("All device states cleared")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing all states: {e}")
            return False
    
    def _get_current_timestamp(self) -> str:
        """
        現在のタイムスタンプを取得
        
        Returns:
            str: タイムスタンプ文字列
        """
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_state_file_path(self) -> str:
        """
        状態ファイルのパスを取得
        
        Returns:
            str: 状態ファイルのパス
        """
        return self.state_file_path 