"""
テンプレートリソースモジュール

このモジュールは、Re:lation APIのテンプレートリソースへのアクセスを提供します。
"""
from typing import List, Dict, Any, Optional, Iterator

from ..models import Template


class TemplateResource:
    """テンプレートリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def list(self, message_box_id: int, per_page: Optional[int] = None, page: Optional[int] = None) -> List[Template]:
        """テンプレート一覧を取得

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト10, 最大30）
            page: ページ番号（デフォルト1）

        Returns:
            List[Template]: テンプレートオブジェクトのリスト
        """
        # クエリパラメータの準備
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # APIリクエスト
        response = self.client.get(f'{message_box_id}/templates', params=params)
        
        # レスポンスをテンプレートオブジェクトのリストに変換
        if isinstance(response, list):
            return [Template.from_dict(template_data) for template_data in response]
        return []

    def iter_all(self, message_box_id: int, per_page: Optional[int] = None) -> Iterator[Template]:
        """全ページのテンプレートを透過的に取得

        ページングを意識せずに、すべてのテンプレートを順番に列挙する
        ジェネレータです。内部で ``list`` を ``page=1`` から呼び出し、
        各ページの ``Template`` を逐次 yield します。取得件数が
        ``per_page`` 未満（または0件）になったページを最終ページとみなして
        停止します。

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト10, 最大30）

        Yields:
            Template: テンプレートオブジェクト
        """
        # per_page 未指定時はAPIデフォルト件数を停止判定に用いる
        page_size = per_page if per_page is not None else 10
        # 無限ループに対する安全弁（通常運用では到達しない十分大きな上限）
        max_pages = 1000
        for page in range(1, max_pages + 1):
            templates = self.list(message_box_id=message_box_id, per_page=per_page, page=page)
            for template in templates:
                yield template
            if len(templates) < page_size:
                break

    def search(self, message_box_id: int, template_category_name: Optional[str] = None) -> List[Template]:
        """テンプレートを検索

        Args:
            message_box_id: 受信箱ID
            template_category_name: テンプレートカテゴリ名

        Returns:
            List[Template]: テンプレートオブジェクトのリスト
        """
        # リクエストデータの準備
        data = {}
        if template_category_name:
            data['template_category_name'] = template_category_name
        
        # APIリクエスト
        response = self.client.post(f'{message_box_id}/templates/search', data=data)
        
        # レスポンスをテンプレートオブジェクトのリストに変換
        if isinstance(response, list):
            return [Template.from_dict(template_data) for template_data in response]
        return [] 