"""
チケット分類リソースのテスト

このモジュールは、CaseCategoryResourceクラスのテストを提供します。
"""
import pytest
from unittest import mock

from relation_client.models import CaseCategory
from relation_client.resources.case_categories import CaseCategoryResource


class TestCaseCategoryResource:
    """CaseCategoryResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        # list メソッドのレスポンスを設定
        client.get.return_value = [
            {
                "case_category_id": 1,
                "name": "お問い合わせ",
                "parent_id": None,
                "archived": False
            },
            {
                "case_category_id": 2,
                "name": "お問い合わせ > 顧客",
                "parent_id": 1,
                "archived": True
            },
            {
                "case_category_id": 3,
                "name": "サポート",
                "parent_id": None,
                "archived": False
            }
        ]

        # create メソッドのレスポンスを設定
        client.post.return_value = {"case_category_id": 4}

        # update メソッドのレスポンスを設定（204 No Content を想定）
        client.put.return_value = {}

        return client

    @pytest.fixture
    def case_category_resource(self, client_mock):
        """CaseCategoryResourceインスタンス"""
        return CaseCategoryResource(client_mock)

    def test_list(self, case_category_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = case_category_resource.list(message_box_id=123, per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('123/case_categories', params={'per_page': 50, 'page': 1})
        assert isinstance(result, list)
        assert len(result) == 3
        assert isinstance(result[0], CaseCategory)

        # 1番目のチケット分類を検証
        assert result[0].case_category_id == 1
        assert result[0].name == "お問い合わせ"
        assert result[0].parent_id is None
        assert result[0].archived is False

        # 2番目のチケット分類を検証
        assert result[1].case_category_id == 2
        assert result[1].name == "お問い合わせ > 顧客"
        assert result[1].parent_id == 1
        assert result[1].archived is True

        # 3番目のチケット分類を検証
        assert result[2].case_category_id == 3
        assert result[2].name == "サポート"
        assert result[2].parent_id is None
        assert result[2].archived is False

    def test_list_with_default_params(self, case_category_resource, client_mock):
        """list()メソッドのデフォルトパラメータのテスト"""
        # 実行
        result = case_category_resource.list(message_box_id=123)

        # 検証
        client_mock.get.assert_called_once_with('123/case_categories', params={})
        assert isinstance(result, list)
        assert len(result) == 3

    def test_create(self, case_category_resource, client_mock):
        """create()メソッドのテスト"""
        # 実行
        result = case_category_resource.create(
            message_box_id=123,
            name="新しいカテゴリ",
            parent_id=1
        )

        # 検証
        client_mock.post.assert_called_once_with('123/case_categories', data={'name': '新しいカテゴリ', 'parent_id': 1})
        assert result == {"case_category_id": 4}

    def test_create_without_parent(self, case_category_resource, client_mock):
        """create()メソッドの親なしのテスト"""
        # 実行
        result = case_category_resource.create(
            message_box_id=123,
            name="親なしカテゴリ"
        )

        # 検証
        client_mock.post.assert_called_once_with('123/case_categories', data={'name': '親なしカテゴリ'})
        assert result == {"case_category_id": 4}

    def test_update(self, case_category_resource, client_mock):
        """update()メソッドのテスト"""
        # 実行
        case_category_resource.update(
            message_box_id=123,
            case_category_id=1,
            name="更新カテゴリ",
            parent_id=2,
            archived=True
        )

        # 検証
        client_mock.put.assert_called_once_with('123/case_categories/1', data={
            'name': '更新カテゴリ',
            'parent_id': 2,
            'archived': True
        })

    def test_update_partial(self, case_category_resource, client_mock):
        """update()メソッドの部分更新テスト"""
        # 実行
        case_category_resource.update(
            message_box_id=123,
            case_category_id=1,
            name="名前のみ更新"
        )

        # 検証
        client_mock.put.assert_called_once_with('123/case_categories/1', data={'name': '名前のみ更新'})

    def test_update_parent_only(self, case_category_resource, client_mock):
        """update()メソッドで parent_id のみ指定するテスト"""
        # 実行
        case_category_resource.update(
            message_box_id=123,
            case_category_id=5,
            parent_id=2
        )

        # 検証
        client_mock.put.assert_called_once_with('123/case_categories/5', data={'parent_id': 2})

    def test_update_archived_only(self, case_category_resource, client_mock):
        """update()メソッドで archived のみ指定するテスト"""
        # 実行
        case_category_resource.update(
            message_box_id=123,
            case_category_id=7,
            archived=True
        )

        # 検証
        client_mock.put.assert_called_once_with('123/case_categories/7', data={'archived': True})

    def test_update_empty(self, case_category_resource, client_mock):
        """update()メソッドで何も指定しない場合のテスト"""
        # 実行
        case_category_resource.update(message_box_id=123, case_category_id=9)

        # 検証
        client_mock.put.assert_called_once_with('123/case_categories/9', data={})

    def test_iter_all_single_page(self, case_category_resource, client_mock):
        """iter_all()メソッドの単一ページ（短い最終ページ）のテスト"""
        # per_page=100 に対し3件しか返らないため1ページで停止
        result = list(case_category_resource.iter_all(message_box_id=123, per_page=100))

        # 検証
        client_mock.get.assert_called_once_with('123/case_categories', params={'per_page': 100, 'page': 1})
        assert len(result) == 3
        assert all(isinstance(item, CaseCategory) for item in result)
        assert [c.case_category_id for c in result] == [1, 2, 3]

    def test_iter_all_multi_page(self, case_category_resource, client_mock):
        """iter_all()メソッドの複数ページのテスト（フルページ後に短い最終ページ）"""
        full_page = [
            {"case_category_id": i, "name": f"カテゴリ{i}", "parent_id": None, "archived": False}
            for i in range(1, 3)
        ]
        last_page = [
            {"case_category_id": 3, "name": "カテゴリ3", "parent_id": None, "archived": False}
        ]
        client_mock.get.side_effect = [full_page, last_page]

        # per_page=2: 1ページ目はフル(2件)、2ページ目は1件で停止
        result = list(case_category_resource.iter_all(message_box_id=123, per_page=2))

        # 検証
        assert len(result) == 3
        assert [c.case_category_id for c in result] == [1, 2, 3]
        assert client_mock.get.call_count == 2
        client_mock.get.assert_any_call('123/case_categories', params={'per_page': 2, 'page': 1})
        client_mock.get.assert_any_call('123/case_categories', params={'per_page': 2, 'page': 2})

    def test_iter_all_default_per_page(self, case_category_resource, client_mock):
        """iter_all()メソッドで per_page を省略した場合のテスト（デフォルト30で停止）"""
        # 3件 < 30 のため1ページで停止
        result = list(case_category_resource.iter_all(message_box_id=123))

        # 検証
        client_mock.get.assert_called_once_with('123/case_categories', params={'page': 1})
        assert len(result) == 3
