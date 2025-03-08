"""
チケットリソースモジュール

このモジュールは、Re:lation APIのチケット関連操作を処理するリソースクラスを提供します。
"""
from typing import List, Dict, Any, Optional, Union

from ..models import Ticket, Message
from ..constants import (
    STATUS_OPEN, STATUS_ONGOING, STATUS_CLOSED, STATUS_UNWANTED, STATUS_TRASH, STATUS_SPAM,
    METHOD_RECORD, ICON_RECEIVED_PHONE
)


class TicketResource:
    """チケットリソースクラス
    
    このクラスは、チケット関連のAPIエンドポイントへのアクセスを提供します。
    """
    
    def __init__(self, client):
        """初期化
        
        Args:
            client: APIクライアントインスタンス
        """
        self.client = client
        
    def search(
        self, 
        message_box_id: int,
        ticket_ids: Optional[List[int]] = None,
        label_ids: Optional[List[int]] = None,
        status_cds: Optional[List[str]] = None,
        color_cds: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        message_ids: Optional[List[int]] = None,
        has_attachments: Optional[bool] = None,
        method_cds: Optional[List[str]] = None,
        action_cds: Optional[List[str]] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        date: Optional[str] = None,
        within: Optional[str] = None,
        pending_reason_ids: Optional[List[int]] = None,
        per_page: int = 50,
        page: int = 1
    ) -> List[Ticket]:
        """チケットを検索します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_ids: チケットIDリスト
            label_ids: ラベルIDリスト
            status_cds: ステータスコードリスト
            color_cds: 色コードリスト
            assignee: 担当者のメンション名
            message_ids: メッセージIDリスト
            has_attachments: 添付ファイルの有無
            method_cds: チャネルコードリスト
            action_cds: アクションコードリスト
            since: メッセージの送信日時の開始（ISO 8601形式）
            until: メッセージの送信日時の終了（ISO 8601形式）
            date: メッセージの送信日時の終了（ISO 8601形式）
            within: メッセージの送信日時の期間（1days〜99days または 1months〜99months）
            pending_reason_ids: 保留理由IDリスト
            per_page: 1ページあたりの表示件数（最大50）
            page: ページ番号
            
        Returns:
            チケットのリスト
        """
        path = f"{message_box_id}/tickets/search"
        
        # リクエストパラメータを構築
        data = {}
        if ticket_ids:
            data["ticket_ids"] = ticket_ids
        if label_ids:
            data["label_ids"] = label_ids
        if status_cds:
            data["status_cds"] = status_cds
        if color_cds:
            data["color_cds"] = color_cds
        if assignee is not None:
            data["assignee"] = assignee
        if message_ids:
            data["message_ids"] = message_ids
        if has_attachments is not None:
            data["has_attachments"] = has_attachments
        if method_cds:
            data["method_cds"] = method_cds
        if action_cds:
            data["action_cds"] = action_cds
        if since:
            data["since"] = since
        if until:
            data["until"] = until
        if date:
            data["date"] = date
        if within:
            data["within"] = within
        if pending_reason_ids:
            data["pending_reason_ids"] = pending_reason_ids
        if per_page:
            data["per_page"] = per_page
        if page:
            data["page"] = page
            
        # API呼び出し
        response = self.client.post(path, data=data)
        
        # レスポンスをTicketオブジェクトのリストに変換
        return [Ticket.from_dict(ticket_data) for ticket_data in response]
    
    def get(self, message_box_id: int, ticket_id: int) -> Ticket:
        """チケットを取得します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            
        Returns:
            チケット
        """
        path = f"{message_box_id}/tickets/{ticket_id}"
        
        # API呼び出し
        response = self.client.get(path)
        
        # レスポンスをTicketオブジェクトに変換
        return Ticket.from_dict(response)
    
    def update(
        self, 
        message_box_id: int, 
        ticket_id: int,
        status_cd: Optional[str] = None,
        pending_reason_id: Optional[int] = None,
        snooze_term: Optional[str] = None,
        snooze_time: Optional[str] = None,
        snooze_comment: Optional[str] = None,
        notification_mention_name: Optional[str] = None,
        label_ids: Optional[List[int]] = None,
        assignee: Optional[str] = None,
        approval_required: Optional[bool] = None,
        assign_comment: Optional[str] = None,
        color_cd: Optional[str] = None,
        case_category_ids: Optional[List[int]] = None
    ) -> None:
        """チケットを更新します。
        
        Args:
            message_box_id: 受信箱ID
            ticket_id: チケットID
            status_cd: ステータス
            pending_reason_id: 保留理由ID（Noneを指定すると解除）
            snooze_term: スヌーズから復帰する日時（定義済み）
            snooze_time: スヌーズから復帰する日時（任意設定）（ISO 8601形式）
            snooze_comment: スヌーズのコメント
            notification_mention_name: スヌーズ復帰時に通知するユーザのメンション名
            label_ids: ラベルIDのリスト（空リストで解除）
            assignee: 担当者のメンション名（Noneで解除）
            approval_required: 送信操作で上長の承認を必須とするか
            assign_comment: 担当者設定時のコメント
            color_cd: 色（Noneで解除）
            case_category_ids: チケット分類IDのリスト（空リストで解除）
        """
        path = f"{message_box_id}/tickets/{ticket_id}"
        
        # リクエストパラメータを構築
        data = {}
        if status_cd is not None:
            data["status_cd"] = status_cd
        if pending_reason_id is not None:
            data["pending_reason_id"] = pending_reason_id
        if snooze_term is not None:
            data["snooze_term"] = snooze_term
        if snooze_time is not None:
            data["snooze_time"] = snooze_time
        if snooze_comment is not None:
            data["snooze_comment"] = snooze_comment
        if notification_mention_name is not None:
            data["notification_mention_name"] = notification_mention_name
        if label_ids is not None:
            data["label_ids"] = label_ids
        if assignee is not None:
            data["assignee"] = assignee
        if approval_required is not None:
            data["approval_required"] = approval_required
        if assign_comment is not None:
            data["assign_comment"] = assign_comment
        if color_cd is not None:
            data["color_cd"] = color_cd
        if case_category_ids is not None:
            data["case_category_ids"] = case_category_ids
            
        # API呼び出し
        self.client.put(path, data=data)
        
    def create_record(
        self,
        message_box_id: int,
        subject: str,
        operated_at: str,
        duration: int,
        body: str,
        ticket_id: Optional[int] = None,
        status_cd: str = STATUS_CLOSED,
        operator: Optional[str] = None,
        customer_email: Optional[str] = None,
        customer_tel: Optional[str] = None,
        icon_cd: str = ICON_RECEIVED_PHONE,
        is_html: bool = False,
        assignee: Optional[str] = None
    ) -> Dict[str, int]:
        """応対メモを作成します。
        
        Args:
            message_box_id: 受信箱ID
            subject: 件名
            operated_at: 応対日時（ISO 8601形式）
            duration: 応対時間（分）（0〜1440）
            body: 本文
            ticket_id: チケットID（省略時は新規チケット）
            status_cd: ステータス（省略時はclosed）
            operator: 応対者のメンション名
            customer_email: 顧客メールアドレス
            customer_tel: 顧客電話番号
            icon_cd: 応対種別（省略時はreceived_phone）
            is_html: HTMLかどうか（省略時はfalse）
            assignee: 新規チケットとして登録された場合の担当者のメンション名
            
        Returns:
            {"message_id": メッセージID, "ticket_id": チケットID}
        """
        path = f"{message_box_id}/records"
        
        # リクエストパラメータを構築
        data = {
            "subject": subject,
            "operated_at": operated_at,
            "duration": duration,
            "body": body
        }
        
        if ticket_id is not None:
            data["ticket_id"] = ticket_id
        if status_cd is not None:
            data["status_cd"] = status_cd
        if operator is not None:
            data["operator"] = operator
        if customer_email is not None:
            data["customer_email"] = customer_email
        if customer_tel is not None:
            data["customer_tel"] = customer_tel
        if icon_cd is not None:
            data["icon_cd"] = icon_cd
        if is_html is not None:
            data["is_html"] = is_html
        if assignee is not None:
            data["assignee"] = assignee
            
        # API呼び出し
        response = self.client.post(path, data=data)
        
        return response 