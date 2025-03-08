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
from .resources.templates import TemplateResource
from .resources.attachments import AttachmentResource


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
        self.templates = TemplateResource(self)
        self.attachments = AttachmentResource(self)
        
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """APIリクエストを実行します

        Args:
            method: HTTPメソッド (GET, POST, PUT, DELETE)
            path: APIパス (先頭の / は不要)
            params: クエリパラメータ
            data: リクエストボディ (form-data)
            json_data: リクエストボディ (JSON)

        Returns:
            レスポンスの辞書表現

        Raises:
            AuthenticationError: 認証エラー (401)
            PermissionError: 権限エラー (403)
            ResourceNotFoundError: リソースが見つからないエラー (404)
            RateLimitError: レートリミットエラー (429)
            InvalidRequestError: 無効なリクエストエラー (400, 415)
            APIError: APIエラー (500)
            ServiceUnavailableError: サービス利用不可エラー (503)
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        retry_count = 0
        while retry_count <= self.max_retries:
            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json_data,
                    timeout=self.timeout
                )
                
                # レスポンスを処理
                if response.status_code < 400:
                    # 成功レスポンス
                    if not response.content:
                        return {}
                    try:
                        return response.json()
                    except ValueError:
                        return {"data": response.text}
                
                # エラーレスポンスの処理
                error_message = self._extract_error_message(response)
                
                if response.status_code == HTTP_UNAUTHORIZED:
                    raise AuthenticationError(error_message, response)
                elif response.status_code == HTTP_FORBIDDEN:
                    raise PermissionError(error_message, response)
                elif response.status_code == HTTP_NOT_FOUND:
                    raise ResourceNotFoundError(error_message, response)
                elif response.status_code == HTTP_TOO_MANY_REQUESTS:
                    # レートリミットエラー時はリトライ
                    retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                    if retry_count < self.max_retries:
                        time.sleep(retry_after)
                        retry_count += 1
                        continue
                    raise RateLimitError(error_message, response)
                elif response.status_code in (HTTP_BAD_REQUEST, HTTP_UNSUPPORTED_MEDIA_TYPE):
                    raise InvalidRequestError(error_message, response)
                elif response.status_code == HTTP_SERVER_ERROR:
                    raise APIError(error_message, response)
                elif response.status_code == HTTP_SERVICE_UNAVAILABLE:
                    # メンテナンス時はリトライ
                    if retry_count < self.max_retries:
                        time.sleep(self.retry_delay)
                        retry_count += 1
                        continue
                    raise ServiceUnavailableError(error_message, response)
                else:
                    raise APIError(f"予期しないステータスコード: {response.status_code}", response)
                
            except (requests.ConnectionError, requests.Timeout) as e:
                # 接続エラーやタイムアウトのリトライ
                if retry_count < self.max_retries:
                    time.sleep(self.retry_delay)
                    retry_count += 1
                    continue
                raise APIError(f"接続エラー: {str(e)}")
                
        # ここに到達することはないはず
        raise APIError("予期しないエラー: 最大リトライ回数を超えました")
    
    def _extract_error_message(self, response: requests.Response) -> str:
        """レスポンスからエラーメッセージを抽出"""
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                if 'error' in error_data:
                    return error_data['error']
                elif 'message' in error_data:
                    return error_data['message']
            return str(error_data)
        except (ValueError, KeyError):
            return response.text or f"HTTPエラー {response.status_code}"
            
    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GETリクエストを実行"""
        return self.request('GET', path, params=params)
        
    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POSTリクエストを実行"""
        return self.request('POST', path, json_data=data)
        
    def put(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """PUTリクエストを実行"""
        return self.request('PUT', path, json_data=data)
        
    def delete(self, path: str) -> Dict[str, Any]:
        """DELETEリクエストを実行"""
        return self.request('DELETE', path) 