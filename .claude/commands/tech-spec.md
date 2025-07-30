# Technology Specification Research Command

Performs comprehensive technology research within GitHub-based permission constraints.

## Behavior

- Leverages search-specialist for systematic technology investigation
- Coordinates with specialized agents for technology evaluation
- Provides detailed specification reports with implementation recommendations
- Focuses on latest versions, compatibility, and best practices

## Process

1. **Initial Research Phase**
   - Use search-specialist to investigate technology landscape
   - Query GitHub repositories for latest official sources
   - Analyze documentation and release notes
   - Identify current best practices and trends

2. **Technology Evaluation**
   - Coordinate with appropriate specialist agents
   - Assess compatibility with current development environment
   - Evaluate implementation complexity and dependencies
   - Review security and performance implications

3. **Specification Generation**
   - Create detailed technology specification report
   - Include version recommendations and rationale
   - Provide implementation roadmap
   - Document potential risks and mitigation strategies

## Agent Coordination

### Primary Agents

- **search-specialist**: GitHub-based technology research
- **architect-review**: Architecture and design implications
- **security-auditor**: Security assessment of technologies

### Language-Specific Agents

- **javascript-pro**: Node.js ecosystem technologies
- **python-pro**: Python package and framework evaluation
- **rust-pro**: Rust crate and tool assessment
- **golang-pro**: Go module and service evaluation

### Infrastructure Agents

- **devops-troubleshooter**: Deployment and operational considerations
- **cloud-architect**: Cloud service integration analysis
- **database-admin**: Database technology evaluation

## Research Scope

### Within GitHub Permissions

- Official repository documentation
- Release notes and changelogs
- GitHub API data (stars, activity, maintenance status)
- Official GitHub-hosted documentation
- Community discussions in GitHub issues/discussions

### Technology Categories

- **Frameworks**: Web frameworks, testing frameworks, build tools
- **Libraries**: Core dependencies, utility libraries, specialized packages
- **Infrastructure**: Container technologies, CI/CD tools, deployment platforms
- **Development Tools**: IDEs, formatters, linters, debugging tools

## Output Format

### Technology Specification Report

```markdown
# Technology Specification: [Technology Name]

## Executive Summary

- Technology overview and purpose
- Recommended version and rationale
- Implementation timeline estimate
- Risk assessment summary

## Research Methodology

- Sources consulted
- Agent coordination approach
- Evaluation criteria used

## Technical Analysis

- Current version analysis
- Compatibility assessment
- Performance implications
- Security considerations

## Implementation Plan

- Prerequisites and dependencies
- Step-by-step implementation guide
- Testing and validation approach
- Rollback strategy

## Alternatives Considered

- Competing technologies evaluated
- Comparison matrix
- Selection rationale

## Recommendations

- Immediate next steps
- Long-term maintenance considerations
- Team training requirements
```

## Usage Patterns

### New Technology Evaluation

```bash
# Research a specific technology
/tech-spec React 18 TypeScript integration

# Compare multiple options
/tech-spec "state management: Redux vs Zustand vs Jotai"

# Evaluate upgrade path
/tech-spec Node.js 20 migration from 18
```

### Architecture Decision Support

```bash
# Database technology selection
/tech-spec "PostgreSQL vs MongoDB for user data"

# Infrastructure choices
/tech-spec "Docker Compose vs Kubernetes for local development"

# Testing framework evaluation
/tech-spec Jest vs Vitest comparison
```

### Ecosystem Research

```bash
# Full-stack evaluation
/tech-spec "Next.js 14 full-stack setup with TypeScript"

# Development environment
/tech-spec "VS Code extensions for Python development 2024"

# CI/CD pipeline technologies
/tech-spec "GitHub Actions vs Azure DevOps for Node.js"
```

## Integration with Existing Workflow

### Pre-Implementation Phase

1. Use `/tech-spec` for technology research
2. Review recommendations with `/architect-review`
3. Plan implementation with appropriate specialist agents
4. Document decisions in CLAUDE.md

### During Implementation

1. Reference spec report for implementation details
2. Use specialist agents for code implementation
3. Validate against spec requirements
4. Update spec with actual implementation notes

### Post-Implementation

1. Document lessons learned
2. Update technology preferences in CLAUDE.md
3. Share findings with team
4. Plan future technology evaluations

## Quality Assurance

### Source Validation

- Prioritize official GitHub repositories
- Verify information across multiple sources
- Check repository maintenance status
- Assess community adoption metrics

### Recommendation Criteria

- **Stability**: Proven track record, stable releases
- **Maintenance**: Active development, regular updates
- **Community**: Strong community support, documentation
- **Compatibility**: Fits current development environment
- **Security**: No known vulnerabilities, security best practices

### Risk Assessment

- **Technical Risk**: Implementation complexity, breaking changes
- **Maintenance Risk**: Long-term support, update frequency
- **Adoption Risk**: Learning curve, team expertise
- **Business Risk**: Licensing, vendor lock-in, cost implications

## Examples

### Frontend Framework Research

```markdown
# Research Output Example

Technology: Vue 3 Composition API vs React 18 Hooks

Agents Coordinated:

- search-specialist: GitHub ecosystem analysis
- javascript-pro: Technical implementation comparison
- frontend-developer: Developer experience evaluation
- security-auditor: Security posture assessment

Key Findings:

- Vue 3.3+ offers better TypeScript integration
- React 18 has larger ecosystem but higher complexity
- Both have excellent security track records
- Vue offers gentler learning curve for current team

Recommendation: Vue 3.3 for new projects, with specific version and setup guide
```

This command bridges the gap between the original "spec" agent concept and your current environment constraints, providing systematic technology research within your GitHub-focused permission model.
