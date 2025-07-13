"""
設定管理モジュール
"""

import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # IR設定
    ir_gpio_pin: int = 17
    ir_frequency: float = 38.0
    ir_gap_ms: int = 100
    
    # ファイルパス設定
    state_file_path: str = "data/device_state.json"
    codes_file_path: str = "data/codes"
    
    # サーバー設定
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ログ設定
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# グローバル設定インスタンス
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """設定インスタンスを取得"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 