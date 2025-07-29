# Smart Commit Command

Creates well-formatted commits with conventional commit messages and emoji.

## Behavior

- Runs pre-commit checks (linting, building, docs generation)
- Auto-stages files if needed
- Generates conventional commit messages with appropriate emoji
- Suggests commit splitting for multiple logical changes
- Follows atomic commit philosophy

## Commit Format

Uses conventional commits with emoji mapping:

- ✨ feat: new features
- 🐛 fix: bug fixes
- 📝 docs: documentation changes
- 💄 style: formatting, missing semicolons, etc.
- ♻️ refactor: code changes that neither fix bugs nor add features
- ⚡ perf: performance improvements
- ✅ test: adding or correcting tests
- 🔧 chore: maintenance tasks, dependency updates
- 🚀 ci: CI/CD configuration changes
- 🔒 security: security fixes
- 🌐 i18n: internationalization
- 💥 breaking: breaking changes

## Pre-commit Workflow

1. Run linting checks
2. Run tests if applicable
3. Build documentation if needed
4. Stage necessary files
5. Create atomic commits with descriptive messages
6. Ensure each commit represents a single logical change

## Guidelines

- Split complex changes into multiple logical commits
- Each commit should be independently understandable
- Use present tense for commit messages
- Include scope when appropriate: `feat(auth): add login validation`
- Reference issue numbers when applicable: `fix: resolve login issue (#123)`
