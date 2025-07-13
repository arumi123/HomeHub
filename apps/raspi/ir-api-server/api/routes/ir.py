"""
赤外線操作APIエンドポイント

赤外線コードの送信、記録を行うAPI
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel

from devices.ir_system import IRSystem
from api.dependencies import get_ir_system

router = APIRouter()

# リクエストモデル
class IRSendRequest(BaseModel):
    code: str

class IRRecordRequest(BaseModel):
    code_name: str

# レスポンスモデル
class IRResponse(BaseModel):
    success: bool
    message: str = ""
    data: dict = {}

@router.post("/send")
async def send_ir_code(
    request: IRSendRequest,
    ir_system: IRSystem = Depends(get_ir_system)
) -> IRResponse:
    """
    赤外線コードを送信
    
    Args:
        request: 送信リクエスト
        ir_system: 赤外線システム
        
    Returns:
        IRResponse: 送信結果
    """
    try:
        success = await ir_system.send_code(request.code)
        
        if success:
            return IRResponse(
                success=True,
                message=f"IR code '{request.code}' sent successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to send IR code '{request.code}'"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error sending IR code: {str(e)}"
        )

@router.post("/record")
async def record_ir_code(
    request: IRRecordRequest,
    ir_system: IRSystem = Depends(get_ir_system)
) -> IRResponse:
    """
    赤外線コードを記録
    
    Args:
        request: 記録リクエスト
        ir_system: 赤外線システム
        
    Returns:
        IRResponse: 記録結果
    """
    try:
        success = await ir_system.record_code(request.code_name)
        
        if success:
            return IRResponse(
                success=True,
                message=f"IR code '{request.code_name}' recorded successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to record IR code '{request.code_name}'"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error recording IR code: {str(e)}"
        )

@router.get("/codes")
async def get_available_codes(
    ir_system: IRSystem = Depends(get_ir_system)
) -> IRResponse:
    """
    利用可能な赤外線コード一覧を取得
    
    Args:
        ir_system: 赤外線システム
        
    Returns:
        IRResponse: コード一覧
    """
    try:
        codes = ir_system.get_available_codes()
        
        return IRResponse(
            success=True,
            data={"codes": codes}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting available codes: {str(e)}"
        )

@router.get("/status")
async def get_ir_system_status(
    ir_system: IRSystem = Depends(get_ir_system)
) -> IRResponse:
    """
    赤外線システムの状態を取得
    
    Args:
        ir_system: 赤外線システム
        
    Returns:
        IRResponse: システム状態
    """
    try:
        status = {
            "gpio_pin": ir_system.gpio_pin,
            "frequency": ir_system.frequency,
            "codes_file": ir_system.codes_file,
            "available_codes": ir_system.get_available_codes()
        }
        
        return IRResponse(
            success=True,
            data={"status": status}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting IR system status: {str(e)}"
        ) 