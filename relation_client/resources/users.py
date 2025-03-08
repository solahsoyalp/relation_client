"""
ユーザーリソースモジュール

このモジュールは、Re:lation APIのユーザーに関連するリソースクラスを提供します。
"""
from typing import List, Dict, Optional, Any

from ..models import User


class UserResource:
    """ユーザーリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアント
        """
        self.client = client

    def list(self, per_page: Optional[int] = None, page: Optional[int] = None) -> List[User]:
        """ユーザー一覧を取得

        Args:
            per_page: 1ページに表示する件数（デフォルト30, 最大100）
            page: ページ番号（デフォルト1）

        Returns:
            List[User]: ユーザーオブジェクトのリスト
        """
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page

        response = self.client.get('users', params=params)
        return [User.from_dict(item) for item in response] 