"""
MailAccountResourceクラスのテスト

このモジュールは、MailAccountResourceクラスの各メソッドをテストします。
"""
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

    def test_list_non_list_response(self, mail_account_resource, client_mock):
        """list()メソッドがリスト以外のレスポンスで空リストを返すテスト"""
        client_mock.get.return_value = {"error": "not found"}

        result = mail_account_resource.list(message_box_id=123)

        assert result == []

    def test_iter_all_multi_page(self, mail_account_resource, client_mock):
        """iter_all()メソッドの複数ページのテスト"""
        # フルページ(per_page=2)の後に短いページ(1件)を返すことで停止させる
        full_page = [
            {"mail_account_id": 1, "name": "アカウント1", "email": "a1@example.com"},
            {"mail_account_id": 2, "name": "アカウント2", "email": "a2@example.com"},
        ]
        short_page = [
            {"mail_account_id": 3, "name": "アカウント3", "email": "a3@example.com"},
        ]
        client_mock.get.side_effect = [full_page, short_page]

        result = list(mail_account_resource.iter_all(message_box_id=123, per_page=2))

        assert len(result) == 3
        assert all(isinstance(account, MailAccount) for account in result)
        assert [account.mail_account_id for account in result] == [1, 2, 3]
        assert client_mock.get.call_count == 2
        client_mock.get.assert_any_call('123/mail_accounts', params={'per_page': 2, 'page': 1})
        client_mock.get.assert_any_call('123/mail_accounts', params={'per_page': 2, 'page': 2})

    def test_iter_all_single_short_page(self, mail_account_resource, client_mock):
        """iter_all()メソッドが1ページ目で停止するテスト(デフォルトper_page)"""
        # デフォルトの停止判定件数(30)未満なので1ページで停止する
        client_mock.get.return_value = [
            {"mail_account_id": 1, "name": "アカウント1", "email": "a1@example.com"},
        ]

        result = list(mail_account_resource.iter_all(message_box_id=123))

        assert len(result) == 1
        assert client_mock.get.call_count == 1
        client_mock.get.assert_called_once_with('123/mail_accounts', params={'page': 1})

    def test_iter_all_empty(self, mail_account_resource, client_mock):
        """iter_all()メソッドが0件のとき即停止するテスト"""
        client_mock.get.return_value = []

        result = list(mail_account_resource.iter_all(message_box_id=123, per_page=10))

        assert result == []
        assert client_mock.get.call_count == 1
