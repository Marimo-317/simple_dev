# Technology Research Workflows - Usage Guide

Complete guide for leveraging enhanced technology research capabilities in your Claude Code environment.

## Quick Start

### Basic Technology Evaluation

```bash
# Evaluate a single technology
/tech-spec React 18

# Compare multiple technologies
/tech-spec "React vs Vue vs Svelte"

# Migration planning
/tech-spec "migrate from Vue 2 to Vue 3"
```

### Advanced Research Patterns

```bash
# Security-focused evaluation
/tech-spec "FastAPI security analysis"

# Performance-critical assessment
/tech-spec "Node.js vs Bun performance comparison"

# Full-stack evaluation
/tech-spec "MEAN vs MERN vs MEVN stack comparison"
```

## Workflow Types

### 1. Single Technology Assessment

**When to Use**:

- Evaluating adoption of a new technology
- Upgrading to a newer version
- Security or performance concerns about current tech

**Example Scenarios**:

#### Frontend Framework Evaluation

```bash
/tech-spec Next.js 14
```

**Expected Output**:

- Research phase (15-30 min): GitHub ecosystem analysis
- Technical analysis (30-45 min): Implementation patterns, performance
- Security review (20-30 min): Vulnerability assessment
- Architecture review (20-30 min): System integration impact
- Final specification (10-15 min): Complete recommendation

#### Backend Technology Assessment

```bash
/tech-spec FastAPI
```

**Agent Flow**: search-specialist → python-pro → security-auditor → architect-review

#### Database Evaluation

```bash
/tech-spec PostgreSQL 16
```

**Agent Flow**: search-specialist → database-admin → security-auditor → architect-review

### 2. Comparative Analysis

**When to Use**:

- Choosing between multiple technology options
- Evaluating alternatives to current technology
- Strategic technology planning

**Syntax**: `/tech-spec "Technology A vs Technology B vs Technology C"`

#### State Management Comparison

```bash
/tech-spec "Redux vs Zustand vs Jotai"
```

**Process**:

1. **Parallel Research**: Each technology researched simultaneously
2. **Parallel Analysis**: javascript-pro evaluates each option
3. **Consolidated Review**: Results compared in standardized matrix
4. **Cross-cutting Analysis**: Security and architecture implications
5. **Ranked Recommendations**: Final recommendations with rationale

#### Testing Framework Comparison

```bash
/tech-spec "Jest vs Vitest vs Playwright"
```

**Evaluation Matrix Output**:
| Criteria | Jest | Vitest | Playwright |
|----------|------|--------|------------|
| Performance | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Developer Experience | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Ecosystem | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Learning Curve | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

### 3. Migration Planning

**When to Use**:

- Planning technology upgrades
- Replacing legacy technologies
- Modernizing technology stack

**Syntax**: `/tech-spec "migrate from [current] to [target]"`

#### Framework Migration

```bash
/tech-spec "migrate from Angular 12 to React 18"
```

**Migration Workflow**:

1. **Current State Analysis**: Document existing Angular implementation
2. **Target Research**: React 18 capabilities and requirements
3. **Gap Analysis**: Identify incompatibilities and missing features
4. **Strategy Development**: Phased migration approach
5. **Risk Assessment**: Mitigation strategies and contingency plans

#### Database Migration

```bash
/tech-spec "migrate from MySQL to PostgreSQL"
```

**Output Includes**:

- Data migration strategy
- Schema conversion plan
- Performance impact analysis
- Rollback procedures
- Testing validation approach

## Agent Collaboration Patterns

### Understanding Agent Roles

#### search-specialist

- **Primary Role**: GitHub-based technology research
- **Expertise**: Repository analysis, community health, version tracking
- **Output**: Technology landscape analysis, initial recommendations

**Optimization Tips**:

- Provide specific version numbers for targeted research
- Include context about current environment constraints
- Specify evaluation criteria (performance, security, maintainability)

#### Technical Specialists

- **javascript-pro**: Frontend frameworks, Node.js, JavaScript ecosystem
- **python-pro**: Backend frameworks, Python packages, async patterns
- **database-admin**: Database technologies, schema design, performance
- **devops-troubleshooter**: Infrastructure, deployment, operational concerns

**Handoff Context**:
Each specialist receives:

- Research findings from search-specialist
- Technical constraints from environment
- Specific evaluation criteria
- Integration requirements

#### Cross-cutting Specialists

- **security-auditor**: Security assessment across all technologies
- **architect-review**: System integration and architectural impact
- **performance-engineer**: Performance implications and optimization

### Customizing Agent Coordination

#### Specify Focus Areas

```bash
# Security-focused evaluation
/tech-spec React 18 --focus=security

# Performance-critical assessment
/tech-spec "GraphQL vs REST" --focus=performance

# Architecture-focused evaluation
/tech-spec microservices --focus=architecture
```

#### Agent Preferences

```bash
# Prefer specific agents for evaluation
/tech-spec Next.js --agents="search-specialist,javascript-pro,security-auditor"

# Skip certain evaluation phases
/tech-spec PostgreSQL --skip=security

# Extended evaluation with additional agents
/tech-spec Docker --extended --include="devops-troubleshooter,cloud-architect"
```

## Interpretation Guide

### Research Phase Output

#### Quality Indicators

```markdown
✅ **High Quality Research**

- 8+ GitHub sources analyzed
- Latest stable version identified
- Release frequency documented
- Community health metrics included
- Documentation quality assessed

⚠️ **Medium Quality Research**

- 5-7 sources analyzed
- Version information present
- Basic community metrics
- Some documentation gaps

❌ **Low Quality Research**

- <5 sources analyzed
- Version information unclear
- Limited community data
- Poor documentation coverage
```

#### Example Research Summary

```markdown
## Technology Research: React 18.2

### GitHub Analysis (8 sources)

- **Main Repository**: facebook/react (200k+ stars, active)
- **Release Frequency**: Regular 2-3 month cycles
- **Community Health**: Excellent (22k contributors, responsive maintainers)
- **Documentation**: Comprehensive (official docs + community resources)

### Version Stability Assessment

- **Current Stable**: 18.2.0 (Released: June 2023)
- **LTS Status**: React 18 is current LTS
- **Breaking Changes**: Minimal from 17.x, well-documented migration
- **Future Roadmap**: React 19 in development, concurrent features focus
```

### Technical Analysis Output

#### Implementation Complexity Matrix

```markdown
| Aspect                   | Complexity | Notes                                   |
| ------------------------ | ---------- | --------------------------------------- |
| Initial Setup            | Low        | Create React App, Vite support          |
| TypeScript Integration   | Low        | Excellent built-in support              |
| Testing Setup            | Medium     | Jest + RTL recommended                  |
| State Management         | Variable   | Context API (simple) to Redux (complex) |
| Performance Optimization | Medium     | React.memo, useMemo, Suspense           |
```

#### Integration Assessment

```markdown
### Current Environment Compatibility

✅ Node.js 20: Fully supported
✅ TypeScript: Excellent integration
✅ DevContainer: Compatible, fast HMR
✅ GitHub Actions: Standard CI/CD patterns available

### Required Dependencies

- **Core**: react, react-dom
- **Build**: Vite or Create React App
- **TypeScript**: @types/react, @types/react-dom
- **Testing**: @testing-library/react, jest
```

### Security Review Output

#### Risk Assessment Matrix

```markdown
| Risk Level | Category         | Description              | Mitigation                        |
| ---------- | ---------------- | ------------------------ | --------------------------------- |
| Low        | XSS              | React escapes by default | Follow JSX best practices         |
| Low        | Dependencies     | Regular security updates | Use npm audit, Dependabot         |
| Medium     | Third-party libs | Ecosystem packages vary  | Vet packages, use trusted sources |
```

#### Security Recommendations

```markdown
### Immediate Actions

1. Enable Content Security Policy
2. Configure HTTPS in production
3. Implement input validation
4. Use React.StrictMode in development

### Ongoing Monitoring

1. Regular dependency audits (npm audit)
2. Security update tracking (GitHub Security Advisories)
3. Component security reviews for custom code
```

### Architecture Review Output

#### System Integration Impact

```markdown
### Integration Points

- **Frontend-Backend**: RESTful APIs, GraphQL compatibility
- **Authentication**: JWT, OAuth2 integration patterns
- **State Management**: Redux, Zustand, or Context API
- **Routing**: React Router, Next.js routing

### Scalability Assessment

- **Team Scale**: Excellent (component-based architecture)
- **Codebase Scale**: Good (code splitting, lazy loading)
- **Performance Scale**: Good (virtual DOM, concurrent features)

### Long-term Considerations

- **Maintenance**: Active development, stable API
- **Talent Acquisition**: Large developer pool available
- **Technology Evolution**: Gradual, backward-compatible upgrades
```

## Best Practices

### Effective Technology Evaluation

#### 1. Define Clear Criteria

```markdown
Before starting evaluation, document:

- Performance requirements
- Security constraints
- Team expertise level
- Integration requirements
- Timeline constraints
- Budget considerations
```

#### 2. Provide Context

```bash
# Good: Specific context
/tech-spec "React 18 for e-commerce frontend with TypeScript and high performance requirements"

# Better: Include constraints
/tech-spec "React 18 evaluation for B2B dashboard, team has Vue experience, need migration plan"

# Best: Complete context
/tech-spec "React 18 vs Vue 3 for replacing Angular 12 dashboard, TypeScript required, 50k+ users, team of 6 developers"
```

#### 3. Iterative Refinement

```bash
# Initial broad evaluation
/tech-spec "frontend frameworks 2024"

# Focused comparison based on initial findings
/tech-spec "React 18 vs Vue 3 vs Svelte 4"

# Detailed analysis of top choice
/tech-spec "React 18 implementation planning"
```

### Working with Agent Recommendations

#### Understanding Confidence Levels

```markdown
🟢 **High Confidence**: Strong evidence, multiple sources, proven track record
🟡 **Medium Confidence**: Good evidence, some gaps, moderate risk
🔴 **Low Confidence**: Limited evidence, significant unknowns, high risk
```

#### Handling Conflicting Recommendations

```markdown
When agents disagree:

1. **Identify the source of disagreement** (different priorities, criteria)
2. **Request clarification** with specific questions
3. **Seek additional specialist input** if needed
4. **Document the trade-offs** for future reference
```

#### Following Up on Recommendations

```bash
# Get implementation details after technology selection
/tech-spec "React 18 implementation guide for [your specific use case]"

# Plan migration strategy
/tech-spec "Vue 2 to React 18 migration roadmap"

# Ongoing monitoring
/tech-spec "React 18 security monitoring setup"
```

## Troubleshooting

### Common Issues

#### 1. Insufficient Research Data

**Problem**: Agent returns limited information
**Solutions**:

- Specify more sources: `/tech-spec "React 18 --sources=extended"`
- Focus on specific aspects: `/tech-spec "React 18 security analysis"`
- Use different search terms: `/tech-spec "React latest version"`

#### 2. Conflicting Agent Recommendations

**Problem**: Technical and security agents disagree
**Solutions**:

- Request detailed reasoning from each agent
- Seek architect-review for tie-breaking
- Define weighted criteria for decision making

#### 3. Evaluation Takes Too Long

**Problem**: Workflow exceeds expected timeframes
**Solutions**:

- Check quality gates for bottlenecks
- Reduce scope of evaluation
- Use parallel evaluation for comparisons

#### 4. Recommendations Don't Fit Context

**Problem**: Generic recommendations not applicable
**Solutions**:

- Provide more specific context upfront
- Include technical constraints in request
- Ask for context-specific follow-up analysis

### Getting Help

#### Agent-Specific Issues

- **search-specialist**: Issues with research scope or quality
- **Technical specialists**: Implementation or integration concerns
- **security-auditor**: Security assessment questions
- **architect-review**: System design or scaling concerns

#### Workflow Issues

- **Quality gates**: Understanding validation criteria
- **Timeline**: Managing evaluation duration
- **Integration**: Connecting to existing development process

This enhanced technology research capability transforms your Claude Code environment into a systematic technology evaluation platform, ensuring informed decision-making while maintaining development velocity.
