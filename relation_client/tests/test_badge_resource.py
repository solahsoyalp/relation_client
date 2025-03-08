"""
バッジリソースのテスト

このモジュールは、BadgeResourceクラスのテストを提供します。
"""
import json
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