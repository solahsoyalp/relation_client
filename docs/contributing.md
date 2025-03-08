# 貢献ガイドライン

Re:lation API Python クライアントへの貢献を検討していただき、ありがとうございます。このガイドラインは、プロジェクトへの貢献をスムーズに行うための手順を説明します。

## 目次

- [行動規範](#行動規範)
- [はじめに](#はじめに)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [Issue報告](#issue報告)
- [プルリクエスト](#プルリクエスト)
- [コーディング規約](#コーディング規約)
- [テスト](#テスト)
- [ドキュメント](#ドキュメント)

## 行動規範

このプロジェクトは[Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)の行動規範に従います。プロジェクトに参加することにより、この規範に従うことに同意したものとみなされます。

## はじめに

1. プロジェクトをフォークする
2. リポジトリをクローンする
   ```bash
   git clone https://github.com/solahsoyalp/relation_client.git
   cd relation_client
   ```
3. 開発用の依存関係をインストールする
   ```bash
   pip install -e ".[dev]"
   ```

## 開発環境のセットアップ

1. Pythonの仮想環境を作成し、アクティベートする
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix系
   # または
   .\venv\Scripts\activate  # Windows
   ```

2. 依存関係をインストールする
   ```bash
   pip install -e ".[dev]"
   ```

3. pre-commitフックをインストールする
   ```bash
   pre-commit install
   ```

## Issue報告

バグを報告する場合は、以下の情報を含めてください：

- 使用しているPythonのバージョン
- 発生している問題の詳細な説明
- 問題を再現するための手順
- 期待される動作と実際の動作
- エラーメッセージやスタックトレース（該当する場合）

機能リクエストの場合は、以下の情報を含めてください：

- 新機能の詳細な説明
- ユースケースや具体的な使用例
- 既存の機能との関連性

## プルリクエスト

1. 新しい機能ブランチを作成する
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 変更を加える

3. テストを追加・更新し、すべてのテストが通ることを確認する
   ```bash
   pytest
   ```

4. コードスタイルを確認する
   ```bash
   flake8
   black .
   isort .
   ```

5. 変更をコミットする
   ```bash
   git commit -am "Add some feature"
   ```

6. 変更をプッシュする
   ```bash
   git push origin feature/your-feature-name
   ```

7. プルリクエストを作成する：https://github.com/solahsoyalp/relation_client/pulls

## コーディング規約

- [PEP 8](https://www.python.org/dev/peps/pep-0008/)に従う
- [Black](https://black.readthedocs.io/)コードフォーマッターを使用する
- [isort](https://pycqa.github.io/isort/)でインポートを整理する
- 適切なドキュメンテーション文字列を追加する
- 意味のある変数名とコメントを使用する

## テスト

- 新しい機能には必ずテストを追加する
- 既存のテストが壊れていないことを確認する
- テストカバレッジを維持する

テストの実行：
```bash
# すべてのテストを実行
pytest

# カバレッジレポートを生成
pytest --cov=relation_client tests/
```

## ドキュメント

- 新しい機能には適切なドキュメントを追加する
- READMEの更新が必要な場合は更新する
- コードのドキュメンテーション文字列を適切に維持する

---

*Read this in other languages: [English](contributing_en.md), [日本語](contributing.md)* 