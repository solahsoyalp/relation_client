"""
ユーザーリソースモジュール

このモジュールは、Re:lation APIのユーザーに関連するリソースクラスを提供します。
"""
from typing import List, Dict, Optional, Any, Iterator

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

    def iter_all(self, per_page: Optional[int] = None) -> Iterator[User]:
        """全ページのユーザーを透過的に取得

        ページングを意識せずに、すべてのユーザーを順番に列挙する
        ジェネレータです。内部で ``list`` を ``page=1`` から呼び出し、
        各ページの ``User`` を逐次 yield します。取得件数が
        ``per_page`` 未満（または0件）になったページを最終ページとみなして
        停止します。

        Args:
            per_page: 1ページに表示する件数（デフォルト30, 最大100）

        Yields:
            User: ユーザーオブジェクト
        """
        # per_page 未指定時はAPIデフォルト件数を停止判定に用いる
        page_size = per_page if per_page is not None else 30
        # 無限ループに対する安全弁（通常運用では到達しない十分大きな上限）
        max_pages = 1000
        for page in range(1, max_pages + 1):
            users = self.list(per_page=per_page, page=page)
            for user in users:
                yield user
            if len(users) < page_size:
                break 