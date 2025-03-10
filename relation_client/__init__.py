"""
Re:lation API Python クライアントライブラリ

Re:lationのAPIを簡単に利用するためのPythonライブラリです。
"""

__version__ = '0.1.0'

from .client import RelationClient  # noqa
from .models import (
    Customer, CustomerGroup, Email, Tel,
    Ticket, Message, Comment, Attachment,
    ChatPlus, Yahoo, RMesse, Line,
    ChatConversation, ChatPlusConversation, YahooConversation, RMesseConversation, LineConversation,
    MessageBox, PendingReason, User, CaseCategory, Label, Badge, MailAccount, Template
)
from .constants import (
    # ステータス
    STATUS_OPEN, STATUS_ONGOING, STATUS_CLOSED, STATUS_UNWANTED, STATUS_TRASH, STATUS_SPAM,
    # 色
    COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_BLUE, COLOR_PINK,
    # チャネル
    METHOD_MAIL, METHOD_TWEET, METHOD_TWITTER_DM, METHOD_RECORD, METHOD_LINE,
    METHOD_CHATPLUS, METHOD_R_MESSE, METHOD_YAHOO, METHOD_SMS, METHOD_CALL,
    # メッセージの状態
    ACTION_RECEIVED, ACTION_SENT, ACTION_DRAFT, ACTION_REQUESTED, ACTION_APPROVED,
    ACTION_REJECTED, ACTION_SENDING, ACTION_SCHEDULED, ACTION_SEND_ERROR,
    ACTION_CONVERSATION, ACTION_END_CONVERSATION,
    # 応対種別
    ICON_RECEIVED_PHONE, ICON_CALLED_PHONE, ICON_MEETING, ICON_SALES, ICON_POSTAL, ICON_NOTE,
    # コメントタイプ
    COMMENT_TYPE_COMMENT, COMMENT_TYPE_REQUEST, COMMENT_TYPE_APPROVE, COMMENT_TYPE_REJECT,
    COMMENT_TYPE_PULLBACK, COMMENT_TYPE_ASSIGN, COMMENT_TYPE_SNOOZE, COMMENT_TYPE_CANCELED_SNOOZE,
    # チャット会話種別
    CONVERSATION_TYPE_TEXT, CONVERSATION_TYPE_FILE, CONVERSATION_TYPE_IMAGE, CONVERSATION_TYPE_VIDEO,
    CONVERSATION_TYPE_AUDIO, CONVERSATION_TYPE_LOCATION, CONVERSATION_TYPE_STICKER,
    CONVERSATION_TYPE_CHATPLUS_TEXTFORM, CONVERSATION_TYPE_CHATPLUS_CAROUSEL,
    CONVERSATION_TYPE_CHATPLUS_CHATBOT, CONVERSATION_TYPE_CHATPLUS_IMAGEMAP,
    # スヌーズから復帰する日時（定義済み）
    SNOOZE_NO_TERM, SNOOZE_TODAY, SNOOZE_TOMORROW, SNOOZE_WEEKEND,
    SNOOZE_NEXT_MONDAY, SNOOZE_NEXT_WEEK, SNOOZE_NEXT_MONTH, SNOOZE_AFTER_MONTH,
    # ユーザー状態
    USER_STATUS_AVAILABLE, USER_STATUS_CONFIRMING, USER_STATUS_LOCKED, USER_STATUS_DELETED
) 