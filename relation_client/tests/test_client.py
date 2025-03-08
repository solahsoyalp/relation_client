"""
RelationClientのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

from relation_client import RelationClient
from relation_client.exceptions import AuthenticationError


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


if __name__ == '__main__':
    unittest.main() 