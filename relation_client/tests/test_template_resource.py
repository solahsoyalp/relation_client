"""
TemplateResourceクラスのテスト

このモジュールは、TemplateResourceクラスのメソッドをテストします。
"""
import pytest
from unittest import mock

from relation_client.models import Template
from relation_client.resources.templates import TemplateResource


class TestTemplateResource:
    """TemplateResourceのテストクラス"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        client.get.return_value = [
            {
                "template_id": 1,
                "template_category_name": "テストカテゴリ",
                "template_name": "テストテンプレート",
                "from": "from@example.com",
                "to": "to@example.com",
                "cc": "cc@example.com",
                "bcc": "bcc@example.com",
                "title": "テスト件名",
                "html_body": "<div>テスト本文</div>",
                "text_body": "テスト本文",
                "case_category_ids": [1, 2],
                "label_ids": [3, 4],
                "questionnaire_name": "アンケート"
            }
        ]
        client.post.return_value = [
            {
                "template_id": 2,
                "template_category_name": "テストカテゴリ2",
                "template_name": "検索テンプレート",
                "from": "from2@example.com",
                "to": "to2@example.com",
                "cc": "cc2@example.com",
                "bcc": "bcc2@example.com",
                "title": "検索件名",
                "html_body": "<div>検索本文</div>",
                "text_body": "検索本文",
                "case_category_ids": [5, 6],
                "label_ids": [7, 8],
                "questionnaire_name": "検索アンケート"
            }
        ]
        return client

    @pytest.fixture
    def template_resource(self, client_mock):
        """TemplateResourceインスタンス"""
        return TemplateResource(client_mock)

    def test_list(self, template_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        templates = template_resource.list(message_box_id=123, per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('123/templates', params={'per_page': 50, 'page': 1})
        assert len(templates) == 1
        template = templates[0]
        assert isinstance(template, Template)
        assert template.template_id == 1
        assert template.template_category_name == "テストカテゴリ"
        assert template.template_name == "テストテンプレート"
        assert template.from_ == "from@example.com"
        assert template.to == "to@example.com"
        assert template.cc == "cc@example.com"
        assert template.bcc == "bcc@example.com"
        assert template.title == "テスト件名"
        assert template.html_body == "<div>テスト本文</div>"
        assert template.text_body == "テスト本文"
        assert template.case_category_ids == [1, 2]
        assert template.label_ids == [3, 4]
        assert template.questionnaire_name == "アンケート"

    def test_list_with_default_params(self, template_resource, client_mock):
        """デフォルトパラメータでのlist()メソッドのテスト"""
        # 実行
        templates = template_resource.list(message_box_id=123)

        # 検証
        client_mock.get.assert_called_once_with('123/templates', params={})
        assert len(templates) == 1

    def test_search(self, template_resource, client_mock):
        """search()メソッドのテスト"""
        # 実行
        templates = template_resource.search(
            message_box_id=123,
            template_category_name="テストカテゴリ2"
        )

        # 検証
        client_mock.post.assert_called_once_with('123/templates/search', data={'template_category_name': 'テストカテゴリ2'})
        assert len(templates) == 1
        template = templates[0]
        assert isinstance(template, Template)
        assert template.template_id == 2
        assert template.template_category_name == "テストカテゴリ2"
        assert template.template_name == "検索テンプレート"

    def test_search_without_category(self, template_resource, client_mock):
        """カテゴリ指定なしのsearch()メソッドのテスト"""
        # 実行
        templates = template_resource.search(message_box_id=123)

        # 検証
        client_mock.post.assert_called_once_with('123/templates/search', data={})
        assert len(templates) == 1

    def test_list_empty_response(self, template_resource, client_mock):
        """空のレスポンスを返す場合のlist()メソッドのテスト"""
        # モックの設定
        client_mock.get.return_value = []
        
        # 実行
        templates = template_resource.list(message_box_id=123)
        
        # 検証
        assert templates == []
        assert len(templates) == 0
        
    def test_search_empty_response(self, template_resource, client_mock):
        """空のレスポンスを返す場合のsearch()メソッドのテスト"""
        # モックの設定
        client_mock.post.return_value = []
        
        # 実行
        templates = template_resource.search(message_box_id=123, template_category_name="存在しないカテゴリ")
        
        # 検証
        assert templates == []
        assert len(templates) == 0
        
    def test_list_non_list_response(self, template_resource, client_mock):
        """リスト以外のレスポンスを返す場合のlist()メソッドのテスト"""
        # モックの設定
        client_mock.get.return_value = {"error": "何らかのエラー"}
        
        # 実行
        templates = template_resource.list(message_box_id=123)
        
        # 検証
        assert templates == [] 