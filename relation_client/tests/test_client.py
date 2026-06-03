"""
RelationClientのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

import requests

from relation_client import RelationClient
from relation_client.exceptions import AuthenticationError, APIError


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


if __name__ == '__main__':
    unittest.main() 