"""
CustomerResourceのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

from relation_client import RelationClient
from relation_client.models import Customer


class TestCustomerResource(unittest.TestCase):
    """CustomerResourceのテストクラス"""

    def setUp(self):
        """テスト前の準備"""
        self.client = RelationClient(
            access_token='test_token',
            subdomain='test'
        )
        self.customer_group_id = 1

    @patch.object(RelationClient, 'get')
    def test_search(self, mock_get):
        """search メソッドが正しく動作することを確認"""
        # モックの設定
        mock_get.return_value = [
            {
                'customer_id': 1,
                'name': 'テスト太郎',
                'gender_cd': 1,
                'emails': [{'email': 'test@example.com'}],
                'last_updated_at': '2023-01-01T00:00:00Z'
            }
        ]

        # テスト対象メソッドの実行
        result = self.client.customers.search(
            customer_group_id=self.customer_group_id,
            emails=['test@example.com']
        )

        # 検証
        mock_get.assert_called_once_with(
            'customer_groups/1/customers/search',
            params={
                'per_page': 10,
                'page': 1,
                'emails[]': ['test@example.com']
            }
        )
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Customer)
        self.assertEqual(result[0].customer_id, 1)
        self.assertEqual(result[0].emails[0].email, 'test@example.com')

    @patch.object(RelationClient, 'post')
    def test_create(self, mock_post):
        """create メソッドが正しく動作することを確認"""
        # モックの設定
        mock_post.return_value = {
            'customer_id': 1,
            'last_name': '大阪',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'osaka@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = self.client.customers.create(
            customer_group_id=self.customer_group_id,
            last_name='大阪',
            first_name='太郎',
            gender_cd=1,
            emails=[{'email': 'osaka@example.com'}],
            system_id1='EMP0001'
        )

        # 検証
        mock_post.assert_called_once_with(
            'customer_groups/1/customers/create',
            data={
                'last_name': '大阪',
                'first_name': '太郎',
                'gender_cd': 1,
                'emails': [{'email': 'osaka@example.com'}],
                'system_id1': 'EMP0001'
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.customer_id, 1)
        self.assertEqual(result.last_name, '大阪')
        self.assertEqual(result.first_name, '太郎')
        self.assertEqual(result.system_id1, 'EMP0001')

    @patch.object(RelationClient, 'get')
    def test_get_by_system_id1(self, mock_get):
        """get_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        mock_get.return_value = {
            'customer_id': 1,
            'last_name': '大阪',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'osaka@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = self.client.customers.get_by_system_id1(
            customer_group_id=self.customer_group_id,
            system_id1='EMP0001'
        )

        # 検証
        mock_get.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001'
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.customer_id, 1)
        self.assertEqual(result.system_id1, 'EMP0001')

    @patch.object(RelationClient, 'put')
    def test_update_by_system_id1(self, mock_put):
        """update_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        mock_put.return_value = {
            'customer_id': 1,
            'last_name': '東京',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'tokyo@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = self.client.customers.update_by_system_id1(
            customer_group_id=self.customer_group_id,
            system_id1='EMP0001',
            last_name='東京',
            emails=[{'email': 'tokyo@example.com'}]
        )

        # 検証
        mock_put.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001',
            data={
                'last_name': '東京',
                'emails': [{'email': 'tokyo@example.com'}]
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.last_name, '東京')
        self.assertEqual(result.emails[0].email, 'tokyo@example.com')

    @patch.object(RelationClient, 'delete')
    def test_delete_by_system_id1(self, mock_delete):
        """delete_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        mock_delete.return_value = {}

        # テスト対象メソッドの実行
        self.client.customers.delete_by_system_id1(
            customer_group_id=self.customer_group_id,
            system_id1='EMP0001'
        )

        # 検証
        mock_delete.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001'
        )


if __name__ == '__main__':
    unittest.main() 