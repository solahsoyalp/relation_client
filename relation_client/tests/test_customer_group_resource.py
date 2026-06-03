"""
CustomerGroupResourceのテスト
"""

import pytest

from relation_client.models import CustomerGroup
from relation_client.resources.customer_groups import CustomerGroupResource


class TestCustomerGroupResource:
    """CustomerGroupResourceのテストクラス"""

    @pytest.fixture
    def customer_group_resource(self, client_mock):
        """CustomerGroupResourceインスタンス"""
        return CustomerGroupResource(client_mock)

    def test_list(self, customer_group_resource, client_mock):
        """list メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.get.return_value = [
            {
                'customer_group_id': 1,
                'name': 'アドレス帳1',
                'message_box_ids': [1],
                'last_updated_at': '2023-01-01T00:00:00Z'
            },
            {
                'customer_group_id': 2,
                'name': 'アドレス帳2',
                'message_box_ids': [1, 2],
                'last_updated_at': '2023-01-02T00:00:00Z'
            }
        ]

        # テスト対象メソッドの実行
        result = customer_group_resource.list()

        # 検証
        client_mock.get.assert_called_once_with('customer_groups')
        assert len(result) == 2
        assert isinstance(result[0], CustomerGroup)
        assert result[0].customer_group_id == 1
        assert result[0].name == 'アドレス帳1'
        assert result[0].message_box_ids == [1]
        assert isinstance(result[1], CustomerGroup)
        assert result[1].customer_group_id == 2
        assert result[1].name == 'アドレス帳2'
        assert result[1].message_box_ids == [1, 2]

    def test_list_empty(self, customer_group_resource, client_mock):
        """list メソッドが空レスポンスで空リストを返すことを確認"""
        # モックの設定
        client_mock.get.return_value = []

        # テスト対象メソッドの実行
        result = customer_group_resource.list()

        # 検証
        client_mock.get.assert_called_once_with('customer_groups')
        assert result == []

    def test_list_default_message_box_ids(self, customer_group_resource, client_mock):
        """message_box_ids が欠落している場合に空リストになることを確認"""
        # モックの設定（message_box_ids を省略）
        client_mock.get.return_value = [
            {
                'customer_group_id': 10,
                'name': 'アドレス帳X',
            }
        ]

        # テスト対象メソッドの実行
        result = customer_group_resource.list()

        # 検証
        client_mock.get.assert_called_once_with('customer_groups')
        assert len(result) == 1
        assert isinstance(result[0], CustomerGroup)
        assert result[0].customer_group_id == 10
        assert result[0].name == 'アドレス帳X'
        assert result[0].message_box_ids == []
        assert result[0].last_updated_at is None
