"""
Re:lation APIデータモデルモジュール

このモジュールは、Re:lation APIから返されるデータオブジェクトのモデルクラスを定義します。
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


@dataclass
class RelationObject:
    """Re:lation APIオブジェクトの基本クラス"""
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RelationObject':
        """辞書からオブジェクトを作成"""
        instance = cls()
        instance._raw_data = data
        return instance


@dataclass
class Email:
    """メールアドレス情報"""
    email: str

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Email':
        return cls(email=data.get('email', ''))


@dataclass
class Tel:
    """電話番号情報"""
    tel: str

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Tel':
        return cls(tel=data.get('tel', ''))


@dataclass
class Customer(RelationObject):
    """顧客情報"""
    customer_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name_kana: Optional[str] = None
    first_name_kana: Optional[str] = None
    company_name: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    gender_cd: Optional[int] = None
    system_id1: Optional[str] = None
    default_assignee: Optional[str] = None
    default_assignee_id: Optional[int] = None
    emails: List[Email] = field(default_factory=list)
    archived_emails: List[Email] = field(default_factory=list)
    tels: List[Tel] = field(default_factory=list)
    archived_tels: List[Tel] = field(default_factory=list)
    badge_ids: List[int] = field(default_factory=list)
    last_updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """辞書からCustomerオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.customer_id = data.get('customer_id')
        instance.last_name = data.get('last_name')
        instance.first_name = data.get('first_name')
        instance.last_name_kana = data.get('last_name_kana')
        instance.first_name_kana = data.get('first_name_kana')
        instance.company_name = data.get('company_name')
        instance.title = data.get('title')
        instance.url = data.get('url')
        instance.gender_cd = data.get('gender_cd')
        instance.system_id1 = data.get('system_id1')
        instance.default_assignee = data.get('default_assignee')
        instance.default_assignee_id = data.get('default_assignee_id')
        
        # メールアドレス
        instance.emails = [Email.from_dict(email) if isinstance(email, dict) else Email(email=email) 
                           for email in data.get('emails', [])]
        
        # アーカイブメールアドレス
        instance.archived_emails = [Email.from_dict(email) if isinstance(email, dict) else Email(email=email) 
                                    for email in data.get('archived_emails', [])]
        
        # 電話番号
        instance.tels = [Tel.from_dict(tel) if isinstance(tel, dict) else Tel(tel=tel) 
                         for tel in data.get('tels', [])]
        
        # アーカイブ電話番号
        instance.archived_tels = [Tel.from_dict(tel) if isinstance(tel, dict) else Tel(tel=tel) 
                                  for tel in data.get('archived_tels', [])]
        
        # バッジID
        instance.badge_ids = data.get('badge_ids', [])
        
        # 更新日時
        if 'last_updated_at' in data and data['last_updated_at']:
            try:
                instance.last_updated_at = datetime.fromisoformat(data['last_updated_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance


@dataclass
class CustomerGroup(RelationObject):
    """アドレス帳情報"""
    customer_group_id: Optional[int] = None
    name: Optional[str] = None
    message_box_ids: List[int] = field(default_factory=list)
    last_updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomerGroup':
        """辞書からCustomerGroupオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.customer_group_id = data.get('customer_group_id')
        instance.name = data.get('name')
        instance.message_box_ids = data.get('message_box_ids', [])
        
        # 更新日時
        if 'last_updated_at' in data and data['last_updated_at']:
            try:
                instance.last_updated_at = datetime.fromisoformat(data['last_updated_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance 


@dataclass
class Comment(RelationObject):
    """コメント情報"""
    commenter: str = None
    comment_type: str = None
    comment: str = None
    commented_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """辞書からCommentオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.commenter = data.get('commenter')
        instance.comment_type = data.get('comment_type')
        instance.comment = data.get('comment')
        
        # コメント日時
        if 'commented_at' in data and data['commented_at']:
            try:
                instance.commented_at = datetime.fromisoformat(data['commented_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance


@dataclass
class Attachment(RelationObject):
    """添付ファイル情報"""
    attachment_id: int = None
    file_name: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attachment':
        """辞書からAttachmentオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.attachment_id = data.get('attachment_id')
        instance.file_name = data.get('file_name')
                
        return instance


@dataclass
class Message(RelationObject):
    """メッセージ情報"""
    message_id: int = None
    from_address: Optional[str] = None
    to: Optional[str] = None
    cc: Optional[str] = None
    bcc: Optional[str] = None
    sent_at: Optional[datetime] = None
    title: str = None
    body: str = None
    method_cd: str = None
    action_cd: str = None
    is_html: bool = False
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None
    comments: List[Comment] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)
    reply_to: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """辞書からMessageオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.message_id = data.get('message_id')
        instance.from_address = data.get('from')  # fromはPython予約語なのでfrom_addressに変更
        instance.to = data.get('to')
        instance.cc = data.get('cc')
        instance.bcc = data.get('bcc')
        instance.title = data.get('title')
        instance.body = data.get('body')
        instance.method_cd = data.get('method_cd')
        instance.action_cd = data.get('action_cd')
        instance.is_html = data.get('is_html', False)
        instance.reply_to = data.get('reply_to')
        
        # 送信日時
        if 'sent_at' in data and data['sent_at']:
            try:
                instance.sent_at = datetime.fromisoformat(data['sent_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        # 作成日時
        if 'created_at' in data and data['created_at']:
            try:
                instance.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        # 更新日時
        if 'last_updated_at' in data and data['last_updated_at']:
            try:
                instance.last_updated_at = datetime.fromisoformat(data['last_updated_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        # コメント
        instance.comments = [Comment.from_dict(comment) for comment in data.get('comments', [])]
        
        # 添付ファイル
        instance.attachments = [Attachment.from_dict(attachment) for attachment in data.get('attachments', [])]
                
        return instance


@dataclass
class Ticket(RelationObject):
    """チケット情報"""
    ticket_id: int = None
    assignee: Optional[str] = None
    status_cd: str = None
    created_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None
    title: str = None
    color_cd: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    case_category_ids: List[int] = field(default_factory=list)
    label_ids: List[int] = field(default_factory=list)
    pending_reason_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ticket':
        """辞書からTicketオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.ticket_id = data.get('ticket_id')
        instance.assignee = data.get('assignee')
        instance.status_cd = data.get('status_cd')
        instance.title = data.get('title')
        instance.color_cd = data.get('color_cd')
        instance.case_category_ids = data.get('case_category_ids', [])
        instance.label_ids = data.get('label_ids', [])
        instance.pending_reason_id = data.get('pending_reason_id')
        
        # 作成日時
        if 'created_at' in data and data['created_at']:
            try:
                instance.created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        # 更新日時
        if 'last_updated_at' in data and data['last_updated_at']:
            try:
                instance.last_updated_at = datetime.fromisoformat(data['last_updated_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        # メッセージ
        if 'messages' in data:
            instance.messages = [Message.from_dict(message) for message in data.get('messages', [])]
                
        return instance


@dataclass
class ChatConversation(RelationObject):
    """チャット会話の基本クラス"""
    action_cd: str = None
    speaker_name: str = None
    sent_by: Optional[str] = None
    sent_at: Optional[datetime] = None
    conversation_type: str = None
    note: Optional[str] = None
    file_name: Optional[str] = None
    auto_send: Optional[bool] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatConversation':
        """辞書からChatConversationオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.action_cd = data.get('action_cd')
        instance.speaker_name = data.get('speaker_name')
        instance.sent_by = data.get('sent_by')
        instance.conversation_type = data.get('conversation_type')
        instance.note = data.get('note')
        instance.file_name = data.get('file_name')
        instance.auto_send = data.get('auto_send')
        
        # 送信日時
        if 'sent_at' in data and data['sent_at']:
            try:
                instance.sent_at = datetime.fromisoformat(data['sent_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance


@dataclass
class ChatPlusConversation(ChatConversation):
    """ChatPlus会話"""
    chatplus_conversation_id: int = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatPlusConversation':
        """辞書からChatPlusConversationオブジェクトを作成"""
        instance = super().from_dict(data)
        instance.chatplus_conversation_id = data.get('chatplus_conversation_id')
        return instance


@dataclass
class YahooConversation(ChatConversation):
    """Yahoo!ショッピング会話"""
    yahoo_conversation_id: int = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'YahooConversation':
        """辞書からYahooConversationオブジェクトを作成"""
        instance = super().from_dict(data)
        instance.yahoo_conversation_id = data.get('yahoo_conversation_id')
        return instance


@dataclass
class RMesseConversation(ChatConversation):
    """R-Messe会話"""
    r_messe_conversation_id: int = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RMesseConversation':
        """辞書からRMesseConversationオブジェクトを作成"""
        instance = super().from_dict(data)
        instance.r_messe_conversation_id = data.get('r_messe_conversation_id')
        return instance


@dataclass
class LineConversation(ChatConversation):
    """LINE会話"""
    line_conversation_id: int = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LineConversation':
        """辞書からLineConversationオブジェクトを作成"""
        instance = super().from_dict(data)
        instance.line_conversation_id = data.get('line_conversation_id')
        return instance


@dataclass
class ChatPlus(RelationObject):
    """ChatPlus情報"""
    account: str = None
    account_key: str = None
    email: str = None
    company_name: str = None
    site: str = None
    conversations: List[ChatPlusConversation] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatPlus':
        """辞書からChatPlusオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.account = data.get('account')
        instance.account_key = data.get('account_key')
        instance.email = data.get('email')
        instance.company_name = data.get('company_name')
        instance.site = data.get('site')
        
        # 会話
        if 'conversations' in data:
            instance.conversations = [ChatPlusConversation.from_dict(conv) for conv in data.get('conversations', [])]
                
        return instance


@dataclass
class Yahoo(RelationObject):
    """Yahoo!ショッピング情報"""
    account: str = None
    store_account: str = None
    email: str = None
    inquiry_status: str = None
    inquiry_kind: str = None
    inquiry_category: str = None
    order_id: str = None
    order_url: str = None
    item_number: str = None
    item_url: str = None
    conversations: List[YahooConversation] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Yahoo':
        """辞書からYahooオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.account = data.get('account')
        instance.store_account = data.get('store_account')
        instance.email = data.get('email')
        instance.inquiry_status = data.get('inquiry_status')
        instance.inquiry_kind = data.get('inquiry_kind')
        instance.inquiry_category = data.get('inquiry_category')
        instance.order_id = data.get('order_id')
        instance.order_url = data.get('order_url')
        instance.item_number = data.get('item_number')
        instance.item_url = data.get('item_url')
        
        # 会話
        if 'conversations' in data:
            instance.conversations = [YahooConversation.from_dict(conv) for conv in data.get('conversations', [])]
                
        return instance


@dataclass
class RMesse(RelationObject):
    """R-Messe情報"""
    account: str = None
    email: str = None
    inquiry_status: str = None
    inquiry_category: str = None
    inquiry_type: str = None
    inquiry_number: str = None
    inquiry_url: str = None
    order_number: str = None
    item_number: str = None
    item_name: str = None
    item_url: str = None
    conversations: List[RMesseConversation] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RMesse':
        """辞書からRMesseオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.account = data.get('account')
        instance.email = data.get('email')
        instance.inquiry_status = data.get('inquiry_status')
        instance.inquiry_category = data.get('inquiry_category')
        instance.inquiry_type = data.get('inquiry_type')
        instance.inquiry_number = data.get('inquiry_number')
        instance.inquiry_url = data.get('inquiry_url')
        instance.order_number = data.get('order_number')
        instance.item_number = data.get('item_number')
        instance.item_name = data.get('item_name')
        instance.item_url = data.get('item_url')
        
        # 会話
        if 'conversations' in data:
            instance.conversations = [RMesseConversation.from_dict(conv) for conv in data.get('conversations', [])]
                
        return instance


@dataclass
class Line(RelationObject):
    """LINE情報"""
    account: str = None
    channel_id: str = None
    group_name: str = None
    conversations: List[LineConversation] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Line':
        """辞書からLineオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.account = data.get('account')
        instance.channel_id = data.get('channel_id')
        instance.group_name = data.get('group_name')
        
        # 会話
        if 'conversations' in data:
            instance.conversations = [LineConversation.from_dict(conv) for conv in data.get('conversations', [])]
                
        return instance


@dataclass
class MessageBox(RelationObject):
    """受信箱情報"""
    message_box_id: Optional[int] = None
    name: Optional[str] = None
    color: Optional[str] = None
    customer_group_id: Optional[int] = None
    last_updated_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageBox':
        """辞書からMessageBoxオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.message_box_id = data.get('message_box_id')
        instance.name = data.get('name')
        instance.color = data.get('color')
        instance.customer_group_id = data.get('customer_group_id')
        
        # 更新日時
        if 'last_updated_at' in data and data['last_updated_at']:
            try:
                instance.last_updated_at = datetime.fromisoformat(data['last_updated_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance 


@dataclass
class PendingReason(RelationObject):
    """保留理由情報"""
    pending_reason_id: int = None
    name: str = None
    is_snoozed: bool = False
    snooze_term: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PendingReason':
        """辞書からPendingReasonオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.pending_reason_id = data.get('pending_reason_id')
        instance.name = data.get('name')
        instance.is_snoozed = data.get('is_snoozed', False)
        instance.snooze_term = data.get('snooze_term')
                
        return instance 


@dataclass
class User(RelationObject):
    """ユーザー情報"""
    mention_name: str = None
    status_cd: str = None
    first_name: str = None
    last_name: str = None
    department_name: Optional[str] = None
    employee_no: Optional[str] = None
    email: str = None
    is_tenant_admin: bool = False
    is_otp_required: bool = False
    last_page_loaded_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """辞書からUserオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.mention_name = data.get('mention_name')
        instance.status_cd = data.get('status_cd')
        instance.first_name = data.get('first_name')
        instance.last_name = data.get('last_name')
        instance.department_name = data.get('department_name')
        instance.employee_no = data.get('employee_no')
        instance.email = data.get('email')
        instance.is_tenant_admin = data.get('is_tenant_admin', False)
        instance.is_otp_required = data.get('is_otp_required', False)
        
        # 最終アクセス日時
        if 'last_page_loaded_at' in data and data['last_page_loaded_at']:
            try:
                instance.last_page_loaded_at = datetime.fromisoformat(data['last_page_loaded_at'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        return instance 


@dataclass
class CaseCategory(RelationObject):
    """チケット分類情報"""
    case_category_id: int = None
    name: str = None
    parent_id: Optional[int] = None
    archived: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CaseCategory':
        """辞書からCaseCategoryオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.case_category_id = data.get('case_category_id')
        instance.name = data.get('name')
        instance.parent_id = data.get('parent_id')
        instance.archived = data.get('archived', False)
                
        return instance 


@dataclass
class Label(RelationObject):
    """ラベル情報"""
    label_id: int = None
    name: str = None
    color: str = None
    parent_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Label':
        """辞書からLabelオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.label_id = data.get('label_id')
        instance.name = data.get('name')
        instance.color = data.get('color')
        instance.parent_id = data.get('parent_id')
                
        return instance 


@dataclass
class Badge(RelationObject):
    """バッジ情報"""
    badge_id: int = None
    name: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Badge':
        """辞書からBadgeオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.badge_id = data.get('badge_id')
        instance.name = data.get('name')
                
        return instance 


@dataclass
class MailAccount(RelationObject):
    """送信メール設定情報"""
    mail_account_id: int = None
    name: str = None
    email: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MailAccount':
        """辞書からMailAccountオブジェクトを作成"""
        instance = super().from_dict(data)
        
        instance.mail_account_id = data.get('mail_account_id')
        instance.name = data.get('name')
        instance.email = data.get('email')
                
        return instance


@dataclass
class Template(RelationObject):
    """テンプレート情報"""
    template_id: int = None
    template_category_name: str = None
    template_name: str = None
    from_: str = None  # fromはPythonの予約語のため、from_を使用
    to: str = None
    cc: str = None
    bcc: str = None
    title: str = None
    html_body: str = None
    text_body: str = None
    case_category_ids: List[int] = field(default_factory=list)
    label_ids: List[int] = field(default_factory=list)
    questionnaire_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """辞書からテンプレートオブジェクトを作成"""
        instance = cls()
        instance._raw_data = data
        instance.template_id = data.get('template_id')
        instance.template_category_name = data.get('template_category_name')
        instance.template_name = data.get('template_name')
        instance.from_ = data.get('from')  # APIレスポンスでは 'from' だが、Pythonでは 'from_' として扱う
        instance.to = data.get('to')
        instance.cc = data.get('cc')
        instance.bcc = data.get('bcc')
        instance.title = data.get('title')
        instance.html_body = data.get('html_body')
        instance.text_body = data.get('text_body')
        instance.case_category_ids = data.get('case_category_ids', [])
        instance.label_ids = data.get('label_ids', [])
        instance.questionnaire_name = data.get('questionnaire_name')
        return instance