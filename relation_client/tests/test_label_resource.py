"""
LabelResourceクラスのテスト

このモジュールは、LabelResourceクラスの各メソッドをテストします。
"""
import pytest
from unittest import mock

from relation_client.models import Label
from relation_client.resources.labels import LabelResource


class TestLabelResource:
    """LabelResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        # list メソッドのレスポンスを設定
        client.get.return_value = [
            {
                "label_id": 1,
                "name": "重要",
                "color": "red",
                "parent_id": None
            },
            {
                "label_id": 2,
                "name": "サブラベル",
                "color": "blue",
                "parent_id": 1
            }
        ]

        return client

    @pytest.fixture
    def label_resource(self, client_mock):
        """LabelResourceインスタンス"""
        return LabelResource(client_mock)

    def test_list(self, label_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = label_resource.list(message_box_id=123, per_page=50, page=1)

        # 検証
        client_mock.get.assert_called_once_with('123/labels', params={'per_page': 50, 'page': 1})
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Label)

        # 1番目のラベルを検証
        assert result[0].label_id == 1
        assert result[0].name == "重要"
        assert result[0].color == "red"
        assert result[0].parent_id is None

        # 2番目のラベルを検証
        assert result[1].label_id == 2
        assert result[1].name == "サブラベル"
        assert result[1].color == "blue"
        assert result[1].parent_id == 1

    def test_list_with_default_params(self, label_resource, client_mock):
        """list()メソッドのデフォルトパラメータのテスト"""
        # 実行
        result = label_resource.list(message_box_id=123)

        # 検証
        client_mock.get.assert_called_once_with('123/labels', params={})
        assert isinstance(result, list)
        assert len(result) == 2

    def test_list_non_list_response(self, label_resource, client_mock):
        """list()メソッドがリスト以外のレスポンスで空リストを返すテスト"""
        client_mock.get.return_value = {"error": "not found"}

        result = label_resource.list(message_box_id=123)

        assert result == []

    def test_iter_all_multi_page(self, label_resource, client_mock):
        """iter_all()メソッドの複数ページのテスト"""
        # フルページ(per_page=2)の後に短いページ(1件)を返すことで停止させる
        full_page = [
            {"label_id": 1, "name": "ラベル1", "color": "red", "parent_id": None},
            {"label_id": 2, "name": "ラベル2", "color": "blue", "parent_id": None},
        ]
        short_page = [
            {"label_id": 3, "name": "ラベル3", "color": "green", "parent_id": None},
        ]
        client_mock.get.side_effect = [full_page, short_page]

        result = list(label_resource.iter_all(message_box_id=123, per_page=2))

        # 全3件が列挙される
        assert len(result) == 3
        assert all(isinstance(label, Label) for label in result)
        assert [label.label_id for label in result] == [1, 2, 3]

        # 2ページ分のリクエストが行われる
        assert client_mock.get.call_count == 2
        client_mock.get.assert_any_call('123/labels', params={'per_page': 2, 'page': 1})
        client_mock.get.assert_any_call('123/labels', params={'per_page': 2, 'page': 2})

    def test_iter_all_single_short_page(self, label_resource, client_mock):
        """iter_all()メソッドが1ページ目で停止するテスト(デフォルトper_page)"""
        # デフォルトの停止判定件数(50)未満なので1ページで停止する
        client_mock.get.return_value = [
            {"label_id": 1, "name": "ラベル1", "color": "red", "parent_id": None},
        ]

        result = list(label_resource.iter_all(message_box_id=123))

        assert len(result) == 1
        assert client_mock.get.call_count == 1
        client_mock.get.assert_called_once_with('123/labels', params={'page': 1})

    def test_iter_all_empty(self, label_resource, client_mock):
        """iter_all()メソッドが0件のとき即停止するテスト"""
        client_mock.get.return_value = []

        result = list(label_resource.iter_all(message_box_id=123, per_page=10))

        assert result == []
        assert client_mock.get.call_count == 1

    def test_create(self, label_resource, client_mock):
        """create()メソッドのテスト"""
        client_mock.post.return_value = {"label_id": 10}

        result = label_resource.create(message_box_id=123, name="新ラベル", color="red")

        client_mock.post.assert_called_once_with(
            '123/labels', data={'name': '新ラベル', 'color': 'red'}
        )
        assert result == {"label_id": 10}

    def test_create_with_parent_id(self, label_resource, client_mock):
        """create()メソッドのparent_id指定のテスト"""
        client_mock.post.return_value = {"label_id": 11}

        result = label_resource.create(
            message_box_id=123, name="子ラベル", color="blue", parent_id=10
        )

        client_mock.post.assert_called_once_with(
            '123/labels', data={'name': '子ラベル', 'color': 'blue', 'parent_id': 10}
        )
        assert result == {"label_id": 11}

    def test_update_all_fields(self, label_resource, client_mock):
        """update()メソッドの全フィールド指定のテスト"""
        result = label_resource.update(
            message_box_id=123, label_id=5, name="更新名", color="green", parent_id=2
        )

        client_mock.put.assert_called_once_with(
            '123/labels/5', data={'name': '更新名', 'color': 'green', 'parent_id': 2}
        )
        assert result is None

    def test_update_partial_fields(self, label_resource, client_mock):
        """update()メソッドの一部フィールドのみ指定のテスト"""
        label_resource.update(message_box_id=123, label_id=5, name="名前だけ")

        client_mock.put.assert_called_once_with(
            '123/labels/5', data={'name': '名前だけ'}
        )

    def test_update_no_fields(self, label_resource, client_mock):
        """update()メソッドのフィールド未指定のテスト"""
        label_resource.update(message_box_id=123, label_id=5)

        client_mock.put.assert_called_once_with('123/labels/5', data={})
