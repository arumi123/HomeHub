"""
ログ機能

アプリケーション全体で使用するログ機能
"""

import logging
import sys
from typing import Optional

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    ロガーを取得
    
    Args:
        name: ロガー名
        level: ログレベル
        
    Returns:
        logging.Logger: ロガーインスタンス
    """
    logger = logging.getLogger(name)
    
    # ログレベルが設定されていない場合はINFOに設定
    if level is None:
        level = "INFO"
    
    logger.setLevel(getattr(logging, level.upper()))
    
    # ハンドラーが既に設定されている場合は追加しない
    if not logger.handlers:
        # コンソールハンドラーを作成
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))
        
        # フォーマッターを作成
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # ハンドラーをロガーに追加
        logger.addHandler(handler)
    
    return logger 