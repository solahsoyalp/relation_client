"""
チャットリソースモジュール

このモジュールは、Re:lation APIのチャット関連操作を処理するリソースクラスを提供します。
"""
from typing import Dict, Any, Optional

from ..models import ChatPlus, Yahoo, RMesse, Line


class ChatResource:
    """チャットリソースクラス
    
    このクラスは、チャット関連のAPIエンドポイントへのアクセスを提供します。
    """
    
    def __init__(self, client):
        """初期化
        
        Args:
            client: APIクライアントインスタンス
        """
        self.client = client
        
    def get_chatplus(self, message_box_id: int, ticket_id: int, message_id: int) -> ChatPlus:
        """ChatPlus情報を取得します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            message_id: メッセージID
            
        Returns:
            ChatPlus情報
        """
        path = f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/chatplus"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをChatPlusオブジェクトに変換
        return ChatPlus.from_dict(response)
    
    def get_yahoo(self, message_box_id: int, ticket_id: int, message_id: int) -> Yahoo:
        """Yahoo!ショッピング情報を取得します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            message_id: メッセージID
            
        Returns:
            Yahoo!ショッピング情報
        """
        path = f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/yahoo"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをYahooオブジェクトに変換
        return Yahoo.from_dict(response)
    
    def get_r_messe(self, message_box_id: int, ticket_id: int, message_id: int) -> RMesse:
        """R-Messe情報を取得します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            message_id: メッセージID
            
        Returns:
            R-Messe情報
        """
        path = f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/r_messe"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをRMesseオブジェクトに変換
        return RMesse.from_dict(response)
    
    def get_line(self, message_box_id: int, ticket_id: int, message_id: int) -> Line:
        """LINE情報を取得します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            message_id: メッセージID
            
        Returns:
            LINE情報
        """
        path = f"{message_box_id}/tickets/{ticket_id}/messages/{message_id}/line"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをLineオブジェクトに変換
        return Line.from_dict(response) 