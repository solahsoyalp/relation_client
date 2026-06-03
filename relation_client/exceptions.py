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


class RelationPermissionError(RelationError):
    """権限エラー (HTTP 403)"""


# 後方互換性のためのエイリアス（旧名 PermissionError を維持）
PermissionError = RelationPermissionError


class ResourceNotFoundError(RelationError):
    """リソースが見つからないエラー (HTTP 404)"""


class RateLimitError(RelationError):
    """レートリミットエラー (HTTP 429)"""


class InvalidRequestError(RelationError):
    """無効なリクエストエラー (HTTP 400, 415)"""


class APIError(RelationError):
    """APIエラー (HTTP 500)"""


class ServiceUnavailableError(RelationError):
    """サービス利用不可エラー (HTTP 503)"""
