"""
受信箱リソースのテスト

このモジュールは、MessageBoxResourceクラスのテストを提供します。
"""
import pytest
from unittest import mock

from relation_client.models import MessageBox
from relation_client.resources.message_boxes import MessageBoxResource


class TestMessageBoxResource:
    """MessageBoxResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        client.get.return_value = [
            {
                "name": "受信箱1",
                "color": "green",
                "message_box_id": 1,
                "last_updated_at": "2021-01-05T13:31:56Z",
                "customer_group_id": 1
            },
            {
                "name": "受信箱2",
                "color": "orange",
                "message_box_id": 2,
                "last_updated_at": "2021-01-12T16:07:26Z",
                "customer_group_id": 2
            }
        ]
        return client

    @pytest.fixture
    def message_box_resource(self, client_mock):
        """MessageBoxResourceインスタンス"""
        return MessageBoxResource(client_mock)

    def test_list(self, message_box_resource, client_mock):
        """list()メソッドのテスト"""
        # 実行
        result = message_box_resource.list()

        # 検証
        client_mock.get.assert_called_once_with("message_boxes")
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], MessageBox)
        assert result[0].message_box_id == 1
        assert result[0].name == "受信箱1"
        assert result[0].color == "green"
        assert result[0].customer_group_id == 1
        assert result[1].message_box_id == 2
        assert result[1].name == "受信箱2"
        assert result[1].color == "orange"
        assert result[1].customer_group_id == 2

    def test_get(self, message_box_resource, client_mock):
        """get()メソッドのテスト"""
        # 準備
        message_box_id = 1
        client_mock.get.return_value = {
            "name": "受信箱1",
            "color": "green",
            "message_box_id": 1,
            "last_updated_at": "2021-01-05T13:31:56Z",
            "customer_group_id": 1
        }

        # 実行
        result = message_box_resource.get(message_box_id)

        # 検証
        client_mock.get.assert_called_once_with(f"message_boxes/{message_box_id}")
        assert isinstance(result, MessageBox)
        assert result.message_box_id == 1
        assert result.name == "受信箱1"
        assert result.color == "green"
        assert result.customer_group_id == 1

    def test_list_empty(self, message_box_resource, client_mock):
        """list()メソッドが空レスポンスで空リストを返すテスト"""
        # モックの設定
        client_mock.get.return_value = []

        # 実行
        result = message_box_resource.list()

        # 検証
        client_mock.get.assert_called_once_with("message_boxes")
        assert result == []

    def test_get_other_id(self, message_box_resource, client_mock):
        """get()メソッドが任意の message_box_id をパスに含めるテスト"""
        # 準備
        message_box_id = 42
        client_mock.get.return_value = {
            "name": "受信箱42",
            "color": "blue",
            "message_box_id": 42,
            "last_updated_at": "2021-02-01T00:00:00Z",
            "customer_group_id": 7
        }

        # 実行
        result = message_box_resource.get(message_box_id)

        # 検証
        client_mock.get.assert_called_once_with("message_boxes/42")
        assert isinstance(result, MessageBox)
        assert result.message_box_id == 42
        assert result.name == "受信箱42"
        assert result.color == "blue"
        assert result.customer_group_id == 7
