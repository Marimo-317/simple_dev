# Create Issue Command

Automatically create GitHub issues from requirements documents using AI-powered analysis.

## Behavior

- Parses requirements documents (markdown format) to extract user stories and tasks
- Analyzes content using natural language processing to identify key components
- Creates properly formatted GitHub issues with templates and metadata
- Applies appropriate labels, priorities, and assignments automatically
- Supports dry-run mode for preview before creation

## Usage

```bash
/create-issue [REQUIREMENTS_FILE] [OPTIONS]
```

### Parameters

- `REQUIREMENTS_FILE`: Path to markdown file containing requirements/user stories
- `--priority|-p`: Issue priority (low, medium, high, critical) - default: medium
- `--assignee|-a`: GitHub username to assign issues to
- `--milestone|-m`: Milestone to assign issues to
- `--dry-run`: Preview issues without creating them
- `--batch-size|-b`: Number of issues to create at once - default: 5

### Examples

```bash
# Create issues from requirements document
/create-issue docs/requirements/user-auth.md --priority high

# Assign to specific user with milestone
/create-issue docs/features/payment-system.md --assignee @developer --milestone "v2.0"

# Preview what would be created
/create-issue docs/epics/dashboard.md --dry-run

# Batch processing with custom priority
/create-issue docs/backlog/sprint-planning.md --priority medium --batch-size 3
```

## Input Format

The command expects markdown files with structured requirements. Supported formats:

### User Stories

```markdown
## User Story: User Authentication

As a new user, I want to create an account so that I can access personalized features.

### Acceptance Criteria:

- User can register with email and password
- Email verification is required
- Password must meet security requirements
- User receives welcome email after registration

### Technical Requirements:

- Use bcrypt for password hashing
- Implement JWT for session management
- Rate limiting for login attempts
```

### Feature Requirements

```markdown
## Feature: Shopping Cart

- Add items to cart with quantity selection
- Update item quantities in cart
- Remove items from cart
- Calculate total price with taxes
- Persist cart data across sessions
```

### Task Lists

```markdown
## Implementation Tasks

- Set up database schema for user accounts
- Implement user registration API endpoint
- Create email verification system
- Build password reset functionality
- Add user profile management
```

## Output

For each requirements file, the command will:

1. **Parse Content**: Extract user stories, acceptance criteria, and technical requirements
2. **Generate Issues**: Create GitHub issues with proper formatting and metadata
3. **Apply Labels**: Automatically tag issues with type, priority, and component labels
4. **Set Metadata**: Assign issues based on specified parameters
5. **Report Results**: Show summary of created issues with URLs

## Issue Templates

The command uses intelligent templates based on content analysis:

### Feature Issues

- User story format with "As a...I want...so that..." structure
- Detailed acceptance criteria as checkboxes
- Technical requirements section
- Definition of Done checklist

### Bug Issues

- Bug report template with reproduction steps
- Expected vs actual behavior
- Environment information
- Priority and severity assessment

### Task Issues

- Clear task description and requirements
- Implementation notes and constraints
- Definition of Done criteria
- Dependency information

## Integration with Existing Agents

The command automatically coordinates with specialized agents:

- **requirements-analyst**: For complex requirement analysis
- **issue-analyst**: For task breakdown and estimation
- **stakeholder-manager**: For stakeholder approval when needed
- **product-owner**: For priority and roadmap alignment

## Quality Assurance

Before creating issues, the command validates:

- Requirements completeness and clarity
- Acceptance criteria measurability
- Technical feasibility assessment
- Stakeholder approval requirements
- Duplicate issue detection

## Error Handling

- **GitHub CLI Not Available**: Gracefully falls back to manual issue creation
- **Invalid Requirements Format**: Provides specific formatting guidance
- **Rate Limiting**: Respects GitHub API limits with intelligent batching
- **Permission Issues**: Clear error messages for repository access problems

This command bridges the gap between high-level requirements and actionable development tasks.
