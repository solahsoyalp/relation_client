"""
CustomerGroupResourceのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

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


if __name__ == '__main__':
    unittest.main() 