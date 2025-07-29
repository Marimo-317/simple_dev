# 📋 Project Configuration

Project: Claude Code Development Environment  
Version: 1.0  
Stack: Node.js 20 + Python 3.11 + DevContainer + GitHub Actions

## 🚨 CRITICAL RULES

- Never modify the existing 45+ specialized agents in `.claude/agents/` without explicit permission
- Always respect the permission settings in `.claude/settings.local.json`
- Use slash commands for common development tasks: `/commit`, `/create-pr`, `/todo`, `/clean`, `/context-prime`
- Hooks are configured for automatic formatting - let them handle code style
- Never push to remote without explicit user approval

## 🎯 PROJECT CONTEXT

- **Purpose**: Professional Claude Code development environment with advanced agent orchestration
- **Architecture**: DevContainer-based with VS Code integration
- **Languages**: JavaScript/TypeScript (Node.js 20), Python 3.11
- **Agent System**: 45+ specialized agents including language experts (python-pro, golang-pro, rust-pro) and role-based specialists (security-auditor, ai-engineer, devops-troubleshooter)
- **CI/CD**: GitHub Actions workflow with Claude Code integration (`@claude` trigger)
- **Development Tools**: Prettier, ESLint, GitLens, Black formatter, Tailwind CSS

## 🔧 DEVELOPMENT PATTERNS

**File Structure**:

- `.claude/agents/` - 45+ specialized subagents (DO NOT MODIFY)
- `.claude/commands/` - Slash commands for workflow automation
- `.claude/settings.json` - Hooks configuration for automation
- `.claude/settings.local.json` - Permission and security settings
- `.devcontainer/` - Complete development environment setup
- `.github/workflows/` - CI/CD automation with Claude Code integration

**Coding Standards**:

- Use existing agents for specialized tasks (e.g., python-pro for Python, security-auditor for security reviews)
- Code formatting handled automatically via PostToolUse hooks (Prettier, Black)
- Follow conventional commit messages (automatically handled by `/commit` command)
- Use TypeScript strict mode for new JavaScript code
- Prefer modern ES6+ syntax and patterns

**Agent Utilization**:

- Language tasks → Use specialized agents (python-pro, javascript-pro, etc.)
- Architecture decisions → Use architect-review, backend-architect
- Security concerns → Use security-auditor
- Performance issues → Use performance-engineer
- Debugging → Use debugger, error-detective

## 🚀 WORKFLOW AUTOMATION

**Available Slash Commands**:

- `/commit` - Smart Git commits with conventional messaging and emoji
- `/create-pr` - Automated pull request creation with proper formatting
- `/todo` - Project task management in todos.md
- `/clean` - Code quality cleanup (formatters, linters, type checkers)
- `/context-prime` - Load comprehensive project context
- `/hooks` - Manage and configure automation hooks

**Automated Hooks**:

- **PostToolUse**: Auto-format files with Prettier (JS/TS) and Black (Python)
- **Stop**: Log session completion timestamps
- **File Operations**: Automatic code quality enforcement

**GitHub Integration**:

- Use `@claude` in issues/PRs to trigger Claude Code assistance
- Workflow runs on issue comments, PR reviews, and new PRs/issues
- 10-minute timeout with agent mode for complex tasks

## 🔧 DEVELOPMENT COMMANDS

**DevContainer Commands**:

- Development environment is fully containerized
- Node.js 20 and Python 3.11 pre-installed
- VS Code extensions configured for optimal development
- Git and GitHub CLI integrated

**Common Workflows**:

1. Start development → `/context-prime` to load project context
2. Code changes → Hooks automatically format and validate
3. Commit changes → `/commit` for proper conventional commits
4. Create PR → `/create-pr` for automated PR workflow
5. Manage tasks → `/todo` for project task tracking

## 🧠 AGENT ORCHESTRATION

**Specialized Agents Available**:

- **Language Experts**: python-pro, javascript-pro, golang-pro, rust-pro, c-pro, cpp-pro, sql-pro
- **Architecture**: backend-architect, frontend-developer, cloud-architect, graphql-architect
- **Operations**: devops-troubleshooter, deployment-engineer, database-admin, terraform-specialist
- **Quality**: code-reviewer, security-auditor, test-automator, performance-engineer
- **Data & AI**: data-scientist, data-engineer, ai-engineer, ml-engineer, mlops-engineer
- **Specialized**: incident-responder, search-specialist, prompt-engineer

**Agent Selection Guidelines**:

- For Python code → Use python-pro agent
- For security reviews → Use security-auditor agent
- For performance issues → Use performance-engineer agent
- For complex debugging → Use debugger or error-detective agents
- For architecture decisions → Use architect-review agent

## 🔒 SECURITY & PERMISSIONS

**Configured Permissions** (settings.local.json):

- Bash commands: ls, find, mkdir operations
- WebFetch access: GitHub domains (api.github.com, raw.githubusercontent.com)
- File operations controlled through standard Claude Code permissions

**Security Practices**:

- Never expose sensitive configuration in commits
- Use security-auditor agent for security reviews
- Follow principle of least privilege for tool access
- Keep credentials in .claude/.credentials.json (git-ignored)

## 📊 MONITORING & ANALYTICS

**Session Tracking**:

- Stop hooks log completion timestamps
- GitHub Actions provide CI/CD visibility
- Agent usage automatically tracked through Claude Code

**Quality Metrics**:

- Code formatting enforced via hooks
- Conventional commits ensure readable history
- PR automation maintains consistent workflows
