"""
RelationClientのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

import requests

from relation_client import RelationClient
from relation_client.exceptions import (
    AuthenticationError, APIError, RelationPermissionError, PermissionError,
    ResourceNotFoundError, RateLimitError, InvalidRequestError,
    ServiceUnavailableError
)


class TestRelationClient(unittest.TestCase):
    """RelationClientのテストクラス"""

    def setUp(self):
        """テスト前の準備"""
        self.access_token = 'test_token'
        self.subdomain = 'test'
        self.client = RelationClient(
            access_token=self.access_token,
            subdomain=self.subdomain
        )

    def test_init(self):
        """初期化が正しく行われることを確認"""
        self.assertEqual(self.client.access_token, self.access_token)
        self.assertEqual(self.client.subdomain, self.subdomain)
        self.assertEqual(self.client.api_version, 'v2')
        self.assertEqual(self.client._base_url, 'https://test.relationapp.jp/api/v2')

    def test_valid_subdomains_accepted(self):
        """正常なサブドメインは従来通り利用できることを確認"""
        for sub in ('test', 'my-company', 'abc123', 'a', '0', 'a' * 63):
            client = RelationClient(access_token='t', subdomain=sub)
            self.assertEqual(client.subdomain, sub)
            self.assertEqual(client._base_url, f'https://{sub}.relationapp.jp/api/v2')

    def test_invalid_subdomain_rejected(self):
        """ホスト名を変形し得るサブドメインが拒否されることを確認"""
        invalid_values = [
            'attacker.example/path',  # '/' でパス／ホストを変形
            'evil.example',           # '.' で別ホストを指定
            'a?b',                    # クエリ注入
            'user@host',              # 認証情報部の注入
            'sub domain',             # 空白
            '-leading',               # 先頭ハイフン
            'trailing-',              # 末尾ハイフン
            'UPPER',                  # 大文字（小文字のみ許可）
            '',                       # 空文字
            'a' * 64,                 # 64文字（上限超過）
        ]
        for value in invalid_values:
            with self.assertRaises(ValueError):
                RelationClient(access_token='t', subdomain=value)

    @patch('requests.Session.request')
    def test_get_success(self, mock_request):
        """GETリクエストが成功することを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_request.return_value = mock_response

        # テスト対象メソッドの実行
        result = self.client.get('test_path')

        # 検証
        mock_request.assert_called_once_with(
            method='GET',
            url='https://test.relationapp.jp/api/v2/test_path',
            headers={
                'Authorization': 'Bearer test_token',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            params=None,
            data=None,
            json=None,
            timeout=30
        )
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.Session.request')
    def test_post_success(self, mock_request):
        """POSTリクエストが成功することを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1}
        mock_request.return_value = mock_response

        # テスト対象メソッドの実行
        data = {'name': 'test'}
        result = self.client.post('test_path', data)

        # 検証
        mock_request.assert_called_once_with(
            method='POST',
            url='https://test.relationapp.jp/api/v2/test_path',
            headers={
                'Authorization': 'Bearer test_token',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            params=None,
            data=None,
            json=data,
            timeout=30
        )
        self.assertEqual(result, {'id': 1})

    @patch('requests.Session.request')
    def test_authentication_error(self, mock_request):
        """認証エラーが発生した場合に例外が投げられることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_request.return_value = mock_response

        # 例外が発生することを確認
        with self.assertRaises(AuthenticationError):
            self.client.get('test_path')

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_post_not_retried_on_connection_error(self, mock_request, mock_sleep):
        """POSTは接続エラー時にリトライされず、APIErrorが送出されることを確認"""
        # 接続エラーを常に発生させる
        mock_request.side_effect = requests.ConnectionError("boom")

        # 非冪等なPOSTはリトライされず即座にAPIErrorになる
        with self.assertRaises(APIError):
            self.client.post('test_path', {'name': 'test'})

        # session.request は1回しか呼ばれない (リトライなし)
        self.assertEqual(mock_request.call_count, 1)

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_get_retried_on_connection_error(self, mock_request, mock_sleep):
        """GETは接続エラー時にmax_retries回までリトライされることを確認"""
        # 接続エラーを常に発生させる
        mock_request.side_effect = requests.ConnectionError("boom")

        # 冪等なGETはリトライされ、最終的にAPIErrorになる
        with self.assertRaises(APIError):
            self.client.get('test_path')

        # 初回 + max_retries 回のリトライで合計 max_retries + 1 回呼ばれる
        self.assertEqual(mock_request.call_count, self.client.max_retries + 1)

    def test_permission_error_backward_compatible_alias(self):
        """旧名 PermissionError が RelationPermissionError と同一クラスであることを確認"""
        # エイリアスが同一クラスを指している
        self.assertIs(PermissionError, RelationPermissionError)

    @patch('requests.Session.request')
    def test_permission_error_caught_by_old_name(self, mock_request):
        """HTTP 403 が旧名 PermissionError でも捕捉できることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {'error': 'Forbidden'}
        mock_request.return_value = mock_response

        # 旧名 PermissionError で捕捉できる
        with self.assertRaises(PermissionError):
            self.client.get('test_path')

    @patch('requests.Session.request')
    def test_last_rate_limit_populated(self, mock_request):
        """レスポンスヘッダから last_rate_limit が設定されることを確認"""
        # モックの設定（レートリミットヘッダを含む）
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_response.headers = {
            'X-RateLimit-Limit': '60',
            'X-RateLimit-Remaining': '59',
            'X-RateLimit-Reset': '1700000000',
        }
        mock_request.return_value = mock_response

        self.client.get('test_path')

        # ヘッダが整数として解析されている
        self.assertEqual(
            self.client.last_rate_limit,
            {'limit': 60, 'remaining': 59, 'reset': 1700000000}
        )

    @patch('requests.Session.request')
    def test_last_rate_limit_missing_headers(self, mock_request):
        """ヘッダが欠落／非整数の場合に None になることを確認"""
        # モックの設定（ヘッダなし・非整数を含む）
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_response.headers = {'X-RateLimit-Limit': 'not-a-number'}
        mock_request.return_value = mock_response

        self.client.get('test_path')

        # 欠落・非整数のヘッダは None になる
        self.assertEqual(
            self.client.last_rate_limit,
            {'limit': None, 'remaining': None, 'reset': None}
        )

    def test_context_manager_closes_session(self):
        """コンテキストマネージャー終了時にセッションがクローズされることを確認"""
        # セッションの close をモック
        self.client._session.close = MagicMock()

        with self.client as c:
            # __enter__ は自身を返す
            self.assertIs(c, self.client)

        # __exit__ で close が呼ばれている
        self.client._session.close.assert_called_once()

    def test_close_closes_session(self):
        """close() がセッションをクローズすることを確認"""
        # セッションの close をモック
        self.client._session.close = MagicMock()

        self.client.close()

        self.client._session.close.assert_called_once()

    @patch('requests.Session.request')
    def test_resource_not_found_error(self, mock_request):
        """HTTP 404 で ResourceNotFoundError が送出されることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'Not Found'}
        mock_request.return_value = mock_response

        # 404 は ResourceNotFoundError になる
        with self.assertRaises(ResourceNotFoundError):
            self.client.get('test_path')

    @patch('requests.Session.request')
    def test_invalid_request_error_400(self, mock_request):
        """HTTP 400 で InvalidRequestError が送出されることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}
        mock_request.return_value = mock_response

        # 400 は InvalidRequestError になる
        with self.assertRaises(InvalidRequestError):
            self.client.get('test_path')

    @patch('requests.Session.request')
    def test_invalid_request_error_415(self, mock_request):
        """HTTP 415 で InvalidRequestError が送出されることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 415
        mock_response.json.return_value = {'error': 'Unsupported Media Type'}
        mock_request.return_value = mock_response

        # 415 は InvalidRequestError になる
        with self.assertRaises(InvalidRequestError):
            self.client.get('test_path')

    @patch('requests.Session.request')
    def test_server_error_500(self, mock_request):
        """HTTP 500 で APIError が送出されることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_request.return_value = mock_response

        # 500 は APIError になる
        with self.assertRaises(APIError):
            self.client.get('test_path')

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_rate_limit_retried_then_success(self, mock_request, mock_sleep):
        """HTTP 429 後にリトライして成功することを確認"""
        # 1回目は429、2回目は成功を返す
        rate_limited = MagicMock()
        rate_limited.status_code = 429
        rate_limited.headers = {'Retry-After': '2'}
        rate_limited.json.return_value = {'error': 'Too Many Requests'}

        success = MagicMock()
        success.status_code = 200
        success.json.return_value = {'data': 'ok'}
        mock_request.side_effect = [rate_limited, success]

        result = self.client.get('test_path')

        # Retry-After に従ってスリープし、最終的に成功結果を返す
        mock_sleep.assert_called_once_with(2)
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(result, {'data': 'ok'})

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_rate_limit_exhausted_raises(self, mock_request, mock_sleep):
        """HTTP 429 がリトライ上限を超えると RateLimitError になることを確認"""
        # 常に429を返す
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '1'}
        mock_response.json.return_value = {'error': 'Too Many Requests'}
        mock_request.return_value = mock_response

        # リトライ上限を超えると RateLimitError になる
        with self.assertRaises(RateLimitError):
            self.client.get('test_path')

        # 初回 + max_retries 回のリトライで合計 max_retries + 1 回呼ばれる
        self.assertEqual(mock_request.call_count, self.client.max_retries + 1)
        self.assertEqual(mock_sleep.call_count, self.client.max_retries)

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_service_unavailable_retried_then_success(self, mock_request, mock_sleep):
        """HTTP 503 後にリトライして成功することを確認"""
        # 1回目は503、2回目は成功を返す
        unavailable = MagicMock()
        unavailable.status_code = 503
        unavailable.json.return_value = {'error': 'Service Unavailable'}

        success = MagicMock()
        success.status_code = 200
        success.json.return_value = {'data': 'ok'}
        mock_request.side_effect = [unavailable, success]

        result = self.client.get('test_path')

        # retry_delay に従ってスリープし、最終的に成功結果を返す
        mock_sleep.assert_called_once_with(self.client.retry_delay)
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(result, {'data': 'ok'})

    @patch('time.sleep', return_value=None)
    @patch('requests.Session.request')
    def test_service_unavailable_exhausted_raises(self, mock_request, mock_sleep):
        """HTTP 503 がリトライ上限を超えると ServiceUnavailableError になることを確認"""
        # 常に503を返す
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.json.return_value = {'error': 'Service Unavailable'}
        mock_request.return_value = mock_response

        # リトライ上限を超えると ServiceUnavailableError になる
        with self.assertRaises(ServiceUnavailableError):
            self.client.get('test_path')

        # 初回 + max_retries 回のリトライで合計 max_retries + 1 回呼ばれる
        self.assertEqual(mock_request.call_count, self.client.max_retries + 1)
        self.assertEqual(mock_sleep.call_count, self.client.max_retries)

    @patch('requests.Session.request')
    def test_unexpected_status_code_raises_api_error(self, mock_request):
        """想定外のステータスコードで APIError が送出されることを確認"""
        # モックの設定（マッピングのない 418 を返す）
        mock_response = MagicMock()
        mock_response.status_code = 418
        mock_response.json.return_value = {'error': "I'm a teapot"}
        mock_request.return_value = mock_response

        # 予期しないステータスコードのメッセージを持つ APIError になる
        with self.assertRaises(APIError) as ctx:
            self.client.get('test_path')

        self.assertIn('予期しないステータスコード', ctx.exception.message)
        self.assertIn('418', ctx.exception.message)

    @patch('requests.Session.request')
    def test_error_message_from_json_error_key(self, mock_request):
        """JSONボディの error キーが message に反映されることを確認"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'エラーメッセージ'}
        mock_request.return_value = mock_response

        # error キーの値が例外の message になる
        with self.assertRaises(InvalidRequestError) as ctx:
            self.client.get('test_path')

        self.assertEqual(ctx.exception.message, 'エラーメッセージ')

    @patch('requests.Session.request')
    def test_error_message_from_json_message_key(self, mock_request):
        """JSONボディの message キーが message に反映されることを確認"""
        # モックの設定（error キーは無く message キーを持つ）
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'message': 'メッセージキー'}
        mock_request.return_value = mock_response

        # message キーの値が例外の message になる
        with self.assertRaises(InvalidRequestError) as ctx:
            self.client.get('test_path')

        self.assertEqual(ctx.exception.message, 'メッセージキー')

    @patch('requests.Session.request')
    def test_error_message_from_non_json_text(self, mock_request):
        """非JSONのテキストボディが message に反映されることを確認"""
        # モックの設定（json() は ValueError、text を持つ）
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError('No JSON')
        mock_response.text = 'プレーンテキストエラー'
        mock_request.return_value = mock_response

        # 非JSONの場合は text の値が例外の message になる
        with self.assertRaises(InvalidRequestError) as ctx:
            self.client.get('test_path')

        self.assertEqual(ctx.exception.message, 'プレーンテキストエラー')

    @patch('requests.Session.request')
    def test_success_empty_body_returns_empty_dict(self, mock_request):
        """成功レスポンスのボディが空の場合に空辞書が返ることを確認"""
        # モックの設定（content が空）
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = b''
        mock_request.return_value = mock_response

        result = self.client.delete('test_path')

        # 空ボディは空辞書を返す
        self.assertEqual(result, {})

    @patch('requests.Session.request')
    def test_success_non_json_body_returns_data_wrapper(self, mock_request):
        """成功レスポンスが非JSONの場合に data でラップされることを確認"""
        # モックの設定（content はあるが json() は ValueError）
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'plain text'
        mock_response.json.side_effect = ValueError('No JSON')
        mock_response.text = 'plain text'
        mock_request.return_value = mock_response

        result = self.client.get('test_path')

        # 非JSONの成功ボディは {"data": <text>} で返る
        self.assertEqual(result, {'data': 'plain text'})


if __name__ == '__main__':
    unittest.main()
