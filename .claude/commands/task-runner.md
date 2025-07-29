# Claude Task Runner Command

Execute tasks with context isolation and Boomerang approach for large projects.

## Behavior

- Breaks down complex tasks into manageable, isolated contexts
- Provides real-time progress tracking with Textual dashboard
- Integrates with existing 45+ agent system for specialized execution
- Overcomes context length limitations through intelligent task splitting
- Maintains task state and execution history

## Available Commands

### Create Project

Creates a new task runner project from a markdown task list.

**Usage**: `/task-runner create PROJECT_NAME TASK_LIST_PATH`

**Example**: `/task-runner create refactor-auth docs/tasks/auth-refactor.md`

### Run Tasks

Executes tasks with optional Textual dashboard for visual progress tracking.

**Usage**: `/task-runner run PROJECT_NAME [--no-textual]`

**Example**: `/task-runner run refactor-auth`

### Status Check

Shows status of all task runner projects.

**Usage**: `/task-runner status`

### Cleanup

Cleans up any running task runner processes.

**Usage**: `/task-runner clean`

## Task List Format

Create markdown files with the following structure:

```markdown
# Project Name

## Task 1: Component Analysis

- Analyze existing authentication components
- Identify security vulnerabilities
- Document current architecture patterns

## Task 2: Database Schema Update

- Design new user table structure
- Create migration scripts
- Update existing queries

## Task 3: API Endpoint Refactoring

- Refactor login endpoint
- Update password reset flow
- Implement OAuth2 integration

## Task 4: Testing & Validation

- Create comprehensive test suite
- Perform security audit
- Update documentation
```

## Integration with Existing Agents

Task Runner automatically leverages your 45+ specialized agents:

- **python-pro**: For Python code refactoring tasks
- **security-auditor**: For security-related validation
- **test-automator**: For test creation and execution
- **database-optimizer**: For database-related tasks
- **frontend-developer**: For UI component updates

## Context Management

- **Boomerang Mode**: Large tasks are broken into focused subtasks
- **Isolation**: Each subtask runs in its own context to prevent information overflow
- **Integration**: Results are intelligently merged back into the main project
- **State Persistence**: Task progress is maintained across sessions

## Real-time Monitoring

- **Textual Dashboard**: Visual progress tracking with rich terminal interface
- **Live Updates**: Real-time streaming of task execution output
- **Error Handling**: Immediate notification of task failures with detailed logs
- **Intervention**: Ability to pause, resume, or modify running tasks

## Best Practices

1. **Task Granularity**: Break large features into 5-10 focused subtasks
2. **Clear Descriptions**: Use specific, actionable task descriptions
3. **Agent Hints**: Include hints about which agents should handle specific tasks
4. **Dependencies**: Order tasks to handle dependencies logically
5. **Validation**: Include verification steps in each task

## Example Workflows

### Large Feature Development

```bash
# Create task list for new feature
/task-runner create user-dashboard docs/tasks/dashboard-feature.md

# Run with visual dashboard
/task-runner run user-dashboard

# Monitor progress and intervene if needed
/task-runner status
```

### Legacy Code Refactoring

```bash
# Break down refactoring into manageable chunks
/task-runner create legacy-refactor docs/tasks/payment-system-refactor.md

# Execute with specialized agents
/task-runner run legacy-refactor
```

### Security Audit Implementation

```bash
# Comprehensive security review
/task-runner create security-audit docs/tasks/security-hardening.md

# Run with security-auditor integration
/task-runner run security-audit
```
