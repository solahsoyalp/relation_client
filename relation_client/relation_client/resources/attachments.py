"""
添付ファイルリソースモジュール

このモジュールは、Re:lation APIの添付ファイルリソースへのアクセスを提供します。
"""
from typing import Dict, Any


class AttachmentResource:
    """添付ファイルリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def get_download_url(self, message_box_id: int, attachment_id: int) -> Dict[str, Any]:
        """添付ファイルダウンロード用URLを取得

        Args:
            message_box_id: 受信箱ID
            attachment_id: 添付ファイルID

        Returns:
            Dict[str, Any]: ダウンロード情報
                - url: ダウンロード用URL
                - file_name: ファイル名
                - expires_in_sec: 有効期限（秒）
        """
        return self.client.get(f'{message_box_id}/messages/attachments/{attachment_id}') 