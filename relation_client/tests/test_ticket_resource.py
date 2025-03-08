"""
チケットリソースのテスト

このモジュールは、TicketResourceクラスのテストを提供します。
"""
import json
import pytest
from unittest import mock

from relation_client.models import Ticket, Message
from relation_client.resources.tickets import TicketResource


class TestTicketResource:
    """TicketResourceクラスのテスト"""

    @pytest.fixture
    def client_mock(self):
        """APIクライアントのモック"""
        client = mock.Mock()
        return client

    @pytest.fixture
    def ticket_resource(self, client_mock):
        """TicketResourceインスタンス"""
        return TicketResource(client_mock)

    def test_search(self, ticket_resource, client_mock):
        """search()メソッドのテスト"""
        # 準備
        message_box_id = 123
        client_mock.get.return_value = [
            {
                "ticket_id": 1,
                "assignee": "yamada",
                "status_cd": "open",
                "created_at": "2021-01-05T13:31:56Z",
                "last_updated_at": "2021-01-05T13:31:56Z",
                "title": "お問い合わせ",
                "color_cd": "red"
            },
            {
                "ticket_id": 2,
                "assignee": "tanaka",
                "status_cd": "ongoing",
                "created_at": "2021-01-06T10:15:30Z",
                "last_updated_at": "2021-01-06T10:15:30Z",
                "title": "商品について",
                "color_cd": "blue"
            }
        ]

        # 実行
        result = ticket_resource.search(
            message_box_id=message_box_id,
            status_cds=["open", "ongoing"],
            method_cds=["mail"],
            per_page=20,
            page=1
        )

        # 検証
        client_mock.get.assert_called_once()
        assert f"{message_box_id}/tickets" in client_mock.get.call_args[0][0]
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Ticket)
        assert result[0].ticket_id == 1
        assert result[0].assignee == "yamada"
        assert result[0].status_cd == "open"
        assert result[0].title == "お問い合わせ"
        assert result[1].ticket_id == 2
        assert result[1].status_cd == "ongoing"
        assert result[1].color_cd == "blue"

    def test_get(self, ticket_resource, client_mock):
        """get()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        client_mock.get.return_value = {
            "ticket_id": 456,
            "assignee": "yamada",
            "status_cd": "open",
            "created_at": "2021-01-05T13:31:56Z",
            "last_updated_at": "2021-01-05T13:31:56Z",
            "title": "お問い合わせ",
            "color_cd": "red",
            "messages": [
                {
                    "message_id": 789,
                    "from": "customer@example.com",
                    "to": "support@example.com",
                    "sent_at": "2021-01-05T13:30:00Z",
                    "title": "商品について",
                    "body": "商品の詳細を教えてください",
                    "method_cd": "mail",
                    "action_cd": "received"
                }
            ]
        }

        # 実行
        result = ticket_resource.get(message_box_id, ticket_id)

        # 検証
        client_mock.get.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}")
        assert isinstance(result, Ticket)
        assert result.ticket_id == 456
        assert result.assignee == "yamada"
        assert result.status_cd == "open"
        assert result.title == "お問い合わせ"
        assert len(result.messages) == 1
        assert isinstance(result.messages[0], Message)
        assert result.messages[0].message_id == 789
        assert result.messages[0].from_address == "customer@example.com"
        assert result.messages[0].title == "商品について"
        assert result.messages[0].method_cd == "mail"

    def test_update(self, ticket_resource, client_mock):
        """update()メソッドのテスト"""
        # 準備
        message_box_id = 123
        ticket_id = 456
        update_data = {
            "status_cd": "closed",
            "color_cd": "red",
            "assignee": "yamada"
        }
        client_mock.put.return_value = {
            "ticket_id": 456,
            "assignee": "yamada",
            "status_cd": "closed",
            "color_cd": "red"
        }

        # 実行
        ticket_resource.update(
            message_box_id=message_box_id,
            ticket_id=ticket_id,
            status_cd="closed",
            color_cd="red",
            assignee="yamada"
        )

        # 検証
        client_mock.put.assert_called_once_with(f"{message_box_id}/tickets/{ticket_id}", update_data)

    def test_create_record(self, ticket_resource, client_mock):
        """create_record()メソッドのテスト"""
        # 準備
        message_box_id = 123
        subject = "応対メモ"
        operated_at = "2021-01-05T13:30:00+09:00"
        duration = 30
        body = "お問い合わせ対応しました"
        client_mock.post.return_value = {
            "message_id": 789,
            "ticket_id": 456
        }

        # 新規チケットの場合
        # 実行
        result = ticket_resource.create_record(
            message_box_id=message_box_id,
            subject=subject,
            operated_at=operated_at,
            duration=duration,
            body=body,
            status_cd="open",
            icon_cd="meeting",
            customer_email="customer@example.com",
            operator="tanaka"
        )

        # 検証
        client_mock.post.assert_called_once()
        assert f"{message_box_id}/records" in client_mock.post.call_args[0][0]
        assert isinstance(result, dict)
        assert result["message_id"] == 789
        assert result["ticket_id"] == 456

        # 既存チケットの場合
        client_mock.reset_mock()
        ticket_id = 456
        client_mock.post.return_value = {
            "message_id": 790
        }

        # 実行
        result = ticket_resource.create_record(
            message_box_id=message_box_id,
            subject=subject,
            operated_at=operated_at,
            duration=duration,
            body=body,
            ticket_id=ticket_id,
            icon_cd="called_phone"
        )

        # 検証
        client_mock.post.assert_called_once()
        assert f"{message_box_id}/tickets/{ticket_id}/records" in client_mock.post.call_args[0][0]
        assert isinstance(result, dict)
        assert result["message_id"] == 790 