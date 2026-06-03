"""models モジュールのテスト（_parse_dt のリファクタリングと to_dict 追加分）"""
from datetime import datetime, timezone

import pytest

from relation_client.models import (
    _parse_dt,
    Attachment,
    Comment,
    Customer,
    Email,
    Message,
    Record,
    Tel,
    Ticket,
)


class TestParseDt:
    """_parse_dt ヘルパーのテスト"""

    def test_valid_z_suffixed_string(self):
        result = _parse_dt('2026-04-01T12:34:56Z')
        assert result == datetime(2026, 4, 1, 12, 34, 56, tzinfo=timezone.utc)

    def test_valid_offset_string(self):
        result = _parse_dt('2026-04-01T12:34:56+09:00')
        assert result is not None
        assert result.year == 2026

    def test_none_returns_none(self):
        assert _parse_dt(None) is None

    def test_empty_string_returns_none(self):
        assert _parse_dt('') is None

    def test_garbage_returns_none(self):
        assert _parse_dt('not-a-date') is None

    @pytest.mark.parametrize('value', [123, 1.5, [], {}, object()])
    def test_non_string_returns_none(self, value):
        """文字列以外（int 等）でも例外を送出せず None を返す"""
        assert _parse_dt(value) is None


class TestCustomerRoundTrip:
    """Customer.from_dict / to_dict のラウンドトリップ"""

    def test_round_trip_preserves_dict(self):
        d = {
            'customer_id': 100,
            'last_name': '山田',
            'first_name': '太郎',
            'last_name_kana': 'ヤマダ',
            'first_name_kana': 'タロウ',
            'company_name': 'テスト株式会社',
            'gender_cd': 1,
            'emails': [{'email': 'taro@example.com'}],
            'tels': [{'tel': '03-1234-5678'}],
            'badge_ids': [1, 2, 3],
            'last_updated_at': '2026-04-01T12:00:00Z',
        }
        customer = Customer.from_dict(d)
        assert customer.to_dict() == d

    def test_to_dict_is_a_copy(self):
        d = {'customer_id': 1}
        customer = Customer.from_dict(d)
        result = customer.to_dict()
        result['customer_id'] = 999
        assert customer.to_dict()['customer_id'] == 1

    def test_datetime_parsed(self):
        customer = Customer.from_dict({'last_updated_at': '2026-04-01T12:00:00Z'})
        assert customer.last_updated_at == datetime(2026, 4, 1, 12, 0, 0, tzinfo=timezone.utc)

    def test_missing_datetime_defaults_none(self):
        customer = Customer.from_dict({'customer_id': 1})
        assert customer.last_updated_at is None

    def test_invalid_datetime_defaults_none(self):
        customer = Customer.from_dict({'last_updated_at': 'garbage'})
        assert customer.last_updated_at is None


class TestEmailTelToDict:
    """Email / Tel の to_dict"""

    def test_email_to_dict(self):
        assert Email(email='a@example.com').to_dict() == {'email': 'a@example.com'}

    def test_tel_to_dict(self):
        assert Tel(tel='03-0000-0000').to_dict() == {'tel': '03-0000-0000'}


class TestTicketWithMessages:
    """メッセージ付き Ticket の datetime パース（リファクタ後の確認）"""

    def test_ticket_and_message_datetimes(self):
        d = {
            'ticket_id': 1,
            'status_cd': 'open',
            'title': 'テストチケット',
            'created_at': '2026-04-01T10:00:00Z',
            'last_updated_at': '2026-04-02T11:00:00Z',
            'messages': [
                {
                    'message_id': 10,
                    'sent_at': '2026-04-01T10:05:00Z',
                    'created_at': '2026-04-01T10:05:01Z',
                    'last_updated_at': '2026-04-01T10:05:02Z',
                    'comments': [
                        {'commenter': 'u', 'comment': 'hi',
                         'commented_at': '2026-04-01T10:06:00Z'},
                    ],
                },
            ],
        }
        ticket = Ticket.from_dict(d)
        assert ticket.created_at == datetime(2026, 4, 1, 10, 0, 0, tzinfo=timezone.utc)
        assert ticket.last_updated_at == datetime(2026, 4, 2, 11, 0, 0, tzinfo=timezone.utc)

        assert len(ticket.messages) == 1
        msg = ticket.messages[0]
        assert msg.sent_at == datetime(2026, 4, 1, 10, 5, 0, tzinfo=timezone.utc)
        assert msg.created_at == datetime(2026, 4, 1, 10, 5, 1, tzinfo=timezone.utc)
        assert msg.last_updated_at == datetime(2026, 4, 1, 10, 5, 2, tzinfo=timezone.utc)

        assert len(msg.comments) == 1
        assert msg.comments[0].commented_at == datetime(2026, 4, 1, 10, 6, 0, tzinfo=timezone.utc)

    def test_ticket_to_dict_round_trip(self):
        d = {'ticket_id': 5, 'status_cd': 'open', 'title': 't'}
        assert Ticket.from_dict(d).to_dict() == d


class TestAttachment:
    """Attachment.from_dict のテスト（models.py 186-191 のカバレッジ）"""

    def test_from_dict_populates_fields(self):
        d = {'attachment_id': 42, 'file_name': 'invoice.pdf'}
        attachment = Attachment.from_dict(d)
        assert attachment.attachment_id == 42
        assert attachment.file_name == 'invoice.pdf'

    def test_from_dict_missing_keys_default_none(self):
        attachment = Attachment.from_dict({})
        assert attachment.attachment_id is None
        assert attachment.file_name is None

    def test_from_dict_null_values(self):
        attachment = Attachment.from_dict({'attachment_id': None, 'file_name': None})
        assert attachment.attachment_id is None
        assert attachment.file_name is None

    def test_to_dict_round_trip(self):
        d = {'attachment_id': 7, 'file_name': 'a.txt'}
        assert Attachment.from_dict(d).to_dict() == d


class TestMessageWithAttachmentsAndRecord:
    """Message の attachments / record（Record）の取り扱い"""

    def test_message_parses_attachments(self):
        d = {
            'message_id': 1,
            'attachments': [
                {'attachment_id': 100, 'file_name': 'one.png'},
                {'attachment_id': 101, 'file_name': 'two.png'},
            ],
        }
        msg = Message.from_dict(d)
        assert len(msg.attachments) == 2
        assert isinstance(msg.attachments[0], Attachment)
        assert msg.attachments[0].attachment_id == 100
        assert msg.attachments[1].file_name == 'two.png'

    def test_message_with_record_dict(self):
        d = {
            'message_id': 2,
            'method_cd': 'record',
            'record': {
                'customer_id': 500,
                'customer_name': '山田太郎',
                'customer_emails': ['taro@example.com'],
                'customer_tels': ['03-1234-5678'],
            },
        }
        msg = Message.from_dict(d)
        assert isinstance(msg.record, Record)
        assert msg.record.customer_id == 500
        assert msg.record.customer_name == '山田太郎'
        assert msg.record.customer_emails == ['taro@example.com']
        assert msg.record.customer_tels == ['03-1234-5678']

    def test_message_record_none_when_absent(self):
        msg = Message.from_dict({'message_id': 3})
        assert msg.record is None

    def test_message_record_none_when_explicitly_null(self):
        msg = Message.from_dict({'message_id': 4, 'record': None})
        assert msg.record is None

    def test_message_record_ignored_when_not_dict(self):
        # record が文字列など dict でない場合は無視され None のまま
        msg = Message.from_dict({'message_id': 5, 'record': 'not-a-dict'})
        assert msg.record is None

    def test_message_empty_collections(self):
        msg = Message.from_dict({'message_id': 6, 'comments': [], 'attachments': []})
        assert msg.comments == []
        assert msg.attachments == []

    def test_message_missing_collections_default_empty(self):
        msg = Message.from_dict({'message_id': 7})
        assert msg.comments == []
        assert msg.attachments == []

    def test_message_to_dict_round_trip(self):
        d = {
            'message_id': 8,
            'from': 'sender@example.com',
            'method_cd': 'record',
            'record': {'customer_id': 1, 'customer_name': 'n',
                       'customer_emails': [], 'customer_tels': []},
            'attachments': [{'attachment_id': 1, 'file_name': 'f'}],
        }
        msg = Message.from_dict(d)
        assert msg.from_address == 'sender@example.com'
        assert msg.to_dict() == d


class TestRecord:
    """Record.from_dict の境界値テスト"""

    def test_from_dict_full(self):
        d = {
            'customer_id': 9,
            'customer_name': 'name',
            'customer_emails': ['a@b.com'],
            'customer_tels': ['000'],
        }
        record = Record.from_dict(d)
        assert record.customer_id == 9
        assert record.customer_name == 'name'
        assert record.customer_emails == ['a@b.com']
        assert record.customer_tels == ['000']

    def test_from_dict_missing_keys_default(self):
        record = Record.from_dict({})
        assert record.customer_id is None
        assert record.customer_name is None
        assert record.customer_emails == []
        assert record.customer_tels == []

    def test_from_dict_empty_lists(self):
        record = Record.from_dict({'customer_emails': [], 'customer_tels': []})
        assert record.customer_emails == []
        assert record.customer_tels == []


class TestTicketBoundary:
    """Ticket の境界値（空メッセージ／欠損キー）"""

    def test_empty_messages_list(self):
        ticket = Ticket.from_dict({'ticket_id': 1, 'messages': []})
        assert ticket.messages == []

    def test_missing_messages_default_empty(self):
        ticket = Ticket.from_dict({'ticket_id': 2})
        assert ticket.messages == []

    def test_missing_keys_no_exception(self):
        ticket = Ticket.from_dict({})
        assert ticket.ticket_id is None
        assert ticket.case_category_ids == []
        assert ticket.label_ids == []
        assert ticket.messages == []


@pytest.mark.parametrize("value, expected", [
    ('2026-04-01T12:34:56Z', datetime(2026, 4, 1, 12, 34, 56, tzinfo=timezone.utc)),
    (None, None),
    ('', None),
    ('not-a-date', None),
])
def test_parse_dt_parametrized(value, expected):
    assert _parse_dt(value) == expected


@pytest.mark.parametrize("model_cls, data", [
    (Customer, {}),
    (Comment, {}),
    (Attachment, {}),
    (Record, {}),
    (Message, {}),
    (Ticket, {}),
])
def test_from_dict_empty_no_exception(model_cls, data):
    """空の辞書でも例外を出さずに生成できること"""
    instance = model_cls.from_dict(data)
    assert instance.to_dict() == data
