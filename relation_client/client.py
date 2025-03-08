"""
Re:lation APIクライアント

このモジュールは、Re:lation APIとの通信を処理するメインクライアントクラスを提供します。
"""

import json
import time
from typing import Dict, Any, Optional, Union, List, Type, TypeVar

import requests

from .constants import (
    API_VERSION, BASE_URL_FORMAT,
    RATE_LIMIT_LIMIT, RATE_LIMIT_REMAINING, RATE_LIMIT_RESET,
    HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED, HTTP_FORBIDDEN, HTTP_NOT_FOUND,
    HTTP_UNSUPPORTED_MEDIA_TYPE, HTTP_TOO_MANY_REQUESTS, HTTP_SERVER_ERROR,
    HTTP_SERVICE_UNAVAILABLE
)
from .exceptions import (
    AuthenticationError, PermissionError, ResourceNotFoundError,
    RateLimitError, InvalidRequestError, APIError, ServiceUnavailableError
)
from .resources.customers import CustomerResource
from .resources.customer_groups import CustomerGroupResource
from .resources.tickets import TicketResource
from .resources.chats import ChatResource
from .resources.message_boxes import MessageBoxResource
from .resources.pending_reasons import PendingReasonResource
from .resources.users import UserResource
from .resources.case_categories import CaseCategoryResource
from .resources.labels import LabelResource
from .resources.badges import BadgeResource
from .resources.mail_accounts import MailAccountResource
from .resources.mails import MailResource


class RelationClient:
    """Re:lation APIクライアント

    このクラスは、Re:lation APIと通信するための基本クライアントを提供します。
    各エンドポイントへのアクセスは、リソースクラス経由で行います。
    """

    def __init__(
        self,
        access_token: str,
        subdomain: str,
        api_version: str = API_VERSION,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1
    ):
        """RelationClientを初期化します

        Args:
            access_token: APIアクセストークン
            subdomain: ご利用のサブドメイン
            api_version: APIバージョン (デフォルト: v2)
            timeout: リクエストタイムアウト秒数
            max_retries: リトライ最大回数
            retry_delay: リトライ間の待機秒数
        """
        self.access_token = access_token
        self.subdomain = subdomain
        self.api_version = api_version
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self._session = requests.Session()
        self._base_url = BASE_URL_FORMAT.format(
            subdomain=self.subdomain,
            api_version=self.api_version
        )
        
        # リソースの初期化
        self.customers = CustomerResource(self)
        self.customer_groups = CustomerGroupResource(self)
        self.tickets = TicketResource(self)
        self.chats = ChatResource(self)
        self.message_boxes = MessageBoxResource(self)
        self.pending_reasons = PendingReasonResource(self)
        self.users = UserResource(self)
        self.case_categories = CaseCategoryResource(self)
        self.labels = LabelResource(self)
        self.badges = BadgeResource(self)
        self.mail_accounts = MailAccountResource(self)
        self.mails = MailResource(self)
        
