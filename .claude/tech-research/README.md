# 🔬 技術仕様調査システム

Claude Code環境向けに最適化された体系的技術評価・選定システム

## 📋 概要

このシステムは、GitHub権限制約内で動作する高度な技術調査ワークフローです。Claude Code Sub Agents "Spec"技術の代替として設計され、既存の45+エージェントと連携して包括的な技術評価を提供します。

## 🎯 主要機能

### `/tech-spec` コマンド

- **単一技術評価**: 特定技術の詳細分析
- **比較分析**: 複数技術の並列評価
- **マイグレーション計画**: 技術移行戦略策定

### マルチエージェント協調

- **search-specialist**: GitHub-based技術調査
- **技術専門家**: 実装詳細分析
- **security-auditor**: セキュリティ評価
- **architect-review**: アーキテクチャ影響分析

### 自動化ワークフロー

- **品質ゲート**: 段階的評価検証
- **進捗監視**: リアルタイム状況追跡
- **レポート生成**: 構造化された推奨事項

## 📁 ファイル構成

```
.claude/tech-research/
├── README.md                           # このファイル
├── search-specialist-enhancement.md    # 検索機能拡張
├── agent-collaboration-patterns.md     # エージェント連携パターン
├── tech-workflow-orchestrator.md       # ワークフロー自動化
└── usage-guide.md                     # 完全使用ガイド
```

## 🚀 クイックスタート

### 基本的な技術評価

```bash
/tech-spec React 18
```

### 技術比較

```bash
/tech-spec "React vs Vue vs Svelte"
```

### マイグレーション計画

```bash
/tech-spec "migrate from Vue 2 to Vue 3"
```

## 📊 使用例

### フロントエンド技術選定

```bash
# 状態管理ライブラリ比較
/tech-spec "Redux vs Zustand vs Jotai"

# ビルドツール評価
/tech-spec "Vite vs Webpack vs Parcel"
```

### バックエンド技術評価

```bash
# フレームワーク比較
/tech-spec "FastAPI vs Django vs Flask"

# データベース選定
/tech-spec "PostgreSQL vs MongoDB"
```

### インフラ技術調査

```bash
# コンテナ化戦略
/tech-spec "Docker vs Podman"

# CI/CD選定
/tech-spec "GitHub Actions vs Azure DevOps"
```

## 🔧 設定とカスタマイゼーション

### 評価フォーカス指定

```bash
# セキュリティ重視
/tech-spec React 18 --focus=security

# パフォーマンス重視
/tech-spec "GraphQL vs REST" --focus=performance
```

### エージェント選択

```bash
# 特定エージェント指定
/tech-spec Next.js --agents="search-specialist,javascript-pro,security-auditor"

# 拡張評価
/tech-spec Docker --extended --include="devops-troubleshooter,cloud-architect"
```

## 📈 出力形式

### 技術仕様レポート

- **エグゼクティブサマリー**: 推奨事項概要
- **技術分析**: 実装詳細・性能評価
- **セキュリティ評価**: 脆弱性・リスク分析
- **アーキテクチャ影響**: システム統合評価
- **実装ロードマップ**: 段階的導入計画

### 比較マトリックス

| 評価項目       | 技術A      | 技術B      | 技術C    |
| -------------- | ---------- | ---------- | -------- |
| パフォーマンス | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 学習容易性     | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐   |
| エコシステム   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐⭐⭐ |

## 🎯 制約と最適化

### GitHub権限制約内の最適化

- **許可ドメイン**: api.github.com, raw.githubusercontent.com
- **情報源**: 公式リポジトリ, リリースノート, Issues/Discussions
- **検索戦略**: GitHub-specific検索クエリ最適化

### 品質保証

- **最小5GitHub源**: 信頼性確保
- **複数エージェント検証**: 交差検証による精度向上
- **構造化出力**: 一貫性のあるレポート形式

## 🔍 トラブルシューティング

### よくある問題

1. **不十分な調査結果**: より具体的な検索語句を使用
2. **エージェント競合**: 評価基準の明確化
3. **評価時間超過**: スコープの絞り込み

### 解決策

```bash
# 詳細調査
/tech-spec "React 18" --sources=extended

# 焦点調査
/tech-spec "React 18 security" --focus=security

# 段階的評価
/tech-spec React && /tech-spec "React 18 implementation"
```

## 📚 詳細ドキュメント

- **[完全使用ガイド](usage-guide.md)**: 詳細な使用方法とベストプラクティス
- **[エージェント連携パターン](agent-collaboration-patterns.md)**: 高度なワークフロー設計
- **[ワークフロー自動化](tech-workflow-orchestrator.md)**: オーケストレーション詳細
- **[検索機能拡張](search-specialist-enhancement.md)**: search-specialist最適化

---

🔬 **技術選定の科学的アプローチで、より良い開発決定を。**
