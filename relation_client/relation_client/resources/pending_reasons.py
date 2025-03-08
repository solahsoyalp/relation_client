"""
保留理由リソースモジュール

このモジュールは、Re:lation APIの保留理由に関連するリソースクラスを提供します。
"""
from typing import List

from ..models import PendingReason


class PendingReasonResource:
    """保留理由リソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアント
        """
        self.client = client

    def list(self, message_box_id: int) -> List[PendingReason]:
        """保留理由一覧を取得

        Args:
            message_box_id: 受信箱ID

        Returns:
            List[PendingReason]: 保留理由オブジェクトのリスト
        """
        response = self.client.get(f"{message_box_id}/pending_reasons")
        return [PendingReason.from_dict(item) for item in response] 