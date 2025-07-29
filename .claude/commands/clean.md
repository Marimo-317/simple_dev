# Code Quality Cleanup Command

Addresses code formatting and quality issues systematically.

## Behavior

- Fixes code formatting problems
- Organizes imports properly
- Resolves linting issues
- Corrects type errors
- Ensures comprehensive code quality compliance

## For Python Projects

Runs the following tools in sequence:

1. **black** - Code formatting
2. **isort** - Import organization
3. **flake8** - Linting and style guide enforcement
4. **mypy** - Type checking

## For JavaScript/TypeScript Projects

Runs the following tools in sequence:

1. **prettier** - Code formatting
2. **eslint** - Linting and code quality
3. **typescript** - Type checking (if applicable)

## For Other Languages

Applies appropriate formatting and linting tools based on detected language:

- **Go**: gofmt, golint, go vet
- **Rust**: rustfmt, clippy
- **Java**: google-java-format, checkstyle
- **C/C++**: clang-format

## Process

1. Detect project language and tooling configuration
2. Run formatters first to fix style issues
3. Run linters to identify code quality problems
4. Run type checkers to catch type-related errors
5. Report any remaining issues that require manual intervention
6. Suggest fixes for common problems

## Configuration

Respects existing project configuration files:

- .black, pyproject.toml for Python
- .prettierrc, .eslintrc for JavaScript/TypeScript
- Existing formatter/linter configs for other languages
