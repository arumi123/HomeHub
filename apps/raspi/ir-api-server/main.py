"""
赤外線操作APIサーバーのエントリーポイント

HomeKitアプリから接続できる赤外線操作APIサーバー
"""

import uvicorn
from fastapi import FastAPI
from api.routes import devices, ir, health
from core.device_manager import DeviceManager
from core.state_manager import StateManager
from devices.ir_system import IRSystem
from config.settings import get_settings

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="IR Control API",
    description="赤外線制御APIサーバー",
    version="1.0.0"
)

# 設定の取得
settings = get_settings()

# 依存関係の初期化
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化"""
    # IRシステムの初期化
    ir_system = IRSystem(gpio_pin=settings.ir_gpio_pin)
    
    # 状態管理の初期化
    state_manager = StateManager(settings.state_file_path)
    
    # デバイス管理の初期化
    device_manager = DeviceManager(state_manager, ir_system)
    
    # 依存関係をアプリケーションコンテキストに保存
    app.state.device_manager = device_manager
    app.state.state_manager = state_manager
    app.state.ir_system = ir_system

# ルーターの登録
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(ir.router, prefix="/ir", tags=["ir"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 