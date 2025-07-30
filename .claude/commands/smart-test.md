# Smart Test Command

Intelligent test execution based on PR impact analysis, dependency mapping, and risk assessment to optimize testing efficiency and coverage.

## Behavior

- Analyzes code changes to determine optimal test scope and strategy
- Uses dependency graphs and impact analysis to identify affected components
- Provides intelligent test selection based on risk assessment and historical data
- Supports multiple test strategies from minimal to comprehensive coverage
- Integrates with existing test frameworks and CI/CD pipelines
- Generates detailed test execution plans with time estimates

## Usage

```bash
/smart-test [SOURCE] [OPTIONS]
```

### Parameters

- `SOURCE`: Source of changes (PR number, commit range, or current changes)
- `--strategy|-s`: Test strategy (minimal, focused, targeted, comprehensive) - auto-detected by default
- `--test-types|-t`: Specific test types to include (unit, integration, e2e, performance, security)
- `--max-time|-m`: Maximum test execution time in minutes
- `--risk-threshold|-r`: Risk threshold for test inclusion (0.0-1.0, default: 0.3)
- `--dry-run`: Generate test plan without executing tests
- `--parallel|-p`: Enable parallel test execution
- `--verbose|-v`: Enable detailed analysis output

### Examples

```bash
# Smart test execution for current PR
/smart-test --pr 123

# Analyze specific commit range with focused testing
/smart-test --commit-range main..feature-branch --strategy focused

# Quick regression test with time limit
/smart-test --pr 456 --max-time 30 --test-types unit,integration

# Generate test plan without execution
/smart-test --commit-range HEAD~5..HEAD --dry-run --verbose

# Comprehensive testing for high-risk changes
/smart-test --pr 789 --strategy comprehensive --parallel
```

## Test Strategies

### Minimal Strategy

- **Scope**: Only directly affected unit tests
- **Duration**: 5-15 minutes
- **Use Case**: Small, low-risk changes with good test coverage
- **Coverage**: Changed files and immediate dependencies

### Focused Strategy

- **Scope**: Unit tests + critical integration tests
- **Duration**: 15-30 minutes
- **Use Case**: Medium-sized changes in well-tested modules
- **Coverage**: Changed files, dependencies, and related components

### Targeted Strategy

- **Scope**: Comprehensive testing of affected modules
- **Duration**: 30-60 minutes
- **Use Case**: Significant changes or moderate risk modifications
- **Coverage**: Full module testing + cross-module integration

### Comprehensive Strategy

- **Scope**: Full test suite with additional validation
- **Duration**: 60+ minutes
- **Use Case**: High-risk changes, major refactoring, or release preparation
- **Coverage**: Complete test suite + performance and security validation

## Risk-Based Test Selection

### File Risk Assessment

The system evaluates each changed file based on:

- **Historical Impact**: Files with previous regression issues get higher priority
- **Complexity Score**: Lines changed, complexity metrics, and architectural importance
- **Dependency Count**: Number of modules that depend on the changed file
- **Test Coverage**: Existing test coverage and test quality metrics
- **Domain Criticality**: Security, payment, auth modules get higher risk scores

### Module Impact Analysis

Changes are analyzed at the module level for:

- **Blast Radius**: Scope of potential impact across the system
- **Stability Score**: Historical stability and regression rates
- **Integration Points**: APIs, databases, external services affected
- **User Impact**: Customer-facing features and critical workflows

## Test Type Selection

### Unit Tests

**Selected When**:

- Direct file modifications detected
- Function or class signatures changed
- Core business logic modifications

**Optimization**:

- Only run tests for changed files and immediate dependencies
- Skip tests for unmodified utility functions
- Prioritize tests with high assertion coverage

### Integration Tests

**Selected When**:

- API endpoints or database schemas modified
- Service boundaries crossed by changes
- Configuration or infrastructure changes

**Scope**:

- Tests covering changed integration points
- Cross-service communication validation
- Database migration and rollback tests

### End-to-End Tests

**Selected When**:

- UI components or user workflows modified
- Critical user journeys potentially affected
- Multiple system components changed together

**Strategy**:

- Focus on happy path scenarios for changed features
- Include error handling for critical workflows
- Skip lengthy setup-intensive tests for low-risk changes

### Performance Tests

**Selected When**:

- Performance-critical code paths modified
- Database queries or algorithms changed
- Resource utilization patterns affected

**Focus**:

- Baseline comparison for modified components
- Load testing for scalability-critical changes
- Memory and CPU profiling for resource-intensive modifications

### Security Tests

**Selected When**:

- Authentication or authorization code modified
- Input validation or sanitization changed
- Security-sensitive modules affected

**Coverage**:

- Vulnerability scanning for security-related changes
- Authentication and authorization flow validation
- Input validation and injection attack prevention

## Intelligent Test Optimization

### Dependency-Based Selection

```
Change → Direct Tests → Dependency Tests → Integration Tests
  ↓           ↓              ↓                 ↓
File A → test_file_a.py → test_module_b.py → api_tests/
```

### Historical Learning

The system learns from:

- **False Positives**: Tests that frequently pass despite file changes
- **False Negatives**: Regressions caught by tests not initially selected
- **Execution Time**: Actual vs. estimated test duration
- **Flaky Tests**: Tests with inconsistent results that should be deprioritized

### Parallel Execution Planning

When `--parallel` is enabled:

- **Test Grouping**: Group tests by execution time and resource requirements
- **Dependency Ordering**: Ensure dependent tests run after their prerequisites
- **Resource Allocation**: Balance CPU, memory, and I/O intensive tests
- **Failure Isolation**: Design groups to minimize failure cascade effects

## Output Formats

### Test Plan (--dry-run)

```markdown
# 🎯 Smart Test Execution Plan

**Strategy:** TARGETED
**Estimated Duration:** 42 minutes
**Risk Threshold:** 0.3

## Required Tests (32 minutes)

### Unit Tests (15 minutes)

- tests/auth/test_login.py
- tests/api/test_user_endpoints.py
- tests/models/test_user_model.py

### Integration Tests (17 minutes)

- tests/integration/test_auth_flow.py
- tests/integration/test_user_api.py

## Optional Tests (10 minutes)

### Performance Tests (10 minutes)

- tests/performance/test_login_performance.py
```

### Execution Results

```
🧪 Smart Test Execution Results

Strategy: TARGETED (42/45 minutes)
Tests Run: 127 tests across 8 test files
Results: ✅ 125 passed, ❌ 2 failed, ⏭️ 0 skipped

Failed Tests:
❌ tests/auth/test_login.py::test_invalid_credentials
❌ tests/integration/test_auth_flow.py::test_password_reset

Risk Assessment: 🟡 MEDIUM
Recommendation: Fix failing tests before merge
```

### JSON Output

```json
{
  "execution_plan": {
    "strategy": "targeted",
    "estimated_duration_minutes": 42,
    "risk_threshold": 0.3,
    "test_groups": [
      {
        "type": "unit",
        "tests": ["tests/auth/test_login.py"],
        "estimated_minutes": 15,
        "required": true
      }
    ]
  },
  "results": {
    "total_tests": 127,
    "passed": 125,
    "failed": 2,
    "duration_minutes": 42
  }
}
```

## Advanced Features

### Change Impact Visualization

```
File Changes → Module Impact → Test Selection
     ↓              ↓              ↓
  auth.py  →   auth_module   →   unit_tests/
  api.py   →   api_module    →   integration_tests/
  ui.tsx   →   frontend      →   e2e_tests/
```

### Risk Heat Map

- **🔴 High Risk**: Immediate comprehensive testing required
- **🟡 Medium Risk**: Targeted testing with integration focus
- **🟢 Low Risk**: Minimal testing, unit tests sufficient

### Test Prioritization Matrix

```
                High Impact    Medium Impact    Low Impact
High Priority   Run First      Run Second       Run Third
Med Priority    Run Second     Run Third        Optional
Low Priority    Run Third      Optional         Skip
```

## Integration Points

### CI/CD Pipeline Integration

```yaml
# GitHub Actions integration
- name: Smart Test Execution
  run: /smart-test --pr ${{ github.event.number }} --max-time 45
```

### Test Framework Support

- **Jest**: JavaScript/TypeScript test framework
- **pytest**: Python testing framework
- **JUnit**: Java testing framework
- **Go Test**: Native Go testing
- **RSpec**: Ruby testing framework
- **Custom**: Configurable test command patterns

### Coverage Integration

- **Coverage.py**: Python code coverage analysis
- **Istanbul/NYC**: JavaScript code coverage
- **JaCoCo**: Java code coverage
- **Go Cover**: Go coverage analysis
- **LCOV**: Language-agnostic coverage format

## Configuration

### Smart Test Rules

Configure test selection rules in `.claude/settings/smart-test-rules.json`:

```json
{
  "strategies": {
    "minimal": {
      "max_duration_minutes": 15,
      "test_types": ["unit"],
      "risk_threshold": 0.1
    },
    "focused": {
      "max_duration_minutes": 30,
      "test_types": ["unit", "integration"],
      "risk_threshold": 0.3
    }
  },
  "risk_factors": {
    "file_patterns": {
      "**/auth/**": 1.5,
      "**/payment/**": 1.8,
      "**/security/**": 1.6
    },
    "change_size_multipliers": {
      "small": 1.0,
      "medium": 1.2,
      "large": 1.5
    }
  }
}
```

### Test Mappings

Define custom test mappings in `.claude/data/test-mappings.json`:

```json
{
  "src/auth/login.py": [
    "tests/unit/test_login.py",
    "tests/integration/test_auth_flow.py"
  ],
  "src/api/users.py": [
    "tests/unit/test_users.py",
    "tests/integration/test_user_api.py"
  ]
}
```

## Error Handling & Fallbacks

### Analysis Failures

- **Git Access Issues**: Fallback to analyzing staged changes
- **Dependency Graph Errors**: Use basic file-to-test mappings
- **Historical Data Missing**: Use conservative risk estimates

### Test Execution Failures

- **Individual Test Failures**: Continue with remaining tests
- **Framework Issues**: Provide manual test command suggestions
- **Timeout Exceeded**: Prioritize most critical tests within time limit

### Recovery Strategies

- **Partial Results**: Report results for successfully completed tests
- **Alternative Strategies**: Suggest manual test approaches when automation fails
- **Escalation**: Recommend full test suite when risk analysis is uncertain

This command transforms reactive testing into proactive, intelligent test execution, ensuring optimal coverage while minimizing time investment and computational resources.
