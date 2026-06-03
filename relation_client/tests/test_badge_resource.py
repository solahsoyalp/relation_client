"""
バッジリソースのテスト

このモジュールは、BadgeResourceクラスのテストを提供します。
"""
import pytest
from unittest import mock

from relation_client.models import Badge
from relation_client.resources.badges import BadgeResource


class TestBadgeResource:
    """BadgeResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        # list メソッドのレスポンスを設定
        client.get.return_value = [
            {
                "badge_id": 1,
                "name": "VIP"
            },
            {
                "badge_id": 2,
                "name": "要注意"
            },
            {
                "badge_id": 3,
                "name": "新規顧客"
            }
        ]

        return client

    @pytest.fixture
    def badge_resource(self, client_mock):
        """BadgeResourceインスタンス"""
        return BadgeResource(client_mock)

    def test_list(self, badge_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = badge_resource.list(customer_group_id=123, per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('customer_groups/123/badges', params={'per_page': 50, 'page': 1})
        assert isinstance(result, list)
        assert len(result) == 3
        assert isinstance(result[0], Badge)

        # 1番目のバッジを検証
        assert result[0].badge_id == 1
        assert result[0].name == "VIP"

        # 2番目のバッジを検証
        assert result[1].badge_id == 2
        assert result[1].name == "要注意"

        # 3番目のバッジを検証
        assert result[2].badge_id == 3
        assert result[2].name == "新規顧客"

    def test_list_with_default_params(self, badge_resource, client_mock):
        """list()メソッドのデフォルトパラメータのテスト"""
        # 実行
        result = badge_resource.list(customer_group_id=123)

        # 検証
        client_mock.get.assert_called_once_with('customer_groups/123/badges', params={})
        assert isinstance(result, list)
        assert len(result) == 3

    def test_list_non_list_response(self, badge_resource, client_mock):
        """list()メソッドがリスト以外のレスポンスで空リストを返すテスト"""
        client_mock.get.return_value = {"error": "not found"}

        result = badge_resource.list(customer_group_id=123)

        assert result == []

    def test_iter_all_multi_page(self, badge_resource, client_mock):
        """iter_all()メソッドの複数ページのテスト"""
        # フルページ(per_page=2)の後に短いページ(1件)を返すことで停止させる
        full_page = [
            {"badge_id": 1, "name": "VIP"},
            {"badge_id": 2, "name": "要注意"},
        ]
        short_page = [
            {"badge_id": 3, "name": "新規顧客"},
        ]
        client_mock.get.side_effect = [full_page, short_page]

        result = list(badge_resource.iter_all(customer_group_id=123, per_page=2))

        assert len(result) == 3
        assert all(isinstance(badge, Badge) for badge in result)
        assert [badge.badge_id for badge in result] == [1, 2, 3]
        assert client_mock.get.call_count == 2
        client_mock.get.assert_any_call('customer_groups/123/badges', params={'per_page': 2, 'page': 1})
        client_mock.get.assert_any_call('customer_groups/123/badges', params={'per_page': 2, 'page': 2})

    def test_iter_all_single_short_page(self, badge_resource, client_mock):
        """iter_all()メソッドが1ページ目で停止するテスト(デフォルトper_page)"""
        # デフォルトの停止判定件数(30)未満なので1ページで停止する
        client_mock.get.return_value = [
            {"badge_id": 1, "name": "VIP"},
        ]

        result = list(badge_resource.iter_all(customer_group_id=123))

        assert len(result) == 1
        assert client_mock.get.call_count == 1
        client_mock.get.assert_called_once_with('customer_groups/123/badges', params={'page': 1})

    def test_iter_all_empty(self, badge_resource, client_mock):
        """iter_all()メソッドが0件のとき即停止するテスト"""
        client_mock.get.return_value = []

        result = list(badge_resource.iter_all(customer_group_id=123, per_page=10))

        assert result == []
        assert client_mock.get.call_count == 1
