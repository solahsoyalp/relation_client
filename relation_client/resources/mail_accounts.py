"""
送信メール設定リソースモジュール

このモジュールは、Re:lation APIの送信メール設定リソースへのアクセスを提供します。
"""
from typing import List, Optional, Iterator

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

    def iter_all(self, message_box_id: int, per_page: Optional[int] = None) -> Iterator[MailAccount]:
        """全ページの送信メール設定を透過的に取得

        ページングを意識せずに、すべての送信メール設定を順番に列挙する
        ジェネレータです。内部で ``list`` を ``page=1`` から呼び出し、
        各ページの ``MailAccount`` を逐次 yield します。取得件数が
        ``per_page`` 未満（または0件）になったページを最終ページとみなして
        停止します。

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト30, 最大100）

        Yields:
            MailAccount: 送信メール設定オブジェクト
        """
        # per_page 未指定時はAPIデフォルト件数を停止判定に用いる
        page_size = per_page if per_page is not None else 30
        # 無限ループに対する安全弁（通常運用では到達しない十分大きな上限）
        max_pages = 1000
        for page in range(1, max_pages + 1):
            accounts = self.list(message_box_id=message_box_id, per_page=per_page, page=page)
            for account in accounts:
                yield account
            if len(accounts) < page_size:
                break
