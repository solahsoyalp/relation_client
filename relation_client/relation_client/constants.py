"""
Re:lation API定数モジュール

このモジュールは、Re:lation APIで使用される定数を定義します。
"""

# APIエンドポイント
API_VERSION = 'v2'
BASE_URL_FORMAT = 'https://{subdomain}.relationapp.jp/api/{api_version}'

# レートリミット
RATE_LIMIT_LIMIT = 'X-RateLimit-Limit'
RATE_LIMIT_REMAINING = 'X-RateLimit-Remaining'
RATE_LIMIT_RESET = 'X-RateLimit-Reset'

# HTTPステータスコード
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_UNSUPPORTED_MEDIA_TYPE = 415
HTTP_TOO_MANY_REQUESTS = 429
HTTP_SERVER_ERROR = 500
HTTP_SERVICE_UNAVAILABLE = 503

# 性別コード
GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_UNKNOWN = 9 

# チケットステータス
STATUS_OPEN = 'open'  # 未対応
STATUS_ONGOING = 'ongoing'  # 保留
STATUS_CLOSED = 'closed'  # 対応完了
STATUS_UNWANTED = 'unwanted'  # 対応不要
STATUS_TRASH = 'trash'  # ゴミ箱
STATUS_SPAM = 'spam'  # 迷惑メール

# チケット色
COLOR_RED = 'red'  # 赤
COLOR_ORANGE = 'orange'  # オレンジ
COLOR_YELLOW = 'yellow'  # 黄色
COLOR_BLUE = 'blue'  # 青
COLOR_PINK = 'pink'  # ピンク

# チャネル（メソッド）
METHOD_MAIL = 'mail'  # メール
METHOD_TWEET = 'tweet'  # ツイート
METHOD_TWITTER_DM = 'twitter_dm'  # Twitter DM
METHOD_RECORD = 'record'  # 応対メモ
METHOD_LINE = 'line'  # LINE
METHOD_CHATPLUS = 'chatplus'  # ChatPlus
METHOD_R_MESSE = 'r_messe'  # R-Messe
METHOD_YAHOO = 'yahoo'  # Yahoo!ショッピング
METHOD_SMS = 'sms'  # SMS
METHOD_CALL = 'call'  # 通話メモ

# メッセージの状態
ACTION_RECEIVED = 'received'  # 受信
ACTION_SENT = 'sent'  # 送信済み
ACTION_DRAFT = 'draft'  # 下書き
ACTION_REQUESTED = 'requested'  # 承認依頼
ACTION_APPROVED = 'approved'  # 承認済み
ACTION_REJECTED = 'rejected'  # 差し戻し
ACTION_SENDING = 'sending'  # 送信中
ACTION_SCHEDULED = 'scheduled'  # 予約済み
ACTION_SEND_ERROR = 'send_error'  # 送信エラー
ACTION_CONVERSATION = 'conversation'  # チャット中
ACTION_END_CONVERSATION = 'end_conversation'  # チャット終了

# 応対種別（アイコン）
ICON_RECEIVED_PHONE = 'received_phone'  # 受電
ICON_CALLED_PHONE = 'called_phone'  # 架電
ICON_MEETING = 'meeting'  # 会議
ICON_SALES = 'sales'  # 営業
ICON_POSTAL = 'postal'  # 郵便物
ICON_NOTE = 'note'  # その他

# コメントタイプ
COMMENT_TYPE_COMMENT = 'comment'  # コメント
COMMENT_TYPE_REQUEST = 'request'  # 承認依頼
COMMENT_TYPE_APPROVE = 'approve'  # 承認
COMMENT_TYPE_REJECT = 'reject'  # 差戻し
COMMENT_TYPE_PULLBACK = 'pullback'  # 承認依頼キャンセル
COMMENT_TYPE_ASSIGN = 'assign'  # 担当者設定
COMMENT_TYPE_SNOOZE = 'snooze'  # スヌーズ
COMMENT_TYPE_CANCELED_SNOOZE = 'canceled_snooze'  # スヌーズ（キャンセル済み）

# チャット会話種別
CONVERSATION_TYPE_TEXT = 'text'  # テキスト
CONVERSATION_TYPE_FILE = 'file'  # ファイル
CONVERSATION_TYPE_IMAGE = 'image'  # 画像
CONVERSATION_TYPE_VIDEO = 'video'  # 動画
CONVERSATION_TYPE_AUDIO = 'audio'  # 音声
CONVERSATION_TYPE_LOCATION = 'location'  # 位置情報
CONVERSATION_TYPE_STICKER = 'sticker'  # スタンプ
CONVERSATION_TYPE_CHATPLUS_TEXTFORM = 'chatplus_textform'  # テキストフォーム
CONVERSATION_TYPE_CHATPLUS_CAROUSEL = 'chatplus_carousel'  # カルーセル
CONVERSATION_TYPE_CHATPLUS_CHATBOT = 'chatplus_chatbot'  # ChatPlusパーツ
CONVERSATION_TYPE_CHATPLUS_IMAGEMAP = 'chatplus_imagemap'  # イメージマップ

# スヌーズから復帰する日時（定義済み）
SNOOZE_NO_TERM = 'no_term'  # 設定なし
SNOOZE_TODAY = 'today'  # 今日の17時
SNOOZE_TOMORROW = 'tomorrow'  # 明日の8時
SNOOZE_WEEKEND = 'weekend'  # 今週末の8時
SNOOZE_NEXT_MONDAY = 'next_monday'  # 来週月曜の8時
SNOOZE_NEXT_WEEK = 'next_week'  # 1週間後の8時
SNOOZE_NEXT_MONTH = 'next_month'  # 来月1日の8時
SNOOZE_AFTER_MONTH = 'after_month'  # 1ヶ月後の8時

# ユーザー状態
USER_STATUS_AVAILABLE = 'available'  # 有効
USER_STATUS_CONFIRMING = 'confirming'  # 本登録処理中
USER_STATUS_LOCKED = 'locked'  # アカウントロック中
USER_STATUS_DELETED = 'deleted'  # 削除済み 