"""
デバイス操作APIエンドポイント

デバイスの登録、取得、操作を行うAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

from core.device_manager import DeviceManager
from api.dependencies import get_device_manager

router = APIRouter()

# リクエストモデル
class DeviceRegistration(BaseModel):
    device_type: str
    device_config: Dict[str, Any]

class DeviceCommand(BaseModel):
    type: str  # set_status, get_status, send_ir_code
    status: Dict[str, Any] = {}
    code: str = ""

class DeviceStatusUpdate(BaseModel):
    status: Dict[str, Any]

# レスポンスモデル
class DeviceResponse(BaseModel):
    success: bool
    message: str = ""
    data: Dict[str, Any] = {}

@router.post("/register/{device_id}")
async def register_device(
    device_id: str,
    registration: DeviceRegistration,
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    デバイスを登録
    
    Args:
        device_id: デバイスID
        registration: デバイス登録情報
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: 登録結果
    """
    try:
        success = await device_manager.register_device(
            device_id=device_id,
            device_type=registration.device_type,
            device_config=registration.device_config
        )
        
        if success:
            return DeviceResponse(
                success=True,
                message=f"Device {device_id} registered successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to register device {device_id}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error registering device: {str(e)}"
        )

@router.get("/{device_id}/status")
async def get_device_status(
    device_id: str,
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    デバイスの状態を取得
    
    Args:
        device_id: デバイスID
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: デバイス状態
    """
    try:
        status = await device_manager.get_device_status(device_id)
        
        if status is not None:
            return DeviceResponse(
                success=True,
                data={"status": status}
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Device {device_id} not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting device status: {str(e)}"
        )

@router.put("/{device_id}/status")
async def set_device_status(
    device_id: str,
    status_update: DeviceStatusUpdate,
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    デバイスの状態を設定
    
    Args:
        device_id: デバイスID
        status_update: 状態更新情報
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: 設定結果
    """
    try:
        success = await device_manager.set_device_status(
            device_id=device_id,
            status=status_update.status
        )
        
        if success:
            return DeviceResponse(
                success=True,
                message=f"Device {device_id} status updated successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to update device {device_id} status"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error setting device status: {str(e)}"
        )

@router.post("/{device_id}/command")
async def execute_device_command(
    device_id: str,
    command: DeviceCommand,
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    デバイスコマンドを実行
    
    Args:
        device_id: デバイスID
        command: 実行するコマンド
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: 実行結果
    """
    try:
        command_dict = {
            "type": command.type,
            "status": command.status,
            "code": command.code
        }
        
        result = await device_manager.execute_command(
            device_id=device_id,
            command=command_dict
        )
        
        if result.get("success", False):
            return DeviceResponse(
                success=True,
                data=result
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Command execution failed")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing device command: {str(e)}"
        )

@router.get("/")
async def get_all_devices(
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    全デバイスの情報を取得
    
    Args:
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: 全デバイス情報
    """
    try:
        devices = await device_manager.get_all_devices()
        
        return DeviceResponse(
            success=True,
            data={"devices": devices}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting all devices: {str(e)}"
        )

@router.delete("/{device_id}")
async def remove_device(
    device_id: str,
    device_manager: DeviceManager = Depends(get_device_manager)
) -> DeviceResponse:
    """
    デバイスを削除
    
    Args:
        device_id: デバイスID
        device_manager: デバイス管理クラス
        
    Returns:
        DeviceResponse: 削除結果
    """
    try:
        success = await device_manager.remove_device(device_id)
        
        if success:
            return DeviceResponse(
                success=True,
                message=f"Device {device_id} removed successfully"
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Device {device_id} not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing device: {str(e)}"
        ) 