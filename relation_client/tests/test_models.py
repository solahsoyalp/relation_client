"""models モジュールのテスト（_parse_dt のリファクタリングと to_dict 追加分）"""
from datetime import datetime, timezone

from relation_client.models import (
    _parse_dt,
    Customer,
    Email,
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
