"""
MailAccountResourceクラスのテスト

このモジュールは、MailAccountResourceクラスの各メソッドをテストします。
"""
import json
import pytest
from unittest import mock

from relation_client.models import MailAccount
from relation_client.resources.mail_accounts import MailAccountResource

class TestMailAccountResource:
    """MailAccountResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        # list メソッドのレスポンスを設定
        client.get.return_value = [
            {
                "mail_account_id": 1,
                "name": "カスタマーサポートセンター",
                "email": "info1@example.com"
            },
            {
                "mail_account_id": 2,
                "name": "株式会社xxx",
                "email": "info2@example.com"
            }
        ]
        
        return client

    @pytest.fixture
    def mail_account_resource(self, client_mock):
        """MailAccountResourceインスタンス"""
        return MailAccountResource(client_mock)

    def test_list(self, mail_account_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = mail_account_resource.list(message_box_id=123, per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('123/mail_accounts', params={'per_page': 50, 'page': 1})
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], MailAccount)
        
        # 1番目のメールアカウントを検証
        assert result[0].mail_account_id == 1
        assert result[0].name == "カスタマーサポートセンター"
        assert result[0].email == "info1@example.com"
        
        # 2番目のメールアカウントを検証
        assert result[1].mail_account_id == 2
        assert result[1].name == "株式会社xxx"
        assert result[1].email == "info2@example.com"

    def test_list_with_default_params(self, mail_account_resource, client_mock):
        """list()メソッドのデフォルトパラメータのテスト"""
        # 実行
        result = mail_account_resource.list(message_box_id=123)

        # 検証
        client_mock.get.assert_called_once_with('123/mail_accounts', params={})
        assert isinstance(result, list)
        assert len(result) == 2
