from fastapi import FastAPI

app = FastAPI(
    title="HomeHub API",
    description="スマートホーム向けの賢いリモコンシステムのAPI",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"} 