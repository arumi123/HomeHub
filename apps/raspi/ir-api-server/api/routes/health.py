"""
ヘルスチェックAPIエンドポイント

システムの健全性を確認するAPI
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.device_manager import DeviceManager
from devices.ir_system import IRSystem
from api.dependencies import get_device_manager, get_ir_system

router = APIRouter()

# レスポンスモデル
class HealthResponse(BaseModel):
    status: str
    message: str = ""
    details: dict = {}

@router.get("/")
async def health_check() -> HealthResponse:
    """
    基本的なヘルスチェック
    
    Returns:
        HealthResponse: ヘルスチェック結果
    """
    return HealthResponse(
        status="healthy",
        message="IR Control API is running"
    )

@router.get("/detailed")
async def detailed_health_check(
    device_manager: DeviceManager = Depends(get_device_manager),
    ir_system: IRSystem = Depends(get_ir_system)
) -> HealthResponse:
    """
    詳細なヘルスチェック
    
    Args:
        device_manager: デバイス管理クラス
        ir_system: 赤外線システム
        
    Returns:
        HealthResponse: 詳細なヘルスチェック結果
    """
    try:
        # 各コンポーネントの状態を確認
        details = {
            "ir_system": {
                "gpio_pin": ir_system.gpio_pin,
                "frequency": ir_system.frequency,
                "codes_file": ir_system.codes_file
            },
            "device_manager": {
                "registered_devices": len(device_manager.devices)
            }
        }
        
        # 利用可能な赤外線コードを確認
        available_codes = ir_system.get_available_codes()
        details["ir_system"]["available_codes_count"] = len(available_codes)
        
        return HealthResponse(
            status="healthy",
            message="All components are functioning normally",
            details=details
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Health check failed: {str(e)}",
            details={"error": str(e)}
        )

@router.get("/ready")
async def readiness_check(
    device_manager: DeviceManager = Depends(get_device_manager),
    ir_system: IRSystem = Depends(get_ir_system)
) -> HealthResponse:
    """
    準備完了チェック
    
    Args:
        device_manager: デバイス管理クラス
        ir_system: 赤外線システム
        
    Returns:
        HealthResponse: 準備完了チェック結果
    """
    try:
        # 必要なコンポーネントが利用可能かチェック
        checks = {
            "ir_system_available": True,
            "device_manager_available": True,
            "codes_file_accessible": True
        }
        
        # 赤外線システムの状態確認
        try:
            ir_system.get_available_codes()
        except Exception:
            checks["ir_system_available"] = False
            checks["codes_file_accessible"] = False
        
        # 全体的な準備状態を判定
        all_ready = all(checks.values())
        
        return HealthResponse(
            status="ready" if all_ready else "not_ready",
            message="System is ready to handle requests" if all_ready else "System is not ready",
            details=checks
        )
        
    except Exception as e:
        return HealthResponse(
            status="not_ready",
            message=f"Readiness check failed: {str(e)}",
            details={"error": str(e)}
        ) 