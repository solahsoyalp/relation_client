"""
メールリソースモジュール

このモジュールは、Re:lation APIのメール送信、返信、下書き作成機能へのアクセスを提供します。
"""
from typing import Dict, Any, Optional


class MailResource:
    """メールリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def send(
        self,
        message_box_id: int,
        mail_account_id: int,
        to: str,
        subject: str,
        body: str,
        status_cd: str = "open",
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        is_html: bool = False,
        pending_reason_id: Optional[int] = None
    ) -> Dict[str, int]:
        """メールを送信

        Args:
            message_box_id: 受信箱ID
            mail_account_id: メールアカウントID
            to: 宛先
            subject: 件名
            body: 本文
            status_cd: ステータス（デフォルト: "open"）
            cc: CC（任意）
            bcc: BCC（任意）
            is_html: HTMLメールかどうか（デフォルト: False）
            pending_reason_id: 保留理由ID（任意）

        Returns:
            Dict[str, int]: メッセージIDとチケットIDを含む辞書
        """
        # リクエストデータの準備
        data = {
            "status_cd": status_cd,
            "mail_account_id": mail_account_id,
            "to": to,
            "subject": subject,
            "body": body,
            "is_html": is_html
        }

        # 任意パラメータの追加
        if cc:
            data["cc"] = cc
        if bcc:
            data["bcc"] = bcc
        if pending_reason_id:
            data["pending_reason_id"] = pending_reason_id

        # APIリクエスト
        return self.client.post(f'{message_box_id}/mails', data=data)

    def reply(
        self,
        message_box_id: int,
        message_id: int,
        mail_account_id: int,
        to: str,
        subject: str,
        body: str,
        status_cd: str = "open",
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        is_html: bool = False,
        pending_reason_id: Optional[int] = None
    ) -> Dict[str, int]:
        """メールを返信

        Args:
            message_box_id: 受信箱ID
            message_id: 返信元のメッセージID
            mail_account_id: メールアカウントID
            to: 宛先
            subject: 件名
            body: 本文
            status_cd: ステータス（デフォルト: "open"）
            cc: CC（任意）
            bcc: BCC（任意）
            is_html: HTMLメールかどうか（デフォルト: False）
            pending_reason_id: 保留理由ID（任意）

        Returns:
            Dict[str, int]: メッセージIDとチケットIDを含む辞書
        """
        # リクエストデータの準備
        data = {
            "message_id": message_id,
            "status_cd": status_cd,
            "mail_account_id": mail_account_id,
            "to": to,
            "subject": subject,
            "body": body,
            "is_html": is_html
        }

        # 任意パラメータの追加
        if cc:
            data["cc"] = cc
        if bcc:
            data["bcc"] = bcc
        if pending_reason_id:
            data["pending_reason_id"] = pending_reason_id

        # APIリクエスト
        return self.client.post(f'{message_box_id}/mails/reply', data=data)

    def draft(
        self,
        message_box_id: int,
        mail_account_id: int,
        to: str,
        subject: str,
        body: str,
        message_id: Optional[int] = None,
        status_cd: str = "open",
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        is_html: bool = False,
        pending_reason_id: Optional[int] = None
    ) -> Dict[str, int]:
        """メールの下書きを作成

        Args:
            message_box_id: 受信箱ID
            mail_account_id: メールアカウントID
            to: 宛先
            subject: 件名
            body: 本文
            message_id: 返信元のメッセージID（任意、返信時のみ）
            status_cd: ステータス（デフォルト: "open"）
            cc: CC（任意）
            bcc: BCC（任意）
            is_html: HTMLメールかどうか（デフォルト: False）
            pending_reason_id: 保留理由ID（任意）

        Returns:
            Dict[str, int]: メッセージIDとチケットIDを含む辞書
        """
        # リクエストデータの準備
        data = {
            "status_cd": status_cd,
            "mail_account_id": mail_account_id,
            "to": to,
            "subject": subject,
            "body": body,
            "is_html": is_html
        }

        # 任意パラメータの追加
        if message_id:
            data["message_id"] = message_id
        if cc:
            data["cc"] = cc
        if bcc:
            data["bcc"] = bcc
        if pending_reason_id:
            data["pending_reason_id"] = pending_reason_id

        # APIリクエスト
        return self.client.post(f'{message_box_id}/mails/draft', data=data) 