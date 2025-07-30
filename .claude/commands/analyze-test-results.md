# Analyze Test Results Command

AI-powered analysis of test results with intelligent failure diagnosis, pattern recognition, and automated merge recommendations.

## Behavior

- Uses advanced machine learning to analyze test failures and patterns
- Provides automated root cause analysis for failing tests
- Calculates confidence scores for test reliability and auto-merge decisions
- Identifies flaky tests and suggests remediation strategies
- Integrates with multiple test frameworks and CI/CD systems
- Generates comprehensive reports with actionable recommendations

## Usage

```bash
/analyze-test-results [SOURCE] [OPTIONS]
```

### Parameters

- `SOURCE`: Test results source (PR number, GitHub Actions run ID, or file paths)
- `--format|-f`: Output format (json, markdown, summary) - default: markdown
- `--output|-o`: Save analysis to file instead of displaying
- `--confidence-threshold|-c`: Minimum confidence score for auto-merge (default: 85)
- `--include-performance`: Include performance test analysis
- `--include-security`: Include security test analysis
- `--verbose|-v`: Enable detailed analysis output

### Examples

```bash
# Analyze test results for a specific PR
/analyze-test-results --pr 123

# Analyze GitHub Actions run results
/analyze-test-results --github-actions-run 987654321

# Analyze local test result files
/analyze-test-results --test-files results.xml coverage.json

# Generate JSON report with custom confidence threshold
/analyze-test-results --pr 456 --format json --confidence-threshold 80

# Comprehensive analysis with all metrics
/analyze-test-results --pr 789 --include-performance --include-security --verbose
```

## Analysis Capabilities

### Test Result Parsing

- **JUnit XML**: Standard Java/Maven test results
- **Jest JSON**: JavaScript test framework results
- **TAP Format**: Test Anything Protocol results
- **GitHub Actions**: CI/CD workflow test results
- **Custom Formats**: Extensible parser for proprietary formats

### Failure Analysis

- **Pattern Recognition**: Identifies common failure patterns using ML
- **Root Cause Classification**: Categorizes failures by underlying cause
- **Flakiness Detection**: Statistical analysis of test reliability
- **Regression Analysis**: Compares against historical test performance
- **Dependency Analysis**: Identifies failures related to external dependencies

### Intelligence Features

- **Confidence Scoring**: 0-100 scale reliability assessment
- **Auto-Merge Recommendations**: AI-driven merge/block decisions
- **Priority Ranking**: Orders failures by impact and urgency
- **Fix Suggestions**: Automated remediation recommendations
- **Risk Assessment**: Evaluates deployment risk based on test results

## Test Result Categories

### Success Levels

- **Clean Pass (95-100% confidence)**: All tests pass consistently
- **Conditional Pass (80-94% confidence)**: Minor issues, generally safe to merge
- **Investigate (60-79% confidence)**: Requires human review before merge
- **Block (0-59% confidence)**: Critical issues, merge not recommended

### Failure Classifications

- **Critical**: Security, data corruption, or system-breaking failures
- **Major**: Functional failures affecting core features
- **Minor**: Edge case failures or flaky test issues
- **Informational**: Coverage or quality metric warnings

### Flakiness Scoring

- **Highly Reliable (0-0.2)**: Consistent pass/fail behavior
- **Moderately Reliable (0.3-0.5)**: Occasional inconsistencies
- **Flaky (0.6-0.8)**: Frequent intermittent failures
- **Highly Flaky (0.9-1.0)**: Unreliable, requires attention

## Output Formats

### Markdown Report

```markdown
# 🧪 Test Result Analysis Report

**Status:** SUCCESS ✅
**Confidence Score:** 92.5/100
**Auto-Merge Recommendation:** APPROVE ✅

## 🧩 Test Suite Results

### Unit Tests

- **Total Tests:** 150
- **Passed:** 148 (98.7%)
- **Failed:** 2
- **Coverage:** 95.2%

#### 🚨 Failures:

**test_authentication_timeout**

- Category: timeout
- Flaky Score: 0.15
- Suggested Fix: Increase timeout values or optimize slow operations
```

### JSON Output

```json
{
  "analysis_timestamp": "2024-01-15T14:30:00Z",
  "overall_status": "success",
  "confidence_score": 92.5,
  "auto_merge_recommendation": "approve",
  "test_suites": [
    {
      "name": "Unit Tests",
      "total_tests": 150,
      "passed_tests": 148,
      "failed_tests": 2,
      "coverage_percentage": 95.2,
      "failures": [
        {
          "test_name": "test_authentication_timeout",
          "root_cause_category": "timeout",
          "flaky_score": 0.15,
          "suggested_fix": "Increase timeout values or optimize slow operations"
        }
      ]
    }
  ],
  "blocking_issues": [],
  "recommended_actions": ["Address timeout issues in authentication tests"]
}
```

### Summary Format

```
Test Analysis Summary (2024-01-15T14:30:00Z)

Status: SUCCESS (92.5% confidence)
Recommendation: APPROVE

Results: 148/150 tests passed
Risk Level: low

0 blocking issues
1 recommended actions
```

## Intelligence Analysis

### Root Cause Detection

The analyzer uses pattern matching to identify common failure causes:

- **Timeout Issues**: Network delays, slow operations, resource contention
- **Null Reference**: Missing initialization, incorrect assumptions
- **Network Failures**: Service unavailability, connection issues
- **Memory Issues**: Resource exhaustion, memory leaks
- **Permission Errors**: Access rights, authentication failures
- **Dependency Problems**: Missing libraries, version conflicts

### Confidence Calculation

The confidence score is calculated using multiple factors:

```
Base Score (70%): Test pass rate
Coverage Bonus (20%): Code coverage percentage
Comprehensiveness (10%): Number of test suites
Flakiness Penalty: Deduction for unreliable tests
```

### Auto-Merge Decision Logic

```
Confidence ≥ 85% + No Critical Failures → APPROVE
Confidence ≥ 75% + ≤1 Minor Failure → CONDITIONAL_APPROVE
Confidence ≥ 60% + ≤3 Failures → INVESTIGATE
Otherwise → BLOCK
```

## Advanced Features

### Performance Analysis

When `--include-performance` is enabled:

- **Response Time Analysis**: Regression detection against baselines
- **Memory Usage Tracking**: Memory leak and efficiency monitoring
- **Throughput Metrics**: Request per second and scalability analysis
- **Resource Utilization**: CPU, memory, and I/O usage patterns

### Security Testing Integration

When `--include-security` is enabled:

- **Vulnerability Detection**: OWASP top 10 and custom security rules
- **Dependency Scanning**: Known vulnerability detection in dependencies
- **Security Score Calculation**: Overall security posture assessment
- **Compliance Checking**: Industry standard compliance validation

### Historical Learning

The system improves over time through:

- **Pattern Learning**: Identifies new failure patterns automatically
- **Accuracy Tracking**: Compares predictions with actual outcomes
- **Baseline Updates**: Adjusts performance and quality baselines
- **Flakiness Tracking**: Maintains database of test reliability metrics

## Integration Points

### CI/CD Integration

- **GitHub Actions**: Direct integration with workflow results
- **Jenkins**: Plugin-compatible analysis of build results
- **CircleCI**: Artifact-based test result analysis
- **GitLab CI**: Pipeline integration and merge request automation

### Notification Systems

- **Slack Integration**: Automated failure notifications with analysis
- **Email Reports**: Scheduled analysis summaries for teams
- **Dashboard Updates**: Real-time metrics for development dashboards
- **Issue Creation**: Automatic GitHub issue creation for critical failures

### Quality Gates

- **Merge Blocking**: Automatic PR blocking based on analysis results
- **Deployment Gates**: Production deployment approval workflows
- **Quality Metrics**: Integration with SonarQube, CodeClimate, etc.
- **Custom Rules**: Configurable thresholds and criteria

## Configuration

### Analysis Rules

Custom rules can be configured in `.claude/settings/test-analysis-rules.json`:

```json
{
  "confidence_thresholds": {
    "auto_approve": 85,
    "conditional_approve": 75,
    "investigate": 60
  },
  "failure_categories": {
    "critical": ["security", "data_corruption"],
    "blocking": ["memory", "timeout"],
    "warning": ["flaky", "coverage"]
  },
  "flakiness_detection": {
    "threshold": 0.5,
    "minimum_runs": 10,
    "lookback_days": 30
  }
}
```

### Performance Baselines

Baseline metrics in `.claude/settings/performance-baselines.json`:

```json
{
  "response_time_ms": 1000,
  "memory_usage_mb": 512,
  "cpu_usage_percent": 80,
  "test_duration_ms": 30000,
  "coverage_minimum": 80
}
```

## Error Handling

### Analysis Failures

- **Parse Errors**: Detailed error messages for unsupported formats
- **Network Issues**: Retry logic for GitHub API calls
- **Permission Problems**: Clear guidance for repository access
- **Resource Limits**: Graceful handling of large test suites

### Fallback Strategies

- **Basic Analysis**: Simple pass/fail analysis when AI features unavailable
- **Historical Data**: Use cached analysis when current data unavailable
- **Conservative Recommendations**: Default to human review when uncertain
- **Partial Results**: Provide analysis for successfully parsed portions

This command transforms raw test results into actionable intelligence, enabling confident automated decision-making while maintaining high quality standards.
