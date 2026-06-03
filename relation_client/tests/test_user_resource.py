"""
ユーザーリソースのテスト

このモジュールは、UserResourceクラスのテストを提供します。
"""
import pytest
from unittest import mock

from relation_client.models import User
from relation_client.resources.users import UserResource


class TestUserResource:
    """UserResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        client.get.return_value = [
            {
                "mention_name": "taro",
                "status_cd": "available",
                "first_name": "太郎",
                "last_name": "大阪",
                "department_name": "本社",
                "employee_no": "100001",
                "email": "abc@example.com",
                "is_tenant_admin": True,
                "is_otp_required": False,
                "last_page_loaded_at": "2024-01-09T05:18:36Z"
            },
            {
                "mention_name": "hanako",
                "status_cd": "available",
                "first_name": "花子",
                "last_name": "梅田",
                "department_name": "本社",
                "employee_no": "100002",
                "email": "efg@example.com",
                "is_tenant_admin": False,
                "is_otp_required": True,
                "last_page_loaded_at": "2024-01-09T05:20:36Z"
            }
        ]
        return client

    @pytest.fixture
    def user_resource(self, client_mock):
        """UserResourceインスタンス"""
        return UserResource(client_mock)

    def test_list(self, user_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = user_resource.list(per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('users', params={'per_page': 50, 'page': 1})
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], User)

        # 1人目のユーザー情報を検証
        assert result[0].mention_name == "taro"
        assert result[0].status_cd == "available"
        assert result[0].first_name == "太郎"
        assert result[0].last_name == "大阪"
        assert result[0].department_name == "本社"
        assert result[0].employee_no == "100001"
        assert result[0].email == "abc@example.com"
        assert result[0].is_tenant_admin is True
        assert result[0].is_otp_required is False
        assert result[0].last_page_loaded_at.isoformat().replace('+00:00', 'Z') == "2024-01-09T05:18:36Z"

        # 2人目のユーザー情報を検証
        assert result[1].mention_name == "hanako"
        assert result[1].status_cd == "available"
        assert result[1].first_name == "花子"
        assert result[1].last_name == "梅田"
        assert result[1].department_name == "本社"
        assert result[1].employee_no == "100002"
        assert result[1].email == "efg@example.com"
        assert result[1].is_tenant_admin is False
        assert result[1].is_otp_required is True
        assert result[1].last_page_loaded_at.isoformat().replace('+00:00', 'Z') == "2024-01-09T05:20:36Z"

    def test_list_with_default_params(self, user_resource, client_mock):
        """list()メソッドのデフォルトパラメータのテスト"""
        # 実行
        result = user_resource.list()

        # 検証
        client_mock.get.assert_called_once_with('users', params={})
        assert isinstance(result, list)
        assert len(result) == 2

    def test_iter_all_multi_page(self, user_resource, client_mock):
        """iter_all()メソッドの複数ページのテスト"""
        # フルページ(per_page=2)の後に短いページ(1件)を返すことで停止させる
        full_page = [
            {"mention_name": "u1", "email": "u1@example.com"},
            {"mention_name": "u2", "email": "u2@example.com"},
        ]
        short_page = [
            {"mention_name": "u3", "email": "u3@example.com"},
        ]
        client_mock.get.side_effect = [full_page, short_page]

        result = list(user_resource.iter_all(per_page=2))

        assert len(result) == 3
        assert all(isinstance(user, User) for user in result)
        assert [user.mention_name for user in result] == ["u1", "u2", "u3"]
        assert client_mock.get.call_count == 2
        client_mock.get.assert_any_call('users', params={'per_page': 2, 'page': 1})
        client_mock.get.assert_any_call('users', params={'per_page': 2, 'page': 2})

    def test_iter_all_single_short_page(self, user_resource, client_mock):
        """iter_all()メソッドが1ページ目で停止するテスト(デフォルトper_page)"""
        # デフォルトの停止判定件数(30)未満なので1ページで停止する
        client_mock.get.return_value = [
            {"mention_name": "only", "email": "only@example.com"},
        ]

        result = list(user_resource.iter_all())

        assert len(result) == 1
        assert client_mock.get.call_count == 1
        client_mock.get.assert_called_once_with('users', params={'page': 1})

    def test_iter_all_empty(self, user_resource, client_mock):
        """iter_all()メソッドが0件のとき即停止するテスト"""
        client_mock.get.return_value = []

        result = list(user_resource.iter_all(per_page=10))

        assert result == []
        assert client_mock.get.call_count == 1
