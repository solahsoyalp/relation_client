"""
Re:lation APIリソースモジュール

このモジュールは、Re:lation APIの各リソースタイプに対応するクラスを提供します。
"""

from .customers import CustomerResource
from .customer_groups import CustomerGroupResource
from .tickets import TicketResource
from .chats import ChatResource
from .message_boxes import MessageBoxResource
from .pending_reasons import PendingReasonResource
from .users import UserResource
from .case_categories import CaseCategoryResource
from .labels import LabelResource
from .badges import BadgeResource
from .mail_accounts import MailAccountResource
from .mails import MailResource
from .templates import TemplateResource
from .attachments import AttachmentResource 