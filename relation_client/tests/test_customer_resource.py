"""
CustomerResourceのテスト
"""

import unittest
from unittest.mock import patch

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

    @patch.object(RelationClient, 'get')
    def test_iter_all(self, mock_get):
        """iter_all メソッドが全ページを透過的に取得することを確認"""
        per_page = 3

        def make_customer(customer_id):
            return {
                'customer_id': customer_id,
                'name': f'テスト{customer_id}',
                'gender_cd': 1,
                'emails': [{'email': f'test{customer_id}@example.com'}],
                'last_updated_at': '2023-01-01T00:00:00Z'
            }

        # 1ページ目: per_page と同数（フルページ） / 2ページ目: per_page 未満（最終ページ）
        page1 = [make_customer(i) for i in range(1, per_page + 1)]
        page2 = [make_customer(per_page + 1)]
        mock_get.side_effect = [page1, page2]

        result = list(self.client.customers.iter_all(
            customer_group_id=self.customer_group_id,
            per_page=per_page
        ))

        # 全ページの全件が連結して得られる
        self.assertEqual(len(result), per_page + 1)
        self.assertTrue(all(isinstance(c, Customer) for c in result))
        self.assertEqual([c.customer_id for c in result], [1, 2, 3, 4])

        # 2ページ呼び出した時点で停止していること
        self.assertEqual(mock_get.call_count, 2)
        first_call = mock_get.call_args_list[0]
        second_call = mock_get.call_args_list[1]
        self.assertEqual(first_call.kwargs['params']['page'], 1)
        self.assertEqual(first_call.kwargs['params']['per_page'], per_page)
        self.assertEqual(second_call.kwargs['params']['page'], 2)

    @patch.object(RelationClient, 'get')
    def test_iter_all_stops_on_empty_page(self, mock_get):
        """ちょうど満杯のページの後、空ページで停止することを確認"""
        per_page = 2

        def make_customer(customer_id):
            return {
                'customer_id': customer_id,
                'name': f'テスト{customer_id}',
                'gender_cd': 1,
                'emails': [{'email': f'test{customer_id}@example.com'}],
                'last_updated_at': '2023-01-01T00:00:00Z'
            }

        # フルページ -> フルページ -> 空ページ
        mock_get.side_effect = [
            [make_customer(1), make_customer(2)],
            [make_customer(3), make_customer(4)],
            []
        ]

        result = list(self.client.customers.iter_all(
            customer_group_id=self.customer_group_id,
            per_page=per_page
        ))

        self.assertEqual([c.customer_id for c in result], [1, 2, 3, 4])
        self.assertEqual(mock_get.call_count, 3)

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

    @patch.object(RelationClient, 'get')
    def test_get_by_email_encodes_path_segment(self, mock_get):
        """email がパスセグメントとして安全にエンコードされることを確認"""
        mock_get.return_value = {'customer_id': 1}

        # '?' でクエリ注入を試みる値
        self.client.customers.get_by_email(
            customer_group_id=self.customer_group_id,
            email='a@example.com?per_page=999'
        )

        # '@' '?' '=' がすべてパーセントエンコードされ、パスが変形されないこと
        mock_get.assert_called_once_with(
            'customer_groups/1/customers/email/a%40example.com%3Fper_page%3D999'
        )

    @patch.object(RelationClient, 'get')
    def test_get_by_system_id1_encodes_path_segment(self, mock_get):
        """system_id1 の '/' や日本語がエンコードされることを確認"""
        mock_get.return_value = {'customer_id': 1}

        self.client.customers.get_by_system_id1(
            customer_group_id=self.customer_group_id,
            system_id1='a/b 太郎'
        )

        # '/' → %2F, 空白 → %20, 日本語 → UTF-8 パーセントエンコード
        mock_get.assert_called_once_with(
            'customer_groups/1/customers/system_id1/a%2Fb%20%E5%A4%AA%E9%83%8E'
        )

    @patch.object(RelationClient, 'get')
    def test_search_with_all_optional_params(self, mock_get):
        """search が全オプションパラメータのブランチを設定することを確認"""
        mock_get.return_value = []

        self.client.customers.search(
            customer_group_id=self.customer_group_id,
            customer_ids=[1, 2],
            gender_cds=[1, 2],
            system_id1s=['EMP0001'],
            default_assignees=['@taro'],
            emails=['test@example.com'],
            tels=['09000000000'],
            badge_ids=[10, 20],
            per_page=50,
            page=3
        )

        mock_get.assert_called_once_with(
            'customer_groups/1/customers/search',
            params={
                'per_page': 50,
                'page': 3,
                'customer_ids[]': [1, 2],
                'gender_cds[]': [1, 2],
                'system_id1s[]': ['EMP0001'],
                'default_assignees[]': ['@taro'],
                'emails[]': ['test@example.com'],
                'tels[]': ['09000000000'],
                'badge_ids[]': [10, 20],
            }
        )

    @patch.object(RelationClient, 'post')
    def test_create_with_all_optional_fields(self, mock_post):
        """create が全オプションフィールドのブランチを設定することを確認"""
        mock_post.return_value = {
            'customer_id': 5,
            'last_name': '大阪',
            'first_name': '太郎',
            'gender_cd': 1,
            'system_id1': 'EMP0005',
        }

        emails = [{'email': 'osaka@example.com'}]
        archived_emails = [{'email': 'old@example.com'}]
        tels = [{'tel': '09000000000'}]
        archived_tels = [{'tel': '08000000000'}]

        result = self.client.customers.create(
            customer_group_id=self.customer_group_id,
            last_name='大阪',
            first_name='太郎',
            last_name_kana='オオサカ',
            first_name_kana='タロウ',
            company_name='テスト株式会社',
            title='部長',
            url='https://example.com',
            gender_cd=1,
            default_assignee='@taro',
            emails=emails,
            archived_emails=archived_emails,
            tels=tels,
            archived_tels=archived_tels,
            badge_ids=[1, 2],
            system_id1='EMP0005',
        )

        mock_post.assert_called_once_with(
            'customer_groups/1/customers/create',
            data={
                'last_name': '大阪',
                'first_name': '太郎',
                'last_name_kana': 'オオサカ',
                'first_name_kana': 'タロウ',
                'company_name': 'テスト株式会社',
                'title': '部長',
                'url': 'https://example.com',
                'gender_cd': 1,
                'default_assignee': '@taro',
                'emails': emails,
                'archived_emails': archived_emails,
                'tels': tels,
                'archived_tels': archived_tels,
                'badge_ids': [1, 2],
                'system_id1': 'EMP0005',
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.customer_id, 5)
        self.assertEqual(result.system_id1, 'EMP0005')

    @patch.object(RelationClient, 'post')
    def test_create_with_no_optional_fields(self, mock_post):
        """create がオプション未指定時に空のデータを送ることを確認"""
        mock_post.return_value = {'customer_id': 7}

        result = self.client.customers.create(
            customer_group_id=self.customer_group_id
        )

        mock_post.assert_called_once_with(
            'customer_groups/1/customers/create',
            data={}
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.customer_id, 7)

    @patch.object(RelationClient, 'get')
    def test_get_by_email(self, mock_get):
        """get_by_email メソッドが正しく動作することを確認"""
        mock_get.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'first_name': '花子',
            'gender_cd': 2,
            'emails': [{'email': 'kyoto@example.com'}],
            'system_id1': 'EMP0002',
        }

        result = self.client.customers.get_by_email(
            customer_group_id=self.customer_group_id,
            email='kyoto@example.com'
        )

        mock_get.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com'
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.customer_id, 2)
        self.assertEqual(result.last_name, '京都')
        self.assertEqual(result.emails[0].email, 'kyoto@example.com')

    @patch.object(RelationClient, 'put')
    def test_update_by_system_id1_with_all_fields(self, mock_put):
        """update_by_system_id1 が全フィールドのブランチを設定することを確認"""
        mock_put.return_value = {
            'customer_id': 1,
            'last_name': '東京',
            'system_id1': 'EMP0001',
        }

        emails = [{'email': 'tokyo@example.com'}]
        archived_emails = [{'email': 'old@example.com'}]
        tels = [{'tel': '09000000000'}]
        archived_tels = [{'tel': '08000000000'}]

        result = self.client.customers.update_by_system_id1(
            customer_group_id=self.customer_group_id,
            system_id1='EMP0001',
            last_name='東京',
            first_name='次郎',
            last_name_kana='トウキョウ',
            first_name_kana='ジロウ',
            company_name='テスト株式会社',
            title='課長',
            url='https://example.com',
            gender_cd=1,
            default_assignee='@jiro',
            emails=emails,
            archived_emails=archived_emails,
            tels=tels,
            archived_tels=archived_tels,
            badge_ids=[3, 4],
        )

        mock_put.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001',
            data={
                'last_name': '東京',
                'first_name': '次郎',
                'last_name_kana': 'トウキョウ',
                'first_name_kana': 'ジロウ',
                'company_name': 'テスト株式会社',
                'title': '課長',
                'url': 'https://example.com',
                'gender_cd': 1,
                'default_assignee': '@jiro',
                'emails': emails,
                'archived_emails': archived_emails,
                'tels': tels,
                'archived_tels': archived_tels,
                'badge_ids': [3, 4],
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.last_name, '東京')
        self.assertEqual(result.system_id1, 'EMP0001')

    @patch.object(RelationClient, 'put')
    def test_update_by_email(self, mock_put):
        """update_by_email メソッドが正しく動作することを確認"""
        mock_put.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'emails': [{'email': 'kyoto@example.com'}],
            'system_id1': 'EMP0002',
        }

        result = self.client.customers.update_by_email(
            customer_group_id=self.customer_group_id,
            email='kyoto@example.com',
            last_name='京都',
            emails=[{'email': 'kyoto@example.com'}]
        )

        mock_put.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com',
            data={
                'last_name': '京都',
                'emails': [{'email': 'kyoto@example.com'}]
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.last_name, '京都')
        self.assertEqual(result.emails[0].email, 'kyoto@example.com')

    @patch.object(RelationClient, 'put')
    def test_update_by_email_with_all_fields(self, mock_put):
        """update_by_email が全フィールドのブランチを設定することを確認"""
        mock_put.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'system_id1': 'EMP0002',
        }

        emails = [{'email': 'kyoto@example.com'}]
        archived_emails = [{'email': 'old@example.com'}]
        tels = [{'tel': '09000000000'}]
        archived_tels = [{'tel': '08000000000'}]

        result = self.client.customers.update_by_email(
            customer_group_id=self.customer_group_id,
            email='kyoto@example.com',
            last_name='京都',
            first_name='花子',
            last_name_kana='キョウト',
            first_name_kana='ハナコ',
            company_name='テスト株式会社',
            title='主任',
            url='https://example.com',
            gender_cd=2,
            default_assignee='@hanako',
            emails=emails,
            archived_emails=archived_emails,
            tels=tels,
            archived_tels=archived_tels,
            badge_ids=[5, 6],
            system_id1='EMP0002',
        )

        mock_put.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com',
            data={
                'last_name': '京都',
                'first_name': '花子',
                'last_name_kana': 'キョウト',
                'first_name_kana': 'ハナコ',
                'company_name': 'テスト株式会社',
                'title': '主任',
                'url': 'https://example.com',
                'gender_cd': 2,
                'default_assignee': '@hanako',
                'emails': emails,
                'archived_emails': archived_emails,
                'tels': tels,
                'archived_tels': archived_tels,
                'badge_ids': [5, 6],
                'system_id1': 'EMP0002',
            }
        )
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.system_id1, 'EMP0002')

    @patch.object(RelationClient, 'delete')
    def test_delete_by_email(self, mock_delete):
        """delete_by_email メソッドが正しく動作することを確認"""
        mock_delete.return_value = {}

        self.client.customers.delete_by_email(
            customer_group_id=self.customer_group_id,
            email='kyoto@example.com'
        )

        mock_delete.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com'
        )

    @patch.object(RelationClient, 'delete')
    def test_delete_by_email_encodes_path_segment(self, mock_delete):
        """delete 系でも email がエンコードされることを確認"""
        mock_delete.return_value = {}

        self.client.customers.delete_by_email(
            customer_group_id=self.customer_group_id,
            email='x/y@example.com'
        )

        mock_delete.assert_called_once_with(
            'customer_groups/1/customers/email/x%2Fy%40example.com'
        )


if __name__ == '__main__':
    unittest.main()
