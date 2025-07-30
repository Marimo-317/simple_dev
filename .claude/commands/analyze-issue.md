# Analyze Issue Command

AI-powered GitHub issue analysis with intelligent task extraction, complexity estimation, and agent assignment recommendations.

## Behavior

- Uses advanced NLP techniques to parse GitHub issue content
- Extracts actionable tasks with detailed breakdown and dependencies
- Estimates complexity using story points and confidence scoring
- Automatically assigns appropriate specialized agents to tasks
- Identifies critical path and implementation recommendations
- Generates comprehensive analysis reports with multiple output formats

## Usage

```bash
/analyze-issue [ISSUE_NUMBER] [OPTIONS]
```

### Parameters

- `ISSUE_NUMBER`: GitHub issue number to analyze (required)
- `--format|-f`: Output format (json, markdown, summary) - default: markdown
- `--output|-o`: Save analysis to file instead of displaying
- `--create-subtasks`: Automatically create GitHub sub-issues for complex tasks
- `--assign-agents`: Automatically assign recommended agents to tasks
- `--verbose|-v`: Enable detailed analysis output

### Examples

```bash
# Analyze issue with markdown report
/analyze-issue 123 --format markdown

# Generate JSON analysis and save to file
/analyze-issue 456 --format json --output analysis-456.json

# Analyze and create sub-issues automatically
/analyze-issue 789 --create-subtasks --assign-agents

# Quick summary analysis
/analyze-issue 101 --format summary --verbose
```

## Analysis Components

### Task Extraction

- **Smart Parsing**: Identifies tasks from various formats (checkboxes, numbered lists, user stories)
- **Content Analysis**: Extracts acceptance criteria, technical requirements, and dependencies
- **Type Classification**: Categorizes tasks as feature, bug, testing, documentation, or refactoring
- **Priority Assessment**: Determines task priority based on content and context

### Complexity Estimation

- **Story Points**: 1-13 scale based on multiple complexity factors
- **Time Estimates**: Hours estimation using story point conversion
- **Confidence Scoring**: Reliability assessment based on information completeness
- **Complexity Factors**: Detailed breakdown of what drives complexity

### Agent Assignment

- **Skill Matching**: Analyzes task requirements against agent capabilities
- **Multi-Agent Coordination**: Identifies when multiple agents are needed
- **Rationale**: Explains why specific agents were selected
- **Required Skills**: Lists technical skills needed for successful completion

### Dependency Analysis

- **Task Dependencies**: Identifies what each task depends on or blocks
- **External Dependencies**: Detects third-party or system dependencies
- **Related Issues**: Links to connected GitHub issues
- **Critical Path**: Identifies sequence-critical tasks

## Output Formats

### Markdown Report

```markdown
# Issue Analysis Report: #123

**Title:** User Authentication System
**Quality Score:** 85.3/100

## Task Breakdown

### Task 1: Implement JWT Authentication

- **Type:** feature
- **Priority:** high
- **Estimate:** 5 points (20.0h)
- **Assigned Agent:** security-auditor

**Acceptance Criteria:**

- [ ] User can login with email/password
- [ ] JWT tokens expire after 24 hours
- [ ] Refresh token mechanism implemented

**Technical Requirements:**

- Use bcrypt for password hashing
- Implement rate limiting for login attempts
```

### JSON Output

```json
{
  "issue_number": 123,
  "title": "User Authentication System",
  "tasks": [
    {
      "id": "task-1",
      "title": "Implement JWT Authentication",
      "estimate": {
        "story_points": 5,
        "hours_estimate": 20.0,
        "confidence": 85.0
      },
      "agent_assignment": {
        "primary_agent": "security-auditor",
        "secondary_agents": ["backend-architect"],
        "rationale": "Security focus required"
      }
    }
  ]
}
```

### Summary Format

```
Issue #123: User Authentication System

Summary:
- 4 tasks identified
- 18 story points total
- 72.0 hours estimated
- Quality score: 85.3/100

Primary agents needed:
- security-auditor
- backend-architect
- test-automator
```

## Quality Assessment

The analysis includes a quality score (0-100) based on:

### Completeness (40 points)

- Presence of clear tasks and requirements
- Detailed acceptance criteria
- Technical specifications included

### Clarity (30 points)

- Clear task descriptions
- User story format usage
- Unambiguous requirements

### Feasibility (30 points)

- Realistic complexity estimates
- Manageable risk levels
- Clear implementation path

## Integration with Workflow

### Automatic Sub-Issue Creation

When `--create-subtasks` is used:

- Complex tasks (>5 story points) are broken into smaller sub-issues
- Each sub-issue links back to the parent issue
- Appropriate labels and assignments are applied
- Dependencies are maintained across sub-issues

### Agent Coordination

The analysis coordinates with existing agents:

- **issue-analyst**: Provides the core analysis engine
- **workflow-orchestrator**: Manages multi-agent task coordination
- **requirements-analyst**: Validates requirement completeness
- **Specialized agents**: Receive task assignments with context

### CI/CD Integration

Analysis results can trigger automated workflows:

- **GitHub Actions**: Auto-assign agents based on analysis
- **Project Management**: Update sprint planning with estimates
- **Quality Gates**: Block issues with low quality scores
- **Notification Systems**: Alert stakeholders of high-complexity issues

## Advanced Features

### Pattern Recognition

The analyzer recognizes common patterns:

- **Epic Breakdown**: Large features split into manageable tasks
- **Bug Report Analysis**: Root cause identification from symptoms
- **Performance Requirements**: Benchmark and optimization needs
- **Security Considerations**: Threat modeling and compliance needs

### Historical Learning

The system improves over time by:

- **Accuracy Tracking**: Comparing estimates to actual completion times
- **Pattern Learning**: Identifying successful task breakdown approaches
- **Agent Performance**: Optimizing agent assignments based on outcomes
- **Quality Improvement**: Refining quality scoring based on feedback

### Risk Assessment

Each task includes risk analysis:

- **Technical Risks**: Implementation complexity and unknowns
- **Dependencies**: External system or team coordination needs
- **Timeline Risks**: Potential delays and bottlenecks
- **Quality Risks**: Testing and validation challenges

This command transforms unstructured issue descriptions into actionable, well-estimated development plans with intelligent agent coordination.
