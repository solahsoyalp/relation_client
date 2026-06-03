"""
CustomerResourceのテスト
"""

import pytest

from relation_client.models import Customer
from relation_client.resources.customers import CustomerResource


class TestCustomerResource:
    """CustomerResourceのテストクラス"""

    @pytest.fixture
    def customer_resource(self, client_mock):
        """CustomerResourceインスタンス"""
        return CustomerResource(client_mock)

    def test_search(self, customer_resource, client_mock):
        """search メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.get.return_value = [
            {
                'customer_id': 1,
                'name': 'テスト太郎',
                'gender_cd': 1,
                'emails': [{'email': 'test@example.com'}],
                'last_updated_at': '2023-01-01T00:00:00Z'
            }
        ]

        # テスト対象メソッドの実行
        result = customer_resource.search(
            customer_group_id=1,
            emails=['test@example.com']
        )

        # 検証
        client_mock.get.assert_called_once_with(
            'customer_groups/1/customers/search',
            params={
                'per_page': 10,
                'page': 1,
                'emails[]': ['test@example.com']
            }
        )
        assert len(result) == 1
        assert isinstance(result[0], Customer)
        assert result[0].customer_id == 1
        assert result[0].emails[0].email == 'test@example.com'

    def test_iter_all(self, customer_resource, client_mock):
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
        client_mock.get.side_effect = [page1, page2]

        result = list(customer_resource.iter_all(
            customer_group_id=1,
            per_page=per_page
        ))

        # 全ページの全件が連結して得られる
        assert len(result) == per_page + 1
        assert all(isinstance(c, Customer) for c in result)
        assert [c.customer_id for c in result] == [1, 2, 3, 4]

        # 2ページ呼び出した時点で停止していること
        assert client_mock.get.call_count == 2
        first_call = client_mock.get.call_args_list[0]
        second_call = client_mock.get.call_args_list[1]
        assert first_call.kwargs['params']['page'] == 1
        assert first_call.kwargs['params']['per_page'] == per_page
        assert second_call.kwargs['params']['page'] == 2

    def test_iter_all_stops_on_empty_page(self, customer_resource, client_mock):
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
        client_mock.get.side_effect = [
            [make_customer(1), make_customer(2)],
            [make_customer(3), make_customer(4)],
            []
        ]

        result = list(customer_resource.iter_all(
            customer_group_id=1,
            per_page=per_page
        ))

        assert [c.customer_id for c in result] == [1, 2, 3, 4]
        assert client_mock.get.call_count == 3

    def test_create(self, customer_resource, client_mock):
        """create メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.post.return_value = {
            'customer_id': 1,
            'last_name': '大阪',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'osaka@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = customer_resource.create(
            customer_group_id=1,
            last_name='大阪',
            first_name='太郎',
            gender_cd=1,
            emails=[{'email': 'osaka@example.com'}],
            system_id1='EMP0001'
        )

        # 検証
        client_mock.post.assert_called_once_with(
            'customer_groups/1/customers/create',
            data={
                'last_name': '大阪',
                'first_name': '太郎',
                'gender_cd': 1,
                'emails': [{'email': 'osaka@example.com'}],
                'system_id1': 'EMP0001'
            }
        )
        assert isinstance(result, Customer)
        assert result.customer_id == 1
        assert result.last_name == '大阪'
        assert result.first_name == '太郎'
        assert result.system_id1 == 'EMP0001'

    def test_get_by_system_id1(self, customer_resource, client_mock):
        """get_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.get.return_value = {
            'customer_id': 1,
            'last_name': '大阪',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'osaka@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = customer_resource.get_by_system_id1(
            customer_group_id=1,
            system_id1='EMP0001'
        )

        # 検証
        client_mock.get.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001'
        )
        assert isinstance(result, Customer)
        assert result.customer_id == 1
        assert result.system_id1 == 'EMP0001'

    def test_update_by_system_id1(self, customer_resource, client_mock):
        """update_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.put.return_value = {
            'customer_id': 1,
            'last_name': '東京',
            'first_name': '太郎',
            'gender_cd': 1,
            'emails': [{'email': 'tokyo@example.com'}],
            'system_id1': 'EMP0001'
        }

        # テスト対象メソッドの実行
        result = customer_resource.update_by_system_id1(
            customer_group_id=1,
            system_id1='EMP0001',
            last_name='東京',
            emails=[{'email': 'tokyo@example.com'}]
        )

        # 検証
        client_mock.put.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001',
            data={
                'last_name': '東京',
                'emails': [{'email': 'tokyo@example.com'}]
            }
        )
        assert isinstance(result, Customer)
        assert result.last_name == '東京'
        assert result.emails[0].email == 'tokyo@example.com'

    def test_delete_by_system_id1(self, customer_resource, client_mock):
        """delete_by_system_id1 メソッドが正しく動作することを確認"""
        # モックの設定
        client_mock.delete.return_value = {}

        # テスト対象メソッドの実行
        customer_resource.delete_by_system_id1(
            customer_group_id=1,
            system_id1='EMP0001'
        )

        # 検証
        client_mock.delete.assert_called_once_with(
            'customer_groups/1/customers/system_id1/EMP0001'
        )

    def test_get_by_email_encodes_path_segment(self, customer_resource, client_mock):
        """email がパスセグメントとして安全にエンコードされることを確認"""
        client_mock.get.return_value = {'customer_id': 1}

        # '?' でクエリ注入を試みる値
        customer_resource.get_by_email(
            customer_group_id=1,
            email='a@example.com?per_page=999'
        )

        # '@' '?' '=' がすべてパーセントエンコードされ、パスが変形されないこと
        client_mock.get.assert_called_once_with(
            'customer_groups/1/customers/email/a%40example.com%3Fper_page%3D999'
        )

    def test_get_by_system_id1_encodes_path_segment(self, customer_resource, client_mock):
        """system_id1 の '/' や日本語がエンコードされることを確認"""
        client_mock.get.return_value = {'customer_id': 1}

        customer_resource.get_by_system_id1(
            customer_group_id=1,
            system_id1='a/b 太郎'
        )

        # '/' → %2F, 空白 → %20, 日本語 → UTF-8 パーセントエンコード
        client_mock.get.assert_called_once_with(
            'customer_groups/1/customers/system_id1/a%2Fb%20%E5%A4%AA%E9%83%8E'
        )

    def test_search_with_all_optional_params(self, customer_resource, client_mock):
        """search が全オプションパラメータのブランチを設定することを確認"""
        client_mock.get.return_value = []

        customer_resource.search(
            customer_group_id=1,
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

        client_mock.get.assert_called_once_with(
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

    def test_create_with_all_optional_fields(self, customer_resource, client_mock):
        """create が全オプションフィールドのブランチを設定することを確認"""
        client_mock.post.return_value = {
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

        result = customer_resource.create(
            customer_group_id=1,
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

        client_mock.post.assert_called_once_with(
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
        assert isinstance(result, Customer)
        assert result.customer_id == 5
        assert result.system_id1 == 'EMP0005'

    def test_create_with_no_optional_fields(self, customer_resource, client_mock):
        """create がオプション未指定時に空のデータを送ることを確認"""
        client_mock.post.return_value = {'customer_id': 7}

        result = customer_resource.create(
            customer_group_id=1
        )

        client_mock.post.assert_called_once_with(
            'customer_groups/1/customers/create',
            data={}
        )
        assert isinstance(result, Customer)
        assert result.customer_id == 7

    def test_get_by_email(self, customer_resource, client_mock):
        """get_by_email メソッドが正しく動作することを確認"""
        client_mock.get.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'first_name': '花子',
            'gender_cd': 2,
            'emails': [{'email': 'kyoto@example.com'}],
            'system_id1': 'EMP0002',
        }

        result = customer_resource.get_by_email(
            customer_group_id=1,
            email='kyoto@example.com'
        )

        client_mock.get.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com'
        )
        assert isinstance(result, Customer)
        assert result.customer_id == 2
        assert result.last_name == '京都'
        assert result.emails[0].email == 'kyoto@example.com'

    def test_update_by_system_id1_with_all_fields(self, customer_resource, client_mock):
        """update_by_system_id1 が全フィールドのブランチを設定することを確認"""
        client_mock.put.return_value = {
            'customer_id': 1,
            'last_name': '東京',
            'system_id1': 'EMP0001',
        }

        emails = [{'email': 'tokyo@example.com'}]
        archived_emails = [{'email': 'old@example.com'}]
        tels = [{'tel': '09000000000'}]
        archived_tels = [{'tel': '08000000000'}]

        result = customer_resource.update_by_system_id1(
            customer_group_id=1,
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

        client_mock.put.assert_called_once_with(
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
        assert isinstance(result, Customer)
        assert result.last_name == '東京'
        assert result.system_id1 == 'EMP0001'

    def test_update_by_email(self, customer_resource, client_mock):
        """update_by_email メソッドが正しく動作することを確認"""
        client_mock.put.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'emails': [{'email': 'kyoto@example.com'}],
            'system_id1': 'EMP0002',
        }

        result = customer_resource.update_by_email(
            customer_group_id=1,
            email='kyoto@example.com',
            last_name='京都',
            emails=[{'email': 'kyoto@example.com'}]
        )

        client_mock.put.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com',
            data={
                'last_name': '京都',
                'emails': [{'email': 'kyoto@example.com'}]
            }
        )
        assert isinstance(result, Customer)
        assert result.last_name == '京都'
        assert result.emails[0].email == 'kyoto@example.com'

    def test_update_by_email_with_all_fields(self, customer_resource, client_mock):
        """update_by_email が全フィールドのブランチを設定することを確認"""
        client_mock.put.return_value = {
            'customer_id': 2,
            'last_name': '京都',
            'system_id1': 'EMP0002',
        }

        emails = [{'email': 'kyoto@example.com'}]
        archived_emails = [{'email': 'old@example.com'}]
        tels = [{'tel': '09000000000'}]
        archived_tels = [{'tel': '08000000000'}]

        result = customer_resource.update_by_email(
            customer_group_id=1,
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

        client_mock.put.assert_called_once_with(
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
        assert isinstance(result, Customer)
        assert result.system_id1 == 'EMP0002'

    def test_delete_by_email(self, customer_resource, client_mock):
        """delete_by_email メソッドが正しく動作することを確認"""
        client_mock.delete.return_value = {}

        customer_resource.delete_by_email(
            customer_group_id=1,
            email='kyoto@example.com'
        )

        client_mock.delete.assert_called_once_with(
            'customer_groups/1/customers/email/kyoto%40example.com'
        )

    def test_delete_by_email_encodes_path_segment(self, customer_resource, client_mock):
        """delete 系でも email がエンコードされることを確認"""
        client_mock.delete.return_value = {}

        customer_resource.delete_by_email(
            customer_group_id=1,
            email='x/y@example.com'
        )

        client_mock.delete.assert_called_once_with(
            'customer_groups/1/customers/email/x%2Fy%40example.com'
        )
