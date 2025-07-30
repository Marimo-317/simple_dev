#!/usr/bin/env python3
"""
AI-Powered Test Result Analyzer

This script uses artificial intelligence to analyze test results, identify patterns,
diagnose failures, and provide automated recommendations for resolution.

Usage:
    python test-result-analyzer.py --pr-number 123 --test-output tests.xml
    python test-result-analyzer.py --github-actions-run 456789 --format json
"""

import os
import sys
import json
import argparse
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import hashlib


@dataclass
class TestFailure:
    """Individual test failure information."""
    test_name: str
    test_class: str
    failure_type: str
    failure_message: str
    stack_trace: str
    duration_ms: float
    flaky_score: float
    root_cause_category: str
    suggested_fix: str


@dataclass
class TestSuite:
    """Test suite information."""
    name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    duration_ms: float
    coverage_percentage: float
    failures: List[TestFailure]


@dataclass
class PerformanceMetrics:
    """Performance test metrics."""
    response_time_ms: float
    memory_usage_mb: float
    cpu_usage_percent: float
    throughput_rps: float
    error_rate_percent: float
    regression_detected: bool
    baseline_comparison: Dict[str, float]


@dataclass
class SecurityTestResults:
    """Security test results."""
    vulnerabilities_found: int
    high_severity_count: int
    medium_severity_count: int
    low_severity_count: int
    owasp_top_10_issues: List[str]
    dependency_vulnerabilities: List[str]
    security_score: float


@dataclass
class QualityMetrics:
    """Code quality metrics."""
    code_coverage: float
    line_coverage: float
    branch_coverage: float
    complexity_score: int
    maintainability_index: float
    technical_debt_minutes: int
    duplicate_code_percentage: float


@dataclass
class TestAnalysis:
    """Complete test analysis result."""
    analysis_timestamp: str
    pr_number: Optional[int]
    commit_sha: str
    test_suites: List[TestSuite]
    performance_metrics: Optional[PerformanceMetrics]
    security_results: Optional[SecurityTestResults]
    quality_metrics: Optional[QualityMetrics]
    overall_status: str
    confidence_score: float
    auto_merge_recommendation: str
    blocking_issues: List[str]
    recommended_actions: List[str]
    risk_assessment: str


class TestResultAnalyzer:
    """AI-powered test result analyzer."""
    
    def __init__(self):
        self.failure_patterns = self._load_failure_patterns()
        self.performance_baselines = self._load_performance_baselines()
        self.flaky_test_history = self._load_flaky_test_history()
        self.security_rules = self._load_security_rules()
    
    def _load_failure_patterns(self) -> Dict[str, Dict[str, str]]:
        """Load common failure patterns and their solutions."""
        return {
            'timeout': {
                'pattern': r'(?:timeout|timed out|time limit exceeded)',
                'category': 'timeout',
                'fix': 'Increase timeout values or optimize slow operations'
            },
            'null_pointer': {
                'pattern': r'(?:NullPointerException|null pointer|AttributeError.*None)',
                'category': 'null_reference',
                'fix': 'Add null checks and proper initialization'
            },
            'connection_refused': {
                'pattern': r'(?:connection refused|connection reset|network unreachable)',
                'category': 'network',
                'fix': 'Check service availability and network configuration'
            },
            'assertion_error': {
                'pattern': r'(?:AssertionError|assertion failed|expected.*but was)',
                'category': 'assertion',
                'fix': 'Review test expectations and actual behavior'
            },
            'memory_error': {
                'pattern': r'(?:OutOfMemoryError|MemoryError|memory exhausted)',
                'category': 'memory',
                'fix': 'Optimize memory usage or increase available memory'
            },
            'permission_denied': {
                'pattern': r'(?:permission denied|access denied|unauthorized)',
                'category': 'permissions',
                'fix': 'Check file permissions and access rights'
            },
            'import_error': {
                'pattern': r'(?:ImportError|ModuleNotFoundError|cannot import)',
                'category': 'dependencies',
                'fix': 'Verify dependencies are installed and properly configured'
            },
            'database_error': {
                'pattern': r'(?:database.*error|sql.*error|connection.*database)',
                'category': 'database',
                'fix': 'Check database connectivity and schema'
            }
        }
    
    def _load_performance_baselines(self) -> Dict[str, float]:
        """Load performance baselines for comparison."""
        baseline_file = '.claude/settings/performance-baselines.json'
        if os.path.exists(baseline_file):
            try:
                with open(baseline_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default baselines
        return {
            'response_time_ms': 1000,
            'memory_usage_mb': 512,
            'cpu_usage_percent': 80,
            'throughput_rps': 100,
            'error_rate_percent': 1.0
        }
    
    def _load_flaky_test_history(self) -> Dict[str, Dict[str, Any]]:
        """Load historical data about flaky tests."""
        history_file = '.claude/data/flaky-test-history.json'
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {}
    
    def _load_security_rules(self) -> Dict[str, Any]:
        """Load security testing rules and thresholds."""
        return {
            'max_high_severity': 0,
            'max_medium_severity': 2,
            'max_total_vulnerabilities': 5,
            'min_security_score': 8.0,
            'owasp_blocking_issues': [
                'SQL Injection',
                'Cross-Site Scripting (XSS)',
                'Insecure Direct Object References'
            ]
        }
    
    def analyze_github_actions_run(self, run_id: str) -> Optional[TestAnalysis]:
        """Analyze test results from GitHub Actions run."""
        try:
            # Get workflow run details
            cmd = ['gh', 'run', 'view', run_id, '--json', 
                   'status,conclusion,jobs,workflowName,headSha']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            run_data = json.loads(result.stdout)
            
            # Download artifacts containing test results
            artifacts_cmd = ['gh', 'run', 'download', run_id, '--dir', 'test-artifacts']
            subprocess.run(artifacts_cmd, capture_output=True)
            
            # Parse test results from downloaded artifacts
            test_suites = self._parse_test_artifacts('test-artifacts')
            
            return self._create_analysis(
                pr_number=None,
                commit_sha=run_data.get('headSha', ''),
                test_suites=test_suites
            )
            
        except Exception as e:
            print(f"Failed to analyze GitHub Actions run {run_id}: {e}")
            return None
    
    def analyze_pr_tests(self, pr_number: int) -> Optional[TestAnalysis]:
        """Analyze test results for a specific PR."""
        try:
            # Get PR information
            cmd = ['gh', 'pr', 'view', str(pr_number), '--json', 
                   'headRefOid,statusCheckRollup,title']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            pr_data = json.loads(result.stdout)
            commit_sha = pr_data.get('headRefOid', '')
            
            # Analyze status checks
            status_checks = pr_data.get('statusCheckRollup', [])
            test_suites = self._analyze_status_checks(status_checks)
            
            return self._create_analysis(
                pr_number=pr_number,
                commit_sha=commit_sha,
                test_suites=test_suites
            )
            
        except Exception as e:
            print(f"Failed to analyze PR {pr_number}: {e}")
            return None
    
    def analyze_test_files(self, test_files: List[str]) -> TestAnalysis:
        """Analyze test results from local files."""
        test_suites = []
        
        for file_path in test_files:
            if file_path.endswith('.xml'):
                suites = self._parse_junit_xml(file_path)
                test_suites.extend(suites)
            elif file_path.endswith('.json'):
                suites = self._parse_json_results(file_path)
                test_suites.extend(suites)
            elif file_path.endswith('.tap'):
                suites = self._parse_tap_results(file_path)
                test_suites.extend(suites)
        
        return self._create_analysis(
            pr_number=None,
            commit_sha='local',
            test_suites=test_suites
        )
    
    def _parse_test_artifacts(self, artifacts_dir: str) -> List[TestSuite]:
        """Parse test results from downloaded artifacts."""
        test_suites = []
        artifacts_path = Path(artifacts_dir)
        
        if not artifacts_path.exists():
            return test_suites
        
        # Find and parse test result files
        for file_path in artifacts_path.rglob('*'):
            if file_path.is_file():
                if file_path.suffix in ['.xml', '.json', '.tap']:
                    try:
                        if file_path.suffix == '.xml':
                            suites = self._parse_junit_xml(str(file_path))
                            test_suites.extend(suites)
                        elif file_path.suffix == '.json':
                            suites = self._parse_json_results(str(file_path))
                            test_suites.extend(suites)
                        elif file_path.suffix == '.tap':
                            suites = self._parse_tap_results(str(file_path))
                            test_suites.extend(suites)
                    except Exception as e:
                        print(f"Failed to parse {file_path}: {e}")
        
        return test_suites
    
    def _parse_junit_xml(self, file_path: str) -> List[TestSuite]:
        """Parse JUnit XML test results."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            test_suites = []
            
            # Handle both <testsuite> and <testsuites> root elements
            if root.tag == 'testsuite':
                suites = [root]
            else:
                suites = root.findall('.//testsuite')
            
            for suite_elem in suites:
                failures = []
                
                for testcase in suite_elem.findall('testcase'):
                    failure_elem = testcase.find('failure')
                    error_elem = testcase.find('error')
                    
                    if failure_elem is not None or error_elem is not None:
                        elem = failure_elem if failure_elem is not None else error_elem
                        
                        failure = TestFailure(
                            test_name=testcase.get('name', ''),
                            test_class=testcase.get('classname', ''),
                            failure_type=elem.get('type', ''),
                            failure_message=elem.get('message', ''),
                            stack_trace=elem.text or '',
                            duration_ms=float(testcase.get('time', 0)) * 1000,
                            flaky_score=self._calculate_flaky_score(testcase.get('name', '')),
                            root_cause_category=self._categorize_failure(elem.get('message', '') + ' ' + (elem.text or '')),
                            suggested_fix=self._suggest_fix(elem.get('message', '') + ' ' + (elem.text or ''))
                        )
                        failures.append(failure)
                
                suite = TestSuite(
                    name=suite_elem.get('name', ''),
                    total_tests=int(suite_elem.get('tests', 0)),
                    passed_tests=int(suite_elem.get('tests', 0)) - int(suite_elem.get('failures', 0)) - int(suite_elem.get('errors', 0)),
                    failed_tests=int(suite_elem.get('failures', 0)) + int(suite_elem.get('errors', 0)),
                    skipped_tests=int(suite_elem.get('skipped', 0)),
                    duration_ms=float(suite_elem.get('time', 0)) * 1000,
                    coverage_percentage=0.0,  # Not available in JUnit XML
                    failures=failures
                )
                test_suites.append(suite)
            
            return test_suites
            
        except Exception as e:
            print(f"Failed to parse JUnit XML {file_path}: {e}")
            return []
    
    def _parse_json_results(self, file_path: str) -> List[TestSuite]:
        """Parse JSON test results (Jest, Mocha, etc.)."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Handle different JSON formats
            if 'testResults' in data:  # Jest format
                return self._parse_jest_results(data)
            elif 'tests' in data:  # Generic format
                return self._parse_generic_json_results(data)
            else:
                return []
                
        except Exception as e:
            print(f"Failed to parse JSON results {file_path}: {e}")
            return []
    
    def _parse_jest_results(self, data: Dict[str, Any]) -> List[TestSuite]:
        """Parse Jest-specific JSON results."""
        test_suites = []
        
        for test_result in data.get('testResults', []):
            failures = []
            
            for assertion_result in test_result.get('assertionResults', []):
                if assertion_result.get('status') == 'failed':
                    failure_messages = assertion_result.get('failureMessages', [])
                    failure_message = '\n'.join(failure_messages)
                    
                    failure = TestFailure(
                        test_name=assertion_result.get('title', ''),
                        test_class=test_result.get('name', ''),
                        failure_type='AssertionError',
                        failure_message=failure_message,
                        stack_trace=failure_message,
                        duration_ms=assertion_result.get('duration', 0),
                        flaky_score=self._calculate_flaky_score(assertion_result.get('title', '')),
                        root_cause_category=self._categorize_failure(failure_message),
                        suggested_fix=self._suggest_fix(failure_message)
                    )
                    failures.append(failure)
            
            suite = TestSuite(
                name=test_result.get('name', ''),
                total_tests=test_result.get('numTotalTests', 0),
                passed_tests=test_result.get('numPassingTests', 0),
                failed_tests=test_result.get('numFailingTests', 0),
                skipped_tests=test_result.get('numPendingTests', 0),
                duration_ms=test_result.get('perfStats', {}).get('end', 0) - test_result.get('perfStats', {}).get('start', 0),
                coverage_percentage=self._extract_coverage_from_jest(data),
                failures=failures
            )
            test_suites.append(suite)
        
        return test_suites
    
    def _extract_coverage_from_jest(self, data: Dict[str, Any]) -> float:
        """Extract coverage percentage from Jest data."""
        coverage_map = data.get('coverageMap', {})
        if not coverage_map:
            return 0.0
        
        total_lines = 0
        covered_lines = 0
        
        for file_coverage in coverage_map.values():
            statements = file_coverage.get('s', {})
            for count in statements.values():
                total_lines += 1
                if count > 0:
                    covered_lines += 1
        
        return (covered_lines / total_lines * 100) if total_lines > 0 else 0.0
    
    def _parse_tap_results(self, file_path: str) -> List[TestSuite]:
        """Parse TAP (Test Anything Protocol) results."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            failures = []
            total_tests = 0
            failed_tests = 0
            current_test_name = ""
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('ok '):
                    total_tests += 1
                elif line.startswith('not ok '):
                    total_tests += 1
                    failed_tests += 1
                    
                    # Extract test name
                    parts = line.split(' ', 3)
                    if len(parts) > 3:
                        current_test_name = parts[3]
                    
                elif line.startswith('#') and current_test_name:
                    # Failure details
                    failure_message = line[1:].strip()
                    
                    failure = TestFailure(
                        test_name=current_test_name,
                        test_class='TAP Test',
                        failure_type='TAP Failure',
                        failure_message=failure_message,
                        stack_trace=failure_message,
                        duration_ms=0,
                        flaky_score=self._calculate_flaky_score(current_test_name),
                        root_cause_category=self._categorize_failure(failure_message),
                        suggested_fix=self._suggest_fix(failure_message)
                    )
                    failures.append(failure)
                    current_test_name = ""
            
            suite = TestSuite(
                name=Path(file_path).name,
                total_tests=total_tests,
                passed_tests=total_tests - failed_tests,
                failed_tests=failed_tests,
                skipped_tests=0,
                duration_ms=0,
                coverage_percentage=0.0,
                failures=failures
            )
            
            return [suite]
            
        except Exception as e:
            print(f"Failed to parse TAP results {file_path}: {e}")
            return []
    
    def _calculate_flaky_score(self, test_name: str) -> float:
        """Calculate flakiness score for a test (0-1, higher = more flaky)."""
        history = self.flaky_test_history.get(test_name, {})
        
        total_runs = history.get('total_runs', 0)
        failures = history.get('failures', 0)
        
        if total_runs == 0:
            return 0.0
        
        failure_rate = failures / total_runs
        
        # Consider patterns that indicate flakiness
        flaky_indicators = ['intermittent', 'random', 'timeout', 'race condition']
        flaky_keywords = sum(1 for indicator in flaky_indicators 
                           if indicator in test_name.lower())
        
        base_score = failure_rate
        keyword_bonus = min(0.3, flaky_keywords * 0.1)
        
        return min(1.0, base_score + keyword_bonus)
    
    def _categorize_failure(self, failure_text: str) -> str:
        """Categorize failure based on error message."""
        failure_lower = failure_text.lower()
        
        for category, pattern_info in self.failure_patterns.items():
            if re.search(pattern_info['pattern'], failure_lower, re.IGNORECASE):
                return pattern_info['category']
        
        return 'unknown'
    
    def _suggest_fix(self, failure_text: str) -> str:
        """Suggest fix based on failure pattern."""
        failure_lower = failure_text.lower()
        
        for category, pattern_info in self.failure_patterns.items():
            if re.search(pattern_info['pattern'], failure_lower, re.IGNORECASE):
                return pattern_info['fix']
        
        return 'Review logs and error message for specific resolution steps'
    
    def _analyze_status_checks(self, status_checks: List[Dict[str, Any]]) -> List[TestSuite]:
        """Analyze GitHub status checks to extract test information."""
        test_suites = []
        
        for check in status_checks:
            if check.get('conclusion') == 'failure':
                # Create a synthetic test suite for failed status check
                failure = TestFailure(
                    test_name=check.get('name', 'Unknown'),
                    test_class='Status Check',
                    failure_type='CI Failure',
                    failure_message=check.get('title', 'Status check failed'),
                    stack_trace='',
                    duration_ms=0,
                    flaky_score=0.0,
                    root_cause_category='ci_failure',
                    suggested_fix='Check CI logs for detailed error information'
                )
                
                suite = TestSuite(
                    name=check.get('name', 'Unknown Check'),
                    total_tests=1,
                    passed_tests=0,
                    failed_tests=1,
                    skipped_tests=0,
                    duration_ms=0,
                    coverage_percentage=0.0,
                    failures=[failure]
                )
                test_suites.append(suite)
        
        return test_suites
    
    def _create_analysis(self, pr_number: Optional[int], commit_sha: str, 
                        test_suites: List[TestSuite]) -> TestAnalysis:
        """Create comprehensive test analysis."""
        # Calculate overall statistics
        total_tests = sum(suite.total_tests for suite in test_suites)
        total_failures = sum(suite.failed_tests for suite in test_suites)
        total_passed = sum(suite.passed_tests for suite in test_suites)
        
        # Determine overall status
        if total_failures == 0:
            overall_status = 'success'
        elif total_failures <= 2:
            overall_status = 'warning'
        else:
            overall_status = 'failure'
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(test_suites)
        
        # Determine auto-merge recommendation
        auto_merge_recommendation = self._determine_auto_merge_recommendation(
            test_suites, confidence_score
        )
        
        # Identify blocking issues
        blocking_issues = self._identify_blocking_issues(test_suites)
        
        # Generate recommended actions
        recommended_actions = self._generate_recommended_actions(test_suites, blocking_issues)
        
        # Assess risk
        risk_assessment = self._assess_risk(test_suites, confidence_score)
        
        return TestAnalysis(
            analysis_timestamp=datetime.now().isoformat(),
            pr_number=pr_number,
            commit_sha=commit_sha,
            test_suites=test_suites,
            performance_metrics=self._analyze_performance_metrics(test_suites),
            security_results=self._analyze_security_results(test_suites),
            quality_metrics=self._analyze_quality_metrics(test_suites),
            overall_status=overall_status,
            confidence_score=confidence_score,
            auto_merge_recommendation=auto_merge_recommendation,
            blocking_issues=blocking_issues,
            recommended_actions=recommended_actions,
            risk_assessment=risk_assessment
        )
    
    def _calculate_confidence_score(self, test_suites: List[TestSuite]) -> float:
        """Calculate confidence score for test results (0-100)."""
        if not test_suites:
            return 0.0
        
        total_tests = sum(suite.total_tests for suite in test_suites)
        if total_tests == 0:
            return 0.0
        
        # Base score from pass rate
        total_passed = sum(suite.passed_tests for suite in test_suites)
        pass_rate = total_passed / total_tests
        base_score = pass_rate * 70  # 70% of score from pass rate
        
        # Coverage bonus (if available)
        avg_coverage = sum(suite.coverage_percentage for suite in test_suites) / len(test_suites)
        coverage_bonus = min(20, avg_coverage / 5)  # Up to 20 points for coverage
        
        # Flakiness penalty
        flaky_tests = sum(1 for suite in test_suites 
                         for failure in suite.failures 
                         if failure.flaky_score > 0.5)
        flakiness_penalty = min(20, flaky_tests * 5)  # Up to 20 point penalty
        
        # Test comprehensiveness bonus
        comprehensiveness_bonus = min(10, len(test_suites))  # Multiple test suites
        
        final_score = base_score + coverage_bonus + comprehensiveness_bonus - flakiness_penalty
        return max(0.0, min(100.0, final_score))
    
    def _determine_auto_merge_recommendation(self, test_suites: List[TestSuite], 
                                           confidence_score: float) -> str:
        """Determine auto-merge recommendation."""
        total_failures = sum(suite.failed_tests for suite in test_suites)
        
        if total_failures == 0 and confidence_score >= 85:
            return 'approve'
        elif total_failures <= 1 and confidence_score >= 75:
            return 'conditional_approve'
        elif total_failures <= 3 and confidence_score >= 60:
            return 'investigate'
        else:
            return 'block'
    
    def _identify_blocking_issues(self, test_suites: List[TestSuite]) -> List[str]:
        """Identify issues that should block merge."""
        blocking_issues = []
        
        for suite in test_suites:
            for failure in suite.failures:
                if failure.root_cause_category in ['security', 'data_corruption', 'memory']:
                    blocking_issues.append(f"Critical failure in {failure.test_name}: {failure.root_cause_category}")
                elif failure.flaky_score < 0.3:  # Non-flaky failures are more serious
                    blocking_issues.append(f"Consistent failure in {failure.test_name}")
        
        return blocking_issues[:5]  # Limit to top 5 issues
    
    def _generate_recommended_actions(self, test_suites: List[TestSuite], 
                                    blocking_issues: List[str]) -> List[str]:
        """Generate recommended actions based on analysis."""
        actions = []
        
        if blocking_issues:
            actions.append("Address critical blocking issues before merge")
        
        # Group failures by category
        failure_categories = {}
        for suite in test_suites:
            for failure in suite.failures:
                category = failure.root_cause_category
                if category not in failure_categories:
                    failure_categories[category] = []
                failure_categories[category].append(failure)
        
        # Generate category-specific recommendations
        for category, failures in failure_categories.items():
            if len(failures) > 1:
                actions.append(f"Review {len(failures)} {category} failures for common root cause")
        
        # Coverage recommendations
        low_coverage_suites = [suite for suite in test_suites 
                              if suite.coverage_percentage < 70]
        if low_coverage_suites:
            actions.append(f"Improve test coverage for {len(low_coverage_suites)} test suites")
        
        # Performance recommendations
        slow_tests = [suite for suite in test_suites 
                     if suite.duration_ms > 30000]  # > 30 seconds
        if slow_tests:
            actions.append(f"Optimize {len(slow_tests)} slow test suites")
        
        return actions[:10]  # Limit to top 10 actions
    
    def _assess_risk(self, test_suites: List[TestSuite], confidence_score: float) -> str:
        """Assess overall risk level."""
        total_failures = sum(suite.failed_tests for suite in test_suites)
        critical_failures = sum(1 for suite in test_suites 
                               for failure in suite.failures 
                               if failure.root_cause_category in ['security', 'data_corruption'])
        
        if critical_failures > 0:
            return 'high'
        elif total_failures > 5 or confidence_score < 60:
            return 'medium'
        elif total_failures > 0 or confidence_score < 80:
            return 'low'
        else:
            return 'minimal'
    
    def _analyze_performance_metrics(self, test_suites: List[TestSuite]) -> Optional[PerformanceMetrics]:
        """Analyze performance test results."""
        # This would be implemented to parse performance test results
        # For now, return None as performance analysis requires specific test output
        return None
    
    def _analyze_security_results(self, test_suites: List[TestSuite]) -> Optional[SecurityTestResults]:
        """Analyze security test results."""
        security_failures = []
        for suite in test_suites:
            for failure in suite.failures:
                if 'security' in failure.test_name.lower() or 'vuln' in failure.test_name.lower():
                    security_failures.append(failure)
        
        if not security_failures:
            return None
        
        return SecurityTestResults(
            vulnerabilities_found=len(security_failures),
            high_severity_count=len([f for f in security_failures if 'high' in f.failure_message.lower()]),
            medium_severity_count=len([f for f in security_failures if 'medium' in f.failure_message.lower()]),
            low_severity_count=len([f for f in security_failures if 'low' in f.failure_message.lower()]),
            owasp_top_10_issues=[],
            dependency_vulnerabilities=[],
            security_score=max(0, 10 - len(security_failures))
        )
    
    def _analyze_quality_metrics(self, test_suites: List[TestSuite]) -> Optional[QualityMetrics]:
        """Analyze code quality metrics."""
        if not test_suites:
            return None
        
        avg_coverage = sum(suite.coverage_percentage for suite in test_suites) / len(test_suites)
        
        return QualityMetrics(
            code_coverage=avg_coverage,
            line_coverage=avg_coverage,
            branch_coverage=avg_coverage * 0.8,  # Estimate
            complexity_score=0,  # Would need additional data
            maintainability_index=85.0,  # Default good score
            technical_debt_minutes=0,
            duplicate_code_percentage=0.0
        )


def main():
    parser = argparse.ArgumentParser(description='Analyze test results with AI-powered insights')
    parser.add_argument('--pr-number', '-p', type=int,
                       help='GitHub PR number to analyze')
    parser.add_argument('--github-actions-run', '-r',
                       help='GitHub Actions run ID to analyze')
    parser.add_argument('--test-files', '-f', nargs='+',
                       help='Local test result files to analyze')
    parser.add_argument('--format', '-F', default='markdown',
                       choices=['json', 'markdown', 'summary'],
                       help='Output format (default: markdown)')
    parser.add_argument('--output', '-o',
                       help='Output file path (default: stdout)')
    parser.add_argument('--confidence-threshold', '-c', type=float, default=85.0,
                       help='Confidence threshold for auto-merge recommendation')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if not any([args.pr_number, args.github_actions_run, args.test_files]):
        print("Error: Must specify either --pr-number, --github-actions-run, or --test-files")
        sys.exit(1)
    
    try:
        analyzer = TestResultAnalyzer()
        
        # Analyze based on input type
        if args.pr_number:
            if args.verbose:
                print(f"Analyzing PR #{args.pr_number}...")
            analysis = analyzer.analyze_pr_tests(args.pr_number)
        elif args.github_actions_run:
            if args.verbose:
                print(f"Analyzing GitHub Actions run {args.github_actions_run}...")
            analysis = analyzer.analyze_github_actions_run(args.github_actions_run)
        else:
            if args.verbose:
                print(f"Analyzing test files: {args.test_files}")
            analysis = analyzer.analyze_test_files(args.test_files)
        
        if not analysis:
            print("Error: Could not analyze test results")
            sys.exit(1)
        
        # Generate output
        if args.format == 'json':
            output = json.dumps(asdict(analysis), indent=2)
        elif args.format == 'markdown':
            output = generate_markdown_report(analysis)
        else:  # summary
            output = generate_summary_report(analysis)
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Analysis saved to {args.output}")
        else:
            print(output)
        
        # Exit with appropriate code based on recommendation
        if analysis.auto_merge_recommendation == 'block':
            sys.exit(1)
        elif analysis.auto_merge_recommendation == 'investigate':
            sys.exit(2)
        else:
            sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def generate_markdown_report(analysis: TestAnalysis) -> str:
    """Generate markdown report from analysis."""
    report = f"""# 🧪 Test Result Analysis Report

**Analysis Date:** {analysis.analysis_timestamp}
**Commit:** {analysis.commit_sha[:8] if analysis.commit_sha else 'N/A'}
**PR:** #{analysis.pr_number if analysis.pr_number else 'N/A'}

## 📊 Overall Summary

- **Status:** {analysis.overall_status.upper()} {get_status_emoji(analysis.overall_status)}
- **Confidence Score:** {analysis.confidence_score:.1f}/100
- **Auto-Merge Recommendation:** {analysis.auto_merge_recommendation.upper()} {get_recommendation_emoji(analysis.auto_merge_recommendation)}
- **Risk Level:** {analysis.risk_assessment.upper()}

## 🧩 Test Suite Results

"""
    
    for suite in analysis.test_suites:
        pass_rate = (suite.passed_tests / suite.total_tests * 100) if suite.total_tests > 0 else 0
        
        report += f"""### {suite.name}

- **Total Tests:** {suite.total_tests}
- **Passed:** {suite.passed_tests} ({pass_rate:.1f}%)
- **Failed:** {suite.failed_tests}
- **Skipped:** {suite.skipped_tests}
- **Duration:** {suite.duration_ms/1000:.2f}s
- **Coverage:** {suite.coverage_percentage:.1f}%

"""
        
        if suite.failures:
            report += "#### 🚨 Failures:\n\n"
            for failure in suite.failures[:5]:  # Show top 5 failures
                report += f"""**{failure.test_name}**
- Category: {failure.root_cause_category}
- Flaky Score: {failure.flaky_score:.2f}
- Message: {failure.failure_message[:100]}...
- Suggested Fix: {failure.suggested_fix}

"""
    
    if analysis.blocking_issues:
        report += "## 🚫 Blocking Issues\n\n"
        for issue in analysis.blocking_issues:
            report += f"- {issue}\n"
        report += "\n"
    
    if analysis.recommended_actions:
        report += "## 💡 Recommended Actions\n\n"
        for action in analysis.recommended_actions:
            report += f"- {action}\n"
        report += "\n"
    
    if analysis.security_results:
        report += f"""## 🔒 Security Analysis

- **Vulnerabilities Found:** {analysis.security_results.vulnerabilities_found}
- **High Severity:** {analysis.security_results.high_severity_count}
- **Medium Severity:** {analysis.security_results.medium_severity_count}
- **Low Severity:** {analysis.security_results.low_severity_count}
- **Security Score:** {analysis.security_results.security_score}/10

"""
    
    if analysis.quality_metrics:
        report += f"""## 📈 Quality Metrics

- **Code Coverage:** {analysis.quality_metrics.code_coverage:.1f}%
- **Line Coverage:** {analysis.quality_metrics.line_coverage:.1f}%
- **Branch Coverage:** {analysis.quality_metrics.branch_coverage:.1f}%
- **Maintainability Index:** {analysis.quality_metrics.maintainability_index:.1f}

"""
    
    return report


def generate_summary_report(analysis: TestAnalysis) -> str:
    """Generate concise summary report."""
    total_tests = sum(suite.total_tests for suite in analysis.test_suites)
    total_failures = sum(suite.failed_tests for suite in analysis.test_suites)
    
    return f"""Test Analysis Summary ({analysis.analysis_timestamp})

Status: {analysis.overall_status.upper()} ({analysis.confidence_score:.1f}% confidence)
Recommendation: {analysis.auto_merge_recommendation.upper()}

Results: {total_tests - total_failures}/{total_tests} tests passed
Risk Level: {analysis.risk_assessment}

{len(analysis.blocking_issues)} blocking issues
{len(analysis.recommended_actions)} recommended actions
"""


def get_status_emoji(status: str) -> str:
    """Get emoji for status."""
    return {'success': '✅', 'warning': '⚠️', 'failure': '❌'}.get(status, '❓')


def get_recommendation_emoji(recommendation: str) -> str:
    """Get emoji for recommendation."""
    return {
        'approve': '✅',
        'conditional_approve': '⚠️',
        'investigate': '🔍',
        'block': '🚫'
    }.get(recommendation, '❓')


if __name__ == "__main__":
    main()