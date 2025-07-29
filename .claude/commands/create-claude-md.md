# Create CLAUDE.md Command

Generate a project-specific CLAUDE.md file based on codebase analysis.

## Behavior

- Analyzes current project structure and tech stack
- Identifies development patterns and conventions
- Creates comprehensive project context file
- Includes coding standards and workflow guidelines
- Sets up agent utilization patterns

## Template Structure

Creates CLAUDE.md with these sections:

### 📋 Project Configuration

- Project name and version
- Technology stack identification
- Key dependencies and tools

### 🚨 Critical Rules

- Non-negotiable constraints
- Security requirements
- Performance guidelines
- Deployment restrictions

### 🎯 Project Context

- Business purpose and goals
- Architecture overview
- Target users and use cases
- Integration requirements

### 🔧 Development Patterns

- File and directory structure
- Coding standards and conventions
- Testing approaches
- Documentation requirements

### 🚀 Workflow Automation

- Available slash commands
- Configured hooks and automation
- CI/CD pipeline details
- Development scripts

### 🧠 Agent Orchestration

- Recommended agents for different tasks
- Specialized workflows
- Context-specific guidelines

### 🔒 Security & Compliance

- Security practices
- Access control patterns
- Compliance requirements
- Audit trail needs

## Process

1. Scan project files and directories
2. Identify technology stack from package.json, requirements.txt, etc.
3. Analyze existing configuration files
4. Detect coding patterns and conventions
5. Generate context-appropriate CLAUDE.md
6. Include project-specific agent recommendations

## Customization Options

- Language-specific templates (JavaScript, Python, Go, etc.)
- Framework templates (React, Django, Express, etc.)
- Domain templates (web apps, CLI tools, libraries, etc.)
- Team size and workflow patterns
