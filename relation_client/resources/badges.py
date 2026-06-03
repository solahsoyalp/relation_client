"""
バッジリソースモジュール

このモジュールは、Re:lation APIのバッジリソースへのアクセスを提供します。
"""
from typing import List, Optional, Iterator

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

    def iter_all(self, customer_group_id: int, per_page: Optional[int] = None) -> Iterator[Badge]:
        """全ページのバッジを透過的に取得

        ページングを意識せずに、すべてのバッジを順番に列挙する
        ジェネレータです。内部で ``list`` を ``page=1`` から呼び出し、
        各ページの ``Badge`` を逐次 yield します。取得件数が
        ``per_page`` 未満（または0件）になったページを最終ページとみなして
        停止します。

        Args:
            customer_group_id: アドレス帳ID
            per_page: 1ページに表示する件数（デフォルト30, 最大100）

        Yields:
            Badge: バッジオブジェクト
        """
        # per_page 未指定時はAPIデフォルト件数を停止判定に用いる
        page_size = per_page if per_page is not None else 30
        # 無限ループに対する安全弁（通常運用では到達しない十分大きな上限）
        max_pages = 1000
        for page in range(1, max_pages + 1):
            badges = self.list(customer_group_id=customer_group_id, per_page=per_page, page=page)
            for badge in badges:
                yield badge
            if len(badges) < page_size:
                break
