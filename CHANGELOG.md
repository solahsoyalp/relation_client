# 変更履歴

このプロジェクトのすべての重要な変更は、このファイルに記載されます。

フォーマットは[Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)に基づいており、このプロジェクトは[Semantic Versioning](https://semver.org/lang/ja/)を採用しています。

## [Unreleased] - 未リリース

### 追加
- 次回リリースの変更をここに記載します

## [0.3.1] - 2026-06-04

### その他
- メンテナンスリリース。機能・APIの変更はありません。
- リリース自動化（PyPI Trusted Publisher / GitHub Actions OIDC）導入後の初回自動公開の動作確認。

## [0.3.0] - 2026-06-04

### 変更（破壊的）
- **Python 3.8 / 3.9 のサポートを終了**し、`requires-python` を `>=3.10` に引き上げ。3.8 / 3.9 を利用する場合は `0.2.x` を利用してください。
- 依存宣言から環境マーカーを撤廃し、修正版を直接要求するよう統一: `requests>=2.33.0`・`urllib3>=2.7.0`（いずれも Python 3.10+ 必須）。classifier から 3.8 / 3.9 を削除。CI マトリクスを 3.10〜3.12 に変更。

### セキュリティ
- Python 3.8 / 3.9 で残存していた既知脆弱性（`requests` の CVE-2026-25645、`urllib3` の CVE-2026-44431 / CVE-2026-44432）を、サポートを 3.10+ に統一することで完全に解消。`SECURITY.md` の残存リスク記載を更新。

## [0.2.0] - 2026-06-04

### 追加
- 公式API更新（2026/04）への対応
  - `Message` に `record` フィールドを追加（`method_cd` が `record` の応対メモに紐づく顧客情報。顧客情報が紐づかない場合は `None`）。新規 `Record` モデル（`customer_id` / `customer_name` / `customer_emails` / `customer_tels`）を追加
  - R-Messe（`RMesse`）に `social_gift_user_type` フィールドを追加（ソーシャルギフトのユーザー種別: `"注文者"` / `"受取人"` / `None`）
- 型情報の配布: PEP 561 準拠の `py.typed` マーカーを追加（利用側で mypy/Pyright が型を認識可能に）
- GitHub Actions による CI を追加（Python 3.8〜3.12 マトリクスで flake8 / black / isort / mypy / pytest を実行）
- メール送信系（`send` / `reply` / `draft`）に `status_cd`・`pending_reason_id` パラメータを追加
- 全件取得用の `iter_all()` ジェネレータを追加（`customers` / `tickets` / `users` / `labels` / `templates` / `badges` / `case_categories` / `mail_accounts` の各リソース。ページネーションを透過的に処理）
- レートリミット情報を `client.last_rate_limit` として公開（`limit` / `remaining` / `reset`。レスポンスヘッダから取得）
- `RelationClient` をコンテキストマネージャ対応にし、`close()` メソッドを追加（HTTPセッションの明示的クローズ）
- 全モデルに `to_dict()` を追加（`from_dict` ↔ `to_dict` のラウンドトリップ対応）
- 例外 `PermissionError` を `RelationPermissionError` にリネーム（Python 組込みとの衝突を回避）。旧名は後方互換エイリアスとして維持。例外クラスをトップレベル（`relation_client`）からエクスポート
- OpenAPI 3.0 仕様を単一ソースとして扱う仕組みを追加（`scripts/sync_openapi.py` で公式仕様を取得、`spec/` 配下に同期。整合性テスト `test_openapi_consistency.py` を追加。仕様未同期時はスキップ）

### セキュリティ
- **subdomain を検証**（#2）: `RelationClient` 初期化時に `subdomain` を単一DNSラベルとして検証し、`Authorization: Bearer` トークンが意図しないホストへ送信されるのを防止（不正値は `ValueError`）
- **パスパラメータの URL エンコード**（#5）: `CustomerResource` の `email` / `system_id1` を `urllib.parse.quote` でエンコードし、パス／クエリの変形を防止
- **依存脆弱性対応**（#3）: `requests` を環境マーカーで Python 別に最も安全なバージョンへ（3.10+: `>=2.33.0` / 3.8・3.9: `>=2.32.4`）。`SECURITY.md` を新設し方針と残存リスクを明文化。CI に `pip-audit` 依存監査ジョブを追加
- **README 添付ダウンロード例の安全化**（#4）: API 由来の `file_name` を `os.path.basename` で正規化し保存先を限定（パストラバーサル対策）。`raise_for_status()`・`timeout` を追加
- `.gitignore` に `.praeco/`（ローカルツールキャッシュ）を追加し誤コミットを防止

### 修正
- **メール送信が失敗する不具合を修正**: `MailResource.send()` のエンドポイントが誤って `{message_box_id}/mails/send` になっていたため、正しい `{message_box_id}/mails` に修正。必須フィールド `status_cd` の欠落も修正
- ネットワークエラー時のリトライを冪等メソッド（GET / DELETE）のみに限定。POST / PUT はタイムアウト時にメール二重送信などの副作用が重複する恐れがあるためリトライしないよう修正

### 変更
- サポート対象 Python を 3.8 以上に更新（3.6 / 3.7 は EOL のため除外）。classifier に 3.11 / 3.12 を追加
- テストスイートを実装・公式仕様に整合（応対メモ作成パス `{message_box_id}/records`、チケット更新・検索のテスト修正）。全テストが green
- パッケージングを `pyproject.toml`（PEP 621）へ移行（`setup.py` は薄いシムとして維持。バージョンは `__init__.py` を単一ソースとして動的解決）
- `models.py` の日時パース処理を `_parse_dt()` ヘルパーへ共通化し重複を削減（約55行削減）
- ドキュメントをリポジトリ直下の `docs/` に一本化（`relation_client/docs/` の重複を解消し、誘導用 README を配置）

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
- Changes for the next release will be documented here

## [0.3.1] - 2026-06-04

### Misc
- Maintenance release. No functional or API changes.
- Validates the automated release pipeline (PyPI Trusted Publisher / GitHub Actions OIDC).

## [0.3.0] - 2026-06-04

### Changed (Breaking)
- **Dropped support for Python 3.8 / 3.9**; raised `requires-python` to `>=3.10`. Use `0.2.x` if you need 3.8 / 3.9.
- Removed environment markers from the dependency declaration and require fixed versions directly: `requests>=2.33.0` and `urllib3>=2.7.0` (both require Python 3.10+). Removed 3.8 / 3.9 classifiers. CI matrix changed to 3.10–3.12.

### Security
- Fully resolved the vulnerabilities that remained on Python 3.8 / 3.9 (`requests` CVE-2026-25645; `urllib3` CVE-2026-44431 / CVE-2026-44432) by standardizing on Python 3.10+. Updated the residual-risk notes in `SECURITY.md`.

## [0.2.0] - 2026-06-04

### Added
- Support for the official API update (2026/04)
  - Added the `record` field to `Message` (customer info attached to record memos where `method_cd` is `record`; `None` when no customer is linked). Added a new `Record` model (`customer_id` / `customer_name` / `customer_emails` / `customer_tels`)
  - Added the `social_gift_user_type` field to R-Messe (`RMesse`) — the social gift user type: `"注文者"` / `"受取人"` / `None`
- Type distribution: added a PEP 561 `py.typed` marker so downstream mypy/Pyright pick up the package's types
- GitHub Actions CI (runs flake8 / black / isort / mypy / pytest across a Python 3.8–3.12 matrix)
- Added `status_cd` and `pending_reason_id` parameters to the mail `send` / `reply` / `draft` methods
- Added `iter_all()` generators that transparently page through all results (`customers` / `tickets` / `users` / `labels` / `templates` / `badges` / `case_categories` / `mail_accounts`)
- Exposed rate-limit info as `client.last_rate_limit` (`limit` / `remaining` / `reset`, parsed from response headers)
- `RelationClient` is now a context manager and gained a `close()` method (explicit HTTP session shutdown)
- Added `to_dict()` to all models (round-trips with `from_dict`)
- Renamed the `PermissionError` exception to `RelationPermissionError` (avoids shadowing the Python builtin); the old name is kept as a backward-compatible alias. Exception classes are now exported from the top-level `relation_client` package
- Added tooling to treat the OpenAPI 3.0 spec as the single source of truth (`scripts/sync_openapi.py` syncs the official spec into `spec/`; `test_openapi_consistency.py` validates against it, skipping when not synced)

### Fixed
- **Mail sending failure**: `MailResource.send()` used the wrong endpoint `{message_box_id}/mails/send`; corrected to `{message_box_id}/mails`, and fixed the missing required `status_cd` field
- Network-error retries are now limited to idempotent methods (GET / DELETE). POST / PUT are no longer retried on timeout, preventing duplicate side effects such as sending the same email twice

### Changed
- Minimum supported Python raised to 3.8 (3.6 / 3.7 are EOL); added 3.11 / 3.12 classifiers
- Reconciled the test suite with the implementation and official spec (record-creation path `{message_box_id}/records`, ticket update/search tests). All tests pass
- Migrated packaging to `pyproject.toml` (PEP 621); `setup.py` is now a thin shim, version single-sourced from `__init__.py`
- Consolidated the datetime parsing in `models.py` into a `_parse_dt()` helper (~55 lines removed)
- Unified documentation under the repo-root `docs/` (removed the duplicate `relation_client/docs/`, left a pointer README)

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