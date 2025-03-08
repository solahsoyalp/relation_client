"""
メールリソースモジュール

このモジュールは、Re:lation APIのメール送信機能へのアクセスを提供します。
"""
from typing import Dict, Any, Optional, List


class MailResource:
    """メールリソースクラス"""

    def __init__(self, client):
        """初期化

        Args:
            client: APIクライアントインスタンス
        """
        self.client = client

    def send(self, message_box_id: int, mail_account_id: int, to: str, subject: str, body: str,
             cc: Optional[str] = None, bcc: Optional[str] = None,
             reply_to: Optional[str] = None, is_html: bool = False,
             attachments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """メールを送信する

        Args:
            message_box_id: 受信箱ID
            mail_account_id: メールアカウントID
            to: 宛先メールアドレス
            subject: 件名
            body: 本文
            cc: CCアドレス (省略可)
            bcc: BCCアドレス (省略可)
            reply_to: Reply-Toアドレス (省略可)
            is_html: HTMLメールとして送信するかどうか (省略可)
            attachments: 添付ファイル情報のリスト (省略可)

        Returns:
            Dict[str, Any]: 送信結果
        """
        data = {
            'mail_account_id': mail_account_id,
            'to': to,
            'subject': subject,
            'body': body,
            'is_html': is_html
        }

        if cc:
            data['cc'] = cc
        if bcc:
            data['bcc'] = bcc
        if reply_to:
            data['reply_to'] = reply_to
        if attachments:
            data['attachments'] = attachments

        return self.client.post(f'{message_box_id}/mails/send', data=data)

    def reply(self, message_box_id: int, mail_account_id: int, message_id: int,
              body: str, cc: Optional[str] = None, bcc: Optional[str] = None,
              is_html: bool = False, attachments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """メールに返信する

        Args:
            message_box_id: 受信箱ID
            mail_account_id: メールアカウントID
            message_id: 返信元のメッセージID
            body: 本文
            cc: CCアドレス (省略可)
            bcc: BCCアドレス (省略可)
            is_html: HTMLメールとして送信するかどうか (省略可)
            attachments: 添付ファイル情報のリスト (省略可)

        Returns:
            Dict[str, Any]: 返信結果
        """
        data = {
            'mail_account_id': mail_account_id,
            'message_id': message_id,
            'body': body,
            'is_html': is_html
        }

        if cc:
            data['cc'] = cc
        if bcc:
            data['bcc'] = bcc
        if attachments:
            data['attachments'] = attachments

        return self.client.post(f'{message_box_id}/mails/reply', data=data)

    def draft(self, message_box_id: int, mail_account_id: int, to: Optional[str] = None,
              subject: Optional[str] = None, body: Optional[str] = None,
              cc: Optional[str] = None, bcc: Optional[str] = None, reply_to: Optional[str] = None,
              is_html: bool = False, message_id: Optional[int] = None,
              attachments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """メール下書きを作成する

        Args:
            message_box_id: 受信箱ID
            mail_account_id: メールアカウントID
            to: 宛先メールアドレス (新規作成時必須)
            subject: 件名 (新規作成時必須)
            body: 本文
            cc: CCアドレス (省略可)
            bcc: BCCアドレス (省略可)
            reply_to: Reply-Toアドレス (省略可)
            is_html: HTMLメールとして送信するかどうか (省略可)
            message_id: 返信元のメッセージID (省略すると新規作成)
            attachments: 添付ファイル情報のリスト (省略可)

        Returns:
            Dict[str, Any]: 下書き作成結果
        """
        data = {
            'mail_account_id': mail_account_id,
            'is_html': is_html
        }

        if to:
            data['to'] = to
        if subject:
            data['subject'] = subject
        if body:
            data['body'] = body
        if cc:
            data['cc'] = cc
        if bcc:
            data['bcc'] = bcc
        if reply_to:
            data['reply_to'] = reply_to
        if message_id:
            data['message_id'] = message_id
        if attachments:
            data['attachments'] = attachments

        return self.client.post(f'{message_box_id}/mails/draft', data=data) 