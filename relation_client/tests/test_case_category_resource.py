"""
チケット分類リソースのテスト

このモジュールは、CaseCategoryResourceクラスのテストを提供します。
"""
import json
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