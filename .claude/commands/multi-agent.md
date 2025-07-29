# Multi-Agent Orchestration Command

Coordinate multiple specialized agents for complex development tasks.

## Behavior

- Automatically selects and coordinates appropriate agents for complex tasks
- Provides context isolation through Task Runner integration
- Enables parallel agent workflows within Windows environment
- Maintains agent specialization while ensuring task coordination

## Agent Categories

### Language Specialists

- **python-pro**: Python development, refactoring, optimization
- **javascript-pro**: Modern JavaScript, Node.js, browser APIs
- **golang-pro**: Go development, concurrency patterns
- **rust-pro**: Systems programming, memory safety
- **sql-pro**: Database queries, schema design

### Architecture & Infrastructure

- **backend-architect**: API design, system architecture
- **frontend-developer**: UI/UX, responsive design
- **cloud-architect**: Infrastructure design, scalability
- **devops-troubleshooter**: Production issues, deployments

### Quality & Security

- **security-auditor**: Vulnerability assessment, OWASP compliance
- **code-reviewer**: Code quality, maintainability
- **test-automator**: Test strategy, automation
- **performance-engineer**: Optimization, bottlenecks

## Orchestration Patterns

### Sequential Workflow

```
Task → Agent A → Agent B → Agent C → Integration
```

**Example**: Feature Development

1. backend-architect: Design API endpoints
2. python-pro: Implement backend logic
3. frontend-developer: Create UI components
4. test-automator: Build test suite
5. security-auditor: Security review

### Parallel Execution (via Task Runner)

```
Task Breakdown:
├── Subtask A → Agent 1 (isolated context)
├── Subtask B → Agent 2 (isolated context)
└── Subtask C → Agent 3 (isolated context)
```

**Example**: Code Refactoring

- Context A: python-pro refactors backend
- Context B: frontend-developer updates UI
- Context C: security-auditor reviews changes

### Review & Validation Chain

```
Primary Agent → Review Agent → Validation Agent
```

**Example**: Security Implementation

1. python-pro: Implement authentication
2. security-auditor: Security review
3. test-automator: Security testing

## Usage Patterns

### Complex Feature Development

```bash
# Use Task Runner for context isolation
/task-runner create feature-auth docs/tasks/auth-system.md

# Agents automatically selected per task:
# - backend-architect for system design
# - python-pro for implementation
# - security-auditor for review
# - test-automator for validation
```

### Multi-Domain Refactoring

```bash
# Create isolated contexts for different domains
/task-runner create refactor-system docs/tasks/system-refactor.md

# Parallel execution in isolated contexts:
# - python-pro: Backend refactoring
# - javascript-pro: Frontend updates
# - database-optimizer: Schema changes
```

### Security-First Development

```bash
# Security-aware development workflow
/multi-agent security-hardening project-name

# Automatic workflow:
# 1. security-auditor: Initial assessment
# 2. Appropriate specialist: Implementation
# 3. security-auditor: Final review
```

## Integration with Task Runner

### Context Isolation Benefits

- Each agent works in focused, isolated context
- No context pollution between different domains
- Specialized knowledge preserved per agent
- Results intelligently merged

### Boomerang Approach

```
Large Task
    ↓
Task Breakdown (5-7 subtasks)
    ↓
Isolated Agent Execution
    ├── python-pro (Context A)
    ├── security-auditor (Context B)
    └── test-automator (Context C)
    ↓
Result Integration
    ↓
Unified Output
```

## Agent Selection Logic

### Automatic Selection

Agents are automatically selected based on:

- File types and languages involved
- Task keywords (security, performance, testing)
- Project context from CLAUDE.md
- Previous task outcomes

### Explicit Selection

```bash
# Specify agents for specific tasks
/multi-agent --agents="python-pro,security-auditor" secure-api-refactor

# Force specific orchestration pattern
/multi-agent --pattern=sequential database-migration
```

## Monitoring & Progress

### Real-time Tracking

- Textual dashboard shows agent progress
- Context isolation status
- Task completion rates
- Error handling and recovery

### Agent Coordination

- Dependency management between agents
- Conflict resolution for overlapping changes
- State synchronization across contexts

## Best Practices

### Task Granularity

1. Break complex features into 5-7 focused subtasks
2. Assign one primary agent per subtask
3. Include review/validation steps
4. Plan integration points

### Agent Utilization

1. **Leverage specialization**: Use domain experts for their areas
2. **Review patterns**: Always include review agents for quality
3. **Context preservation**: Keep related tasks in same context when possible
4. **Progressive refinement**: Start broad, narrow down with specialized agents

### Quality Assurance

1. **Multi-layer review**: Primary agent → Review agent → Validation
2. **Cross-domain validation**: Security + Performance + Functionality
3. **Integration testing**: Ensure agent outputs work together
4. **Documentation**: Capture agent decisions and rationale

## Example Workflows

### E-commerce Feature

```markdown
# Task: Implement payment processing system

## Subtasks:

1. **backend-architect**: Design payment API endpoints
2. **python-pro**: Implement payment logic
3. **security-auditor**: Review payment security
4. **frontend-developer**: Create payment UI
5. **test-automator**: Build payment tests
6. **devops-troubleshooter**: Setup payment monitoring
```

### Security Audit

```markdown
# Task: Comprehensive security review

## Subtasks:

1. **security-auditor**: Initial vulnerability scan
2. **code-reviewer**: Code quality assessment
3. **python-pro**: Fix backend vulnerabilities
4. **javascript-pro**: Fix frontend issues
5. **test-automator**: Security test suite
6. **security-auditor**: Final validation
```

This approach provides Container Use-like benefits while maintaining full Windows compatibility and leveraging your existing 45+ agent infrastructure.
