"""
CustomerGroupResourceのテスト
"""

import unittest
from unittest.mock import patch

from relation_client import RelationClient
from relation_client.models import CustomerGroup


class TestCustomerGroupResource(unittest.TestCase):
    """CustomerGroupResourceのテストクラス"""

    def setUp(self):
        """テスト前の準備"""
        self.client = RelationClient(
            access_token='test_token',
            subdomain='test'
        )

    @patch.object(RelationClient, 'get')
    def test_list(self, mock_get):
        """list メソッドが正しく動作することを確認"""
        # モックの設定
        mock_get.return_value = [
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
        result = self.client.customer_groups.list()

        # 検証
        mock_get.assert_called_once_with('customer_groups')
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], CustomerGroup)
        self.assertEqual(result[0].customer_group_id, 1)
        self.assertEqual(result[0].name, 'アドレス帳1')
        self.assertEqual(result[0].message_box_ids, [1])
        self.assertIsInstance(result[1], CustomerGroup)
        self.assertEqual(result[1].customer_group_id, 2)
        self.assertEqual(result[1].name, 'アドレス帳2')
        self.assertEqual(result[1].message_box_ids, [1, 2])

    @patch.object(RelationClient, 'get')
    def test_list_empty(self, mock_get):
        """list メソッドが空レスポンスで空リストを返すことを確認"""
        # モックの設定
        mock_get.return_value = []

        # テスト対象メソッドの実行
        result = self.client.customer_groups.list()

        # 検証
        mock_get.assert_called_once_with('customer_groups')
        self.assertEqual(result, [])

    @patch.object(RelationClient, 'get')
    def test_list_default_message_box_ids(self, mock_get):
        """message_box_ids が欠落している場合に空リストになることを確認"""
        # モックの設定（message_box_ids を省略）
        mock_get.return_value = [
            {
                'customer_group_id': 10,
                'name': 'アドレス帳X',
            }
        ]

        # テスト対象メソッドの実行
        result = self.client.customer_groups.list()

        # 検証
        mock_get.assert_called_once_with('customer_groups')
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], CustomerGroup)
        self.assertEqual(result[0].customer_group_id, 10)
        self.assertEqual(result[0].name, 'アドレス帳X')
        self.assertEqual(result[0].message_box_ids, [])
        self.assertIsNone(result[0].last_updated_at)


if __name__ == '__main__':
    unittest.main()
