# コントリビューションガイド

Re:lation API Python クライアントへのコントリビューションを検討いただき、ありがとうございます。このガイドラインでは、プロジェクトへの貢献方法について説明します。

## 開発環境のセットアップ

### リポジトリのクローン

まず、リポジトリをクローンし、開発環境をセットアップします：

```bash
git clone https://github.com/yourusername/relation-client.git
cd relation-client
```

### 依存関係のインストール

開発に必要な依存関係をインストールします：

```bash
pip install -e ".[dev]"
```

または、以下のコマンドでも同様の結果が得られます：

```bash
pip install -r requirements-dev.txt
```

## 開発ワークフロー

### ブランチの作成

新機能や修正を開発する場合は、メインブランチから新しいブランチを作成してください：

```bash
git checkout -b feature/your-feature-name
# または
git checkout -b fix/issue-description
```

### コーディング規約

このプロジェクトでは、以下のコーディング規約に従ってください：

- PEP 8スタイルガイドに準拠すること
- すべてのパブリックメソッドとクラスにはドキュメント文字列を記載すること
- コメントは日本語で記載すること
- 型ヒントを使用すること

### テストの実行

変更を加えた後は、必ずテストを実行してください：

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/test_ticket_resource.py

# テストカバレッジレポートを生成
pytest --cov=relation_client tests/
```

### コードスタイルのチェック

コードスタイルチェックを実行して、コーディング規約に準拠していることを確認してください：

```bash
flake8 relation_client tests
black --check relation_client tests
isort --check relation_client tests
```

スタイルの問題を自動修正するには：

```bash
black relation_client tests
isort relation_client tests
```

## プルリクエストの送信

### コミットメッセージのガイドライン

コミットメッセージは明確で具体的にしてください。以下のような形式を推奨します：

```
機能/修正の短い説明（50文字以下）

必要に応じて、より詳細な説明を記載してください。
行の長さは72文字程度に制限してください。

関連する課題がある場合は、その参照を含めてください：
関連: #123
修正: #456
```

### プルリクエストの作成

1. 変更をコミットし、ブランチにプッシュします：

```bash
git commit -am "機能追加: XXXを実装"
git push origin feature/your-feature-name
```

2. GitHubでプルリクエストを作成します。

3. プルリクエストのテンプレートに従って、変更内容を詳細に記述してください。

### レビュープロセス

プルリクエストは以下の基準でレビューされます：

- コードの品質とスタイル
- テストの有無と品質
- ドキュメントの更新
- 既存機能との互換性

レビューアからのフィードバックがあった場合は、それに対応してコードを修正し、変更をプッシュしてください。

## リリースプロセス

リリースは以下のプロセスで行われます：

1. バージョン番号の更新 (`__init__.py`内の`__version__`変数)
2. CHANGELOGの更新
3. ドキュメントの更新
4. タグの作成とリリース
5. PyPIへのパッケージのアップロード

## 行動規範

このプロジェクトでは、オープンで友好的な環境を維持するために、貢献者に対して以下を期待しています：

- お互いを尊重すること
- 建設的なフィードバックを提供すること
- 共感と理解をもって他者に接すること

## 質問や問題がある場合

質問や問題がある場合は、[GitHub Issues](https://github.com/yourusername/relation-client/issues)で報告してください。 