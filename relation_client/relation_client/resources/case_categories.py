"""
チケット分類リソースモジュール

このモジュールは、Re:lation APIのチケット分類に関連するリソースクラスを提供します。
"""
from typing import List, Dict, Optional, Any

from ..models import CaseCategory


class CaseCategoryResource:
    """チケット分類リソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアント
        """
        self.client = client

    def list(self, message_box_id: int, per_page: Optional[int] = None, page: Optional[int] = None) -> List[CaseCategory]:
        """チケット分類一覧を取得

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト30, 最大100）
            page: ページ番号（デフォルト1）

        Returns:
            List[CaseCategory]: チケット分類オブジェクトのリスト
        """
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page

        response = self.client.get(f'{message_box_id}/case_categories', params=params)
        return [CaseCategory.from_dict(item) for item in response]

    def create(self, message_box_id: int, name: str, parent_id: Optional[int] = None) -> Dict[str, int]:
        """チケット分類を登録

        Args:
            message_box_id: 受信箱ID
            name: チケット分類名
            parent_id: 親チケット分類ID

        Returns:
            Dict[str, int]: 登録したチケット分類ID
        """
        data = {
            'name': name
        }
        if parent_id is not None:
            data['parent_id'] = parent_id

        return self.client.post(f'{message_box_id}/case_categories', data=data)

    def update(self, message_box_id: int, case_category_id: int, name: Optional[str] = None, 
              parent_id: Optional[int] = None, archived: Optional[bool] = None) -> None:
        """チケット分類を更新

        Args:
            message_box_id: 受信箱ID
            case_category_id: チケット分類ID
            name: チケット分類名
            parent_id: 親チケット分類ID
            archived: アーカイブするかどうか
            
        Note:
            - 更新するチケット分類に子チケット分類や孫チケット分類が存在する場合、それらもアーカイブされます。
            - 親チケット分類がアーカイブされている場合、その分類は復活できません。
        """
        data = {}
        if name is not None:
            data['name'] = name
        if parent_id is not None:
            data['parent_id'] = parent_id
        if archived is not None:
            data['archived'] = archived

        path = f'{message_box_id}/case_categories/{case_category_id}'
        self.client.put(path, data=data) 