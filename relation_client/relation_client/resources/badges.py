"""
バッジリソースモジュール

このモジュールは、Re:lation APIのバッジリソースへのアクセスを提供します。
"""
from typing import List, Dict, Any, Optional

from ..models import Badge


class BadgeResource:
    """バッジリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def list(self, customer_group_id: int, per_page: Optional[int] = None, page: Optional[int] = None) -> List[Badge]:
        """バッジ一覧を取得

        Args:
            customer_group_id: アドレス帳ID
            per_page: 1ページに表示する件数（デフォルト30, 最大100）
            page: ページ番号（デフォルト1）

        Returns:
            List[Badge]: バッジオブジェクトのリスト
        """
        # クエリパラメータの準備
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # APIリクエスト
        response = self.client.get(f'customer_groups/{customer_group_id}/badges', params=params)
        
        # レスポンスをバッジオブジェクトのリストに変換
        if isinstance(response, list):
            return [Badge.from_dict(badge_data) for badge_data in response]
        return [] 