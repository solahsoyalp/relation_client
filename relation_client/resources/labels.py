"""
ラベルリソースモジュール

このモジュールは、Re:lation APIのラベルリソースへのアクセスを提供します。
"""
from typing import List, Dict, Any, Optional, Iterator

from ..models import Label


class LabelResource:
    """ラベルリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def list(self, message_box_id: int, per_page: Optional[int] = None, page: Optional[int] = None) -> List[Label]:
        """ラベル一覧を取得

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト50, 最大100）
            page: ページ番号（デフォルト1）

        Returns:
            List[Label]: ラベルオブジェクトのリスト
        """
        # クエリパラメータの準備
        params = {}
        if per_page is not None:
            params['per_page'] = per_page
        if page is not None:
            params['page'] = page
        
        # APIリクエスト
        response = self.client.get(f'{message_box_id}/labels', params=params)
        
        # レスポンスをラベルオブジェクトのリストに変換
        if isinstance(response, list):
            return [Label.from_dict(label_data) for label_data in response]
        return []

    def iter_all(self, message_box_id: int, per_page: Optional[int] = None) -> Iterator[Label]:
        """全ページのラベルを透過的に取得

        ページングを意識せずに、すべてのラベルを順番に列挙する
        ジェネレータです。内部で ``list`` を ``page=1`` から呼び出し、
        各ページの ``Label`` を逐次 yield します。取得件数が
        ``per_page`` 未満（または0件）になったページを最終ページとみなして
        停止します。

        Args:
            message_box_id: 受信箱ID
            per_page: 1ページに表示する件数（デフォルト50, 最大100）

        Yields:
            Label: ラベルオブジェクト
        """
        # per_page 未指定時はAPIデフォルト件数を停止判定に用いる
        page_size = per_page if per_page is not None else 50
        # 無限ループに対する安全弁（通常運用では到達しない十分大きな上限）
        max_pages = 1000
        for page in range(1, max_pages + 1):
            labels = self.list(message_box_id=message_box_id, per_page=per_page, page=page)
            for label in labels:
                yield label
            if len(labels) < page_size:
                break

    def create(self, message_box_id: int, name: str, color: str, parent_id: Optional[int] = None) -> Dict[str, int]:
        """ラベルを登録

        Args:
            message_box_id: 受信箱ID
            name: ラベル名
            color: 色
            parent_id: 親ラベルID（任意）

        Returns:
            Dict[str, int]: 登録されたラベルのIDを含む辞書
        """
        # リクエストデータの準備
        data = {
            'name': name,
            'color': color
        }
        if parent_id is not None:
            data['parent_id'] = parent_id
        
        # APIリクエスト
        return self.client.post(f'{message_box_id}/labels', data=data)
    
    def update(self, message_box_id: int, label_id: int, name: Optional[str] = None, 
               color: Optional[str] = None, parent_id: Optional[int] = None) -> None:
        """ラベルを更新

        Args:
            message_box_id: 受信箱ID
            label_id: ラベルID
            name: ラベル名（任意）
            color: 色（任意）
            parent_id: 親ラベルID（任意、Noneの場合は親なしに設定）
        """
        # リクエストデータの準備
        data = {}
        if name is not None:
            data['name'] = name
        if color is not None:
            data['color'] = color
        if parent_id is not None:
            data['parent_id'] = parent_id
        
        # APIリクエスト
        self.client.put(f'{message_box_id}/labels/{label_id}', data=data) 