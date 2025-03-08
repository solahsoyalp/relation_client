"""
テンプレートリソースモジュール

このモジュールは、Re:lation APIのテンプレートリソースへのアクセスを提供します。
"""
from typing import List, Dict, Any, Optional

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