"""
API依存性注入

FastAPIの依存性注入を管理するモジュール
"""

from fastapi import Request
from core.device_manager import DeviceManager
from core.state_manager import StateManager
from devices.ir_system import IRSystem

def get_device_manager(request: Request) -> DeviceManager:
    """
    デバイス管理クラスを取得
    
    Args:
        request: FastAPIリクエスト
        
    Returns:
        DeviceManager: デバイス管理クラス
    """
    return request.app.state.device_manager

def get_state_manager(request: Request) -> StateManager:
    """
    状態管理クラスを取得
    
    Args:
        request: FastAPIリクエスト
        
    Returns:
        StateManager: 状態管理クラス
    """
    return request.app.state.state_manager

def get_ir_system(request: Request) -> IRSystem:
    """
    赤外線システムを取得
    
    Args:
        request: FastAPIリクエスト
        
    Returns:
        IRSystem: 赤外線システム
    """
    return request.app.state.ir_system 