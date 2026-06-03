"""
保留理由リソースのテスト

このモジュールは、PendingReasonResourceクラスのテストを提供します。
"""
import pytest
from unittest import mock

from relation_client.models import PendingReason
from relation_client.resources.pending_reasons import PendingReasonResource


class TestPendingReasonResource:
    """PendingReasonResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        client.get.return_value = [
            {
                "name": "スヌーズ中",
                "snooze_term": "today",
                "pending_reason_id": 1,
                "is_snoozed": True
            },
            {
                "name": "確認待ち",
                "snooze_term": "no_term",
                "pending_reason_id": 2,
                "is_snoozed": False
            },
            {
                "name": "翌日連絡",
                "snooze_term": "tomorrow",
                "pending_reason_id": 3,
                "is_snoozed": True
            }
        ]
        return client

    @pytest.fixture
    def pending_reason_resource(self, client_mock):
        """PendingReasonResourceインスタンス"""
        return PendingReasonResource(client_mock)

    def test_list(self, pending_reason_resource, client_mock):
        """list()メソッドのテスト"""
        # 準備
        message_box_id = 123

        # 実行
        result = pending_reason_resource.list(message_box_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/pending_reasons")
        assert isinstance(result, list)
        assert len(result) == 3
        assert isinstance(result[0], PendingReason)
        assert result[0].pending_reason_id == 1
        assert result[0].name == "スヌーズ中"
        assert result[0].is_snoozed is True
        assert result[0].snooze_term == "today"
        assert result[1].pending_reason_id == 2
        assert result[1].name == "確認待ち"
        assert result[1].is_snoozed is False
        assert result[1].snooze_term == "no_term"
        assert result[2].pending_reason_id == 3
        assert result[2].name == "翌日連絡"
        assert result[2].is_snoozed is True
        assert result[2].snooze_term == "tomorrow"

    def test_list_empty(self, pending_reason_resource, client_mock):
        """list()メソッドが空レスポンスで空リストを返すテスト"""
        # モックの設定
        client_mock.get.return_value = []

        # 実行
        result = pending_reason_resource.list(456)

        # 検証
        client_mock.get.assert_called_once_with("456/pending_reasons")
        assert result == []

    def test_list_path_uses_message_box_id(self, pending_reason_resource, client_mock):
        """list()メソッドが message_box_id を正しくパスに含めるテスト"""
        # モックの設定（単一要素）
        client_mock.get.return_value = [
            {
                "name": "確認待ち",
                "snooze_term": "no_term",
                "pending_reason_id": 99,
                "is_snoozed": False
            }
        ]

        # 実行
        result = pending_reason_resource.list(789)

        # 検証
        client_mock.get.assert_called_once_with("789/pending_reasons")
        assert len(result) == 1
        assert isinstance(result[0], PendingReason)
        assert result[0].pending_reason_id == 99
        assert result[0].is_snoozed is False
