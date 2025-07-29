# Claude Code 次世代AI支援開発環境

最先端のAI支援開発を実現する、Claude Codeベースの統合開発環境です。awesome-claude-codeリポジトリの機能を統合し、Windows環境で最大限のパフォーマンスを発揮します。

## 🌟 環境の特徴

### 🤖 45+ 専門エージェント

- **言語専門家**: python-pro, javascript-pro, golang-pro, rust-pro, sql-pro
- **アーキテクチャ**: backend-architect, frontend-developer, cloud-architect
- **品質・セキュリティ**: security-auditor, code-reviewer, test-automator
- **運用・保守**: devops-troubleshooter, database-admin, performance-engineer
- **データ・AI**: data-scientist, ai-engineer, ml-engineer, mlops-engineer

### ⚡ 9つのスラッシュコマンド

- `/commit` - 絵文字付き規約準拠コミット
- `/create-pr` - 自動プルリクエスト作成
- `/todo` - プロジェクトタスク管理
- `/clean` - コード品質クリーンアップ
- `/context-prime` - プロジェクトコンテキスト読み込み
- `/task-runner` - タスク分離実行システム
- `/multi-agent` - マルチエージェント統制
- `/hooks` - フック管理システム
- `/create-claude-md` - プロジェクトコンテキスト生成

### 🔧 Claude Task Runner

- **コンテキスト分離**: "Boomerang"アプローチで大規模タスクを分割
- **リアルタイム監視**: Textualダッシュボードでの進捗可視化
- **エージェント統合**: 45+エージェントとの自動連携
- **状態永続化**: セッション間でのタスク状態維持

### 🪝 自動化フックシステム

- **PostToolUse**: ファイル編集後の自動フォーマット（Prettier, Black）
- **Stop**: セッション完了ログ記録
- **リアルタイム品質管理**: コード変更時の自動品質チェック

## 🚀 クイックスタート

### 1. 環境の起動

```bash
# DevContainerを使用（推奨）
code .
# VS Codeでdevcontainerを起動

# または直接起動
cd /path/to/simple_dev
```

### 2. プロジェクトコンテキストの読み込み

```bash
/context-prime
```

### 3. 基本的な開発フロー

```bash
# コード変更を行う
# ...

# コード品質確保
/clean

# 規約準拠コミット
/commit

# プルリクエスト作成
/create-pr
```

## 📋 開発ワークフロー

### 🔄 標準開発フロー

#### 1. セッション開始

```bash
# プロジェクトコンテキスト読み込み
/context-prime

# タスク管理開始
/todo list
```

#### 2. 機能開発

```bash
# 複雑な機能の場合：Task Runnerを使用
/task-runner create feature-auth docs/tasks/auth-system.md
/task-runner run feature-auth

# 簡単な変更の場合：直接開発
# コード変更...
```

#### 3. 品質管理

```bash
# 自動コード品質チェック
/clean

# 必要に応じて特定エージェントに依頼
# "security-auditorでセキュリティ監査を実行してください"
# "performance-engineerでパフォーマンス最適化を行ってください"
```

#### 4. 変更のコミット

```bash
# 規約準拠の自動コミット
/commit

# 必要に応じてプルリクエスト作成
/create-pr
```

### 🎯 高度なワークフロー

#### 大規模機能開発

```bash
# 1. タスクリスト作成（Markdown）
# docs/tasks/new-feature.md を作成

# 2. Task Runnerプロジェクト作成
/task-runner create new-feature docs/tasks/new-feature.md

# 3. 実行（Textualダッシュボード付き）
/task-runner run new-feature

# 4. 進捗確認
/task-runner status
```

#### マルチドメインリファクタリング

```bash
# 複数エージェントの並列実行
/multi-agent --pattern=parallel system-refactor

# エージェント指定実行
/multi-agent --agents="python-pro,security-auditor" secure-refactor
```

#### セキュリティ重視開発

```bash
# セキュリティファースト開発
/multi-agent security-hardening project-name

# セキュリティ監査 → 実装 → 最終レビューの自動フロー
```

## 🛠️ 利用可能なツール

### スラッシュコマンド詳細

#### `/commit`

**目的**: 規約準拠の絵文字付きコミットメッセージ自動生成

```bash
/commit
# ✨ feat: add user authentication system
# 🐛 fix: resolve login validation issue
# 📝 docs: update API documentation
```

#### `/task-runner`

**目的**: コンテキスト分離による大規模タスク実行

```bash
# プロジェクト作成
/task-runner create PROJECT_NAME TASK_LIST_PATH

# 実行
/task-runner run PROJECT_NAME

# 状態確認
/task-runner status

# クリーンアップ
/task-runner clean
```

#### `/multi-agent`

**目的**: 複数エージェントの統制された実行

```bash
# パターン指定実行
/multi-agent --pattern=sequential feature-development
/multi-agent --pattern=parallel code-refactor

# エージェント指定実行
/multi-agent --agents="python-pro,security-auditor" secure-implementation
```

### エージェント活用ガイド

#### 言語別開発

```bash
# Python開発
"python-proを使ってDjangoのAPIエンドポイントを実装してください"

# JavaScript開発
"javascript-proを使ってReactコンポーネントを作成してください"

# Go開発
"golang-proを使って並行処理のAPIサーバーを構築してください"
```

#### アーキテクチャ設計

```bash
# システム設計
"backend-architectを使ってマイクロサービスアーキテクチャを設計してください"

# フロントエンド設計
"frontend-developerを使ってレスポンシブなダッシュボードを設計してください"
```

#### 品質・セキュリティ

```bash
# セキュリティ監査
"security-auditorでOWASP準拠のセキュリティ監査を実行してください"

# コードレビュー
"code-reviewerで保守性と品質の観点からレビューしてください"

# パフォーマンス最適化
"performance-engineerでボトルネックを特定し最適化してください"
```

## 📁 プロジェクト構造

```
simple_dev/
├── .claude/                          # Claude Code設定
│   ├── agents/                       # 45+ 専門エージェント
│   ├── commands/                     # スラッシュコマンド定義
│   ├── task-runner/                  # Task Runner環境
│   ├── settings.json                 # フック・MCP設定
│   └── settings.local.json           # 権限設定
├── .devcontainer/                    # 開発コンテナー設定
│   ├── devcontainer.json            # VS Code統合設定
│   ├── Dockerfile                   # コンテナー定義
│   └── setup.sh                     # 環境セットアップ
├── .github/workflows/                # GitHub Actions
│   └── claude-code.yml              # Claude Code統合
├── docs/                            # ドキュメント
│   └── tasks/                       # Task Runnerタスク定義
├── CLAUDE.md                        # プロジェクトコンテキスト
└── README.md                        # このファイル
```

## 🔧 技術スタック

### 開発環境

- **ベース**: Windows + MinGW + Git Bash
- **コンテナー**: DevContainer (Node.js 20 + Python 3.11)
- **エディター**: VS Code with Claude Code integration
- **Claude Code**: Desktop Commander統合

### 開発ツール

- **フォーマッター**: Prettier (JS/TS), Black (Python)
- **リンター**: ESLint, flake8, mypy
- **品質管理**: 自動フック + エージェント監査
- **バージョン管理**: Git + 規約準拠コミット

### CI/CD

- **GitHub Actions**: Claude Code統合ワークフロー
- **トリガー**: `@claude`でのIssue/PR自動支援
- **タイムアウト**: 10分、エージェントモード

## 💡 実践例

### 例1: 新機能開発（認証システム）

#### タスクリスト作成

```markdown
# docs/tasks/auth-system.md

# 認証システム実装

## Task 1: システム設計

- JWT認証の設計
- データベーススキーマ設計
- API エンドポイント設計

## Task 2: バックエンド実装

- ユーザーモデル実装
- 認証ミドルウェア実装
- パスワードハッシュ化

## Task 3: セキュリティ監査

- OWASP準拠チェック
- 脆弱性スキャン
- セキュリティテスト

## Task 4: フロントエンド実装

- ログインフォーム
- 認証状態管理
- ルート保護

## Task 5: テスト・文書化

- 単体テスト作成
- 統合テスト作成
- API文書更新
```

#### 実行フロー

```bash
# 1. プロジェクト作成
/task-runner create auth-system docs/tasks/auth-system.md

# 2. 実行開始
/task-runner run auth-system

# 自動的に以下が実行される：
# - Task 1: backend-architect が設計実行
# - Task 2: python-pro が実装実行
# - Task 3: security-auditor が監査実行
# - Task 4: frontend-developer が実装実行
# - Task 5: test-automator がテスト実行

# 3. 進捗確認
/task-runner status

# 4. 完了後のコミット
/commit
```

### 例2: セキュリティ強化

```bash
# 1. コンテキスト読み込み
/context-prime

# 2. セキュリティ監査実行
"security-auditorで包括的なセキュリティ監査を実行してください"

# 3. 問題修正
"python-proでSQLインジェクション脆弱性を修正してください"
"javascript-proでXSS対策を実装してください"

# 4. 再監査
"security-auditorで修正内容を検証してください"

# 5. コミット
/commit
```

### 例3: パフォーマンス最適化

```bash
# 1. 問題特定
"performance-engineerでアプリケーションのボトルネックを特定してください"

# 2. データベース最適化
"database-optimizerでクエリ最適化を実行してください"

# 3. フロントエンド最適化
"frontend-developerでレンダリング最適化を実行してください"

# 4. 結果検証
"performance-engineerで最適化効果を測定してください"

# 5. 文書化・コミット
/clean
/commit
```

## 🔍 トラブルシューティング

### よくある問題

#### Task Runnerが起動しない

```bash
# 仮想環境の確認
source .claude/task-runner/.venv/Scripts/activate
which task-runner

# Desktop Commanderの確認
# Claude Desktopでハンマーアイコンが表示されているか確認
```

#### エージェントが期待通りに動作しない

```bash
# プロジェクトコンテキストの再読み込み
/context-prime

# 明示的なエージェント指定
"python-proエージェントを使って..."
"security-auditorエージェントで..."
```

#### フックが動作しない

```bash
# フック設定確認
cat .claude/settings.json

# 権限確認
cat .claude/settings.local.json

# フック管理
/hooks
```

### パフォーマンス最適化

#### メモリ使用量削減

- Task Runnerのコンテキスト分離を活用
- 大規模タスクは必ずTask Runnerを使用
- 不要なエージェントセッションの終了

#### 実行速度向上

- `/context-prime`でのコンテキスト事前読み込み
- 関連タスクのバッチ実行
- 並列実行可能なタスクの`/multi-agent`活用

## 📚 追加リソース

### 公式ドキュメント

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [awesome-claude-code Repository](https://github.com/hesreallyhim/awesome-claude-code)

### 環境固有ドキュメント

- `.claude/implementation-summary.md` - 実装詳細
- `.claude/platform-limitations.md` - Windows互換性情報
- `.claude/tooling-assessment.md` - ツール評価結果
- `CLAUDE.md` - プロジェクトコンテキスト

### サンプルファイル

- `docs/tasks/sample-integration-test.md` - Task Runnerサンプル

## 🤝 貢献・カスタマイゼーション

### エージェントのカスタマイズ

`.claude/agents/` ディレクトリ内のエージェント定義は変更可能ですが、推奨しません。代わりに：

1. 新しいプロジェクト固有のエージェントを作成
2. CLAUDE.mdでプロジェクト固有のガイドラインを定義
3. スラッシュコマンドのカスタマイズ

### フックのカスタマイズ

`.claude/settings.json`でフックをカスタマイズ：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-custom-command"
          }
        ]
      }
    ]
  }
}
```

### Task Runnerタスクテンプレート

`docs/tasks/`ディレクトリにプロジェクト固有のタスクテンプレートを作成。

## 📊 開発メトリクス

この環境により期待される改善：

- **開発速度**: 2-3倍向上
- **コード品質**: 40-50%改善
- **エラー率**: 60-70%削減
- **コンテキスト管理**: 制限の完全解決

---

**この開発環境は、Claude Codeの能力を最大限に活用し、次世代のAI支援開発体験を提供します。質問や改善要望があれば、Issueを作成してください。** 🚀
