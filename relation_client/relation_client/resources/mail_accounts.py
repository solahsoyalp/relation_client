"""
送信メール設定リソースモジュール

このモジュールは、Re:lation APIの送信メール設定リソースへのアクセスを提供します。
"""
from typing import List, Dict, Any, Optional

from ..models import MailAccount


class MailAccountResource:
    """送信メール設定リソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def list(self, message_box_id: int, per_page: Optional[int] = None, page: Optional[int] = None) -> List[MailAccount]:
        """送信メール設定一覧を取得

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト30, 最大100）
            page: ページ番号（デフォルト1）

        Returns:
            List[MailAccount]: 送信メール設定オブジェクトのリスト
        """
        # クエリパラメータの準備
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # APIリクエスト
        response = self.client.get(f'{message_box_id}/mail_accounts', params=params)
        
        # レスポンスを送信メール設定オブジェクトのリストに変換
        if isinstance(response, list):
            return [MailAccount.from_dict(mail_account_data) for mail_account_data in response]
        return [] 