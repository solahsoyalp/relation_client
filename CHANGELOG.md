# 変更履歴

このプロジェクトのすべての重要な変更は、このファイルに記載されます。

フォーマットは[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、このプロジェクトは[Semantic Versioning](https://semver.org/lang/ja/)を採用しています。

## [Unreleased] - 未リリース

### 追加
- 公式API更新（2026/04）への対応
  - `Message` に `record` フィールドを追加（`method_cd` が `record` の応対メモに紐づく顧客情報。顧客情報が紐づかない場合は `None`）。新規 `Record` モデル（`customer_id` / `customer_name` / `customer_emails` / `customer_tels`）を追加
  - R-Messe（`RMesse`）に `social_gift_user_type` フィールドを追加（ソーシャルギフトのユーザー種別: `"注文者"` / `"受取人"` / `None`）
- 型情報の配布: PEP 561 準拠の `py.typed` マーカーを追加（利用側で mypy/Pyright が型を認識可能に）
- GitHub Actions による CI を追加（Python 3.8〜3.12 マトリクスで flake8 / black / isort / mypy / pytest を実行）
- メール送信系（`send` / `reply` / `draft`）に `status_cd`・`pending_reason_id` パラメータを追加

### 修正
- **メール送信が失敗する不具合を修正**: `MailResource.send()` のエンドポイントが誤って `{message_box_id}/mails/send` になっていたため、正しい `{message_box_id}/mails` に修正。必須フィールド `status_cd` の欠落も修正
- ネットワークエラー時のリトライを冪等メソッド（GET / DELETE）のみに限定。POST / PUT はタイムアウト時にメール二重送信などの副作用が重複する恐れがあるためリトライしないよう修正

### 変更
- サポート対象 Python を 3.8 以上に更新（3.6 / 3.7 は EOL のため除外）。classifier に 3.11 / 3.12 を追加
- テストスイートを実装・公式仕様に整合（応対メモ作成パス `{message_box_id}/records`、チケット更新・検索のテスト修正）。全テストが green

## [0.1.0] - 2024-02-27

### 追加
- 初期リリース
- Re:lation API基本クライアント機能
- 顧客（Customer）リソース
- 顧客グループ（CustomerGroup）リソース
- チケット（Ticket）リソース
- チャット（Chat）リソース
- メッセージボックス（MessageBox）リソース
- 保留理由（PendingReason）リソース
- ユーザー（User）リソース
- チケット分類（CaseCategory）リソース
- ラベル（Label）リソース
- バッジ（Badge）リソース
- メールアカウント（MailAccount）リソース
- メール（Mail）リソース
- テンプレート（Template）リソース
- 添付ファイル（Attachment）リソース
- 基本的なエラーハンドリング
- ユニットテスト
- 基本的なドキュメント

### 変更
- なし（初期リリース）

### 修正
- なし（初期リリース）

---

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for the official API update (2026/04)
  - Added the `record` field to `Message` (customer info attached to record memos where `method_cd` is `record`; `None` when no customer is linked). Added a new `Record` model (`customer_id` / `customer_name` / `customer_emails` / `customer_tels`)
  - Added the `social_gift_user_type` field to R-Messe (`RMesse`) — the social gift user type: `"注文者"` / `"受取人"` / `None`
- Type distribution: added a PEP 561 `py.typed` marker so downstream mypy/Pyright pick up the package's types
- GitHub Actions CI (runs flake8 / black / isort / mypy / pytest across a Python 3.8–3.12 matrix)
- Added `status_cd` and `pending_reason_id` parameters to the mail `send` / `reply` / `draft` methods

### Fixed
- **Mail sending failure**: `MailResource.send()` used the wrong endpoint `{message_box_id}/mails/send`; corrected to `{message_box_id}/mails`, and fixed the missing required `status_cd` field
- Network-error retries are now limited to idempotent methods (GET / DELETE). POST / PUT are no longer retried on timeout, preventing duplicate side effects such as sending the same email twice

### Changed
- Minimum supported Python raised to 3.8 (3.6 / 3.7 are EOL); added 3.11 / 3.12 classifiers
- Reconciled the test suite with the implementation and official spec (record-creation path `{message_box_id}/records`, ticket update/search tests). All tests pass

## [0.1.0] - 2024-02-27

### Added
- Initial release
- Basic Re:lation API client functionality
- Customer resource
- CustomerGroup resource
- Ticket resource
- Chat resource
- MessageBox resource
- PendingReason resource
- User resource
- CaseCategory resource
- Label resource
- Badge resource
- MailAccount resource
- Mail resource
- Template resource
- Attachment resource
- Basic error handling
- Unit tests
- Basic documentation

### Changed
- None (initial release)

### Fixed
- None (initial release) 