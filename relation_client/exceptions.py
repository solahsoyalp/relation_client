"""
Re:lation API例外モジュール

このモジュールは、Re:lation APIとの通信中に発生する可能性のある例外を定義します。
"""


class RelationError(Exception):
    """Re:lation APIエラーの基本例外クラス"""

    def __init__(self, message=None, response=None):
        self.message = message
        self.response = response
        super().__init__(self.message)


class AuthenticationError(RelationError):
    """認証エラー (HTTP 401)"""
    pass


class PermissionError(RelationError):
    """権限エラー (HTTP 403)"""
    pass


class ResourceNotFoundError(RelationError):
    """リソースが見つからないエラー (HTTP 404)"""
    pass


class RateLimitError(RelationError):
    """レートリミットエラー (HTTP 429)"""
    pass


class InvalidRequestError(RelationError):
    """無効なリクエストエラー (HTTP 400, 415)"""
    pass


class APIError(RelationError):
    """APIエラー (HTTP 500)"""
    pass


class ServiceUnavailableError(RelationError):
    """サービス利用不可エラー (HTTP 503)"""
    pass 