"""
受信箱リソースモジュール

このモジュールは、Re:lation APIの受信箱関連操作を処理するリソースクラスを提供します。
"""
from typing import List, Dict, Any, Optional

from ..models import MessageBox


class MessageBoxResource:
    """受信箱リソースクラス
    
    このクラスは、受信箱関連のAPIエンドポイントへのアクセスを提供します。
    """
    
    def __init__(self, client):
        """初期化
        
        Args:
            client: APIクライアントインスタンス
        """
        self.client = client
        
    def list(self) -> List[MessageBox]:
        """受信箱一覧を取得します。
        
        Returns:
            受信箱リスト
        """
        path = "message_boxes"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをMessageBoxオブジェクトのリストに変換
        return [MessageBox.from_dict(box) for box in response]
    
    def get(self, message_box_id: int) -> MessageBox:
        """受信箱を取得します。
        
        Args:
            message_box_id: 受信箱ID
            
        Returns:
            受信箱情報
        """
        path = f"message_boxes/{message_box_id}"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをMessageBoxオブジェクトに変換
        return MessageBox.from_dict(response) 