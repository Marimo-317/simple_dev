#!/usr/bin/env python3
"""
PR Impact Analyzer for Smart Regression Testing

This script analyzes pull request changes to determine the scope of impact
and generate targeted test execution plans to optimize testing efficiency.

Usage:
    python impact-analyzer.py --pr-number 123 --output test-plan.json
    python impact-analyzer.py --commit-range main..feature-branch --format markdown
"""

import os
import sys
import json
import argparse
import subprocess
import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class FileChange:
    """Information about a changed file."""
    file_path: str
    change_type: str  # added, modified, deleted, renamed
    lines_added: int
    lines_deleted: int
    complexity_score: int
    risk_level: str
    affected_functions: List[str]
    affected_classes: List[str]
    test_files: List[str]


@dataclass
class ModuleImpact:
    """Impact analysis for a module or component."""
    module_name: str
    files_changed: List[str]
    risk_score: float
    dependent_modules: List[str]
    test_coverage_percentage: float
    recommended_test_types: List[str]
    regression_risk: str


@dataclass
class TestRecommendation:
    """Test execution recommendation."""
    test_type: str
    test_paths: List[str]
    priority: str
    estimated_duration_minutes: int
    rationale: str
    required: bool


@dataclass
class ImpactAnalysis:
    """Complete PR impact analysis."""
    analysis_timestamp: str
    pr_number: Optional[int]
    commit_range: str
    total_files_changed: int
    file_changes: List[FileChange]
    module_impacts: List[ModuleImpact]
    test_recommendations: List[TestRecommendation]
    overall_risk_score: float
    regression_probability: float
    recommended_test_strategy: str
    estimated_test_time_minutes: int


class ImpactAnalyzer:
    """Analyzes PR impact and generates smart test recommendations."""
    
    def __init__(self):
        self.project_structure = self._analyze_project_structure()
        self.test_mappings = self._load_test_mappings()
        self.dependency_graph = self._build_dependency_graph()
        self.complexity_weights = self._load_complexity_weights()
        self.historical_data = self._load_historical_data()
    
    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze project structure to understand modules and components."""
        structure = {
            'modules': {},
            'test_directories': [],
            'build_files': [],
            'config_files': []
        }
        
        # Find common project patterns
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') 
                      and d not in ['node_modules', '__pycache__', 'target', 'build']]
            
            rel_path = os.path.relpath(root, '.')
            if rel_path == '.':
                rel_path = ''
            
            # Identify test directories
            if any(test_dir in root.lower() for test_dir in ['test', 'spec', '__tests__']):
                structure['test_directories'].append(rel_path)
            
            # Identify build and config files
            for file in files:
                if file in ['package.json', 'pom.xml', 'build.gradle', 'Cargo.toml', 
                           'requirements.txt', 'setup.py', 'Dockerfile']:
                    structure['build_files'].append(os.path.join(rel_path, file))
                elif file.endswith('.config.js') or file in ['.eslintrc', '.prettierrc']:
                    structure['config_files'].append(os.path.join(rel_path, file))
        
        return structure
    
    def _load_test_mappings(self) -> Dict[str, List[str]]:
        """Load or generate mappings between source files and test files."""
        mapping_file = '.claude/data/test-mappings.json'
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Generate basic mappings based on naming conventions
        mappings = {}
        
        # Find all source files
        source_files = []
        for ext in ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c']:
            source_files.extend(Path('.').rglob(f'*{ext}'))
        
        # Find corresponding test files
        for source_file in source_files:
            if any(test_dir in str(source_file) for test_dir in ['test', 'spec', '__tests__']):
                continue
                
            source_path = str(source_file)
            test_files = []
            
            # Common test file patterns
            patterns = [
                f"test_{source_file.stem}.py",
                f"{source_file.stem}_test.py",
                f"{source_file.stem}.test.js",
                f"{source_file.stem}.spec.js",
                f"Test{source_file.stem.capitalize()}.java"
            ]
            
            for pattern in patterns:
                test_matches = list(Path('.').rglob(pattern))
                test_files.extend(str(t) for t in test_matches)
            
            if test_files:
                mappings[source_path] = test_files
        
        return mappings
    
    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """Build dependency graph from import/require statements."""
        dependencies = {}
        
        # Analyze Python files
        for py_file in Path('.').rglob('*.py'):
            deps = self._extract_python_dependencies(py_file)
            if deps:
                dependencies[str(py_file)] = deps
        
        # Analyze JavaScript/TypeScript files
        for js_file in Path('.').rglob('*.js'):
            deps = self._extract_js_dependencies(js_file)
            if deps:
                dependencies[str(js_file)] = deps
        
        for ts_file in Path('.').rglob('*.ts'):
            deps = self._extract_js_dependencies(ts_file)
            if deps:
                dependencies[str(ts_file)] = deps
        
        return dependencies
    
    def _extract_python_dependencies(self, file_path: Path) -> Set[str]:
        """Extract Python import dependencies."""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to find imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            dependencies.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            dependencies.add(node.module)
            except SyntaxError:
                # Fallback to regex parsing
                import_pattern = r'^(?:from\s+(\S+)\s+import|import\s+(\S+))'
                for line in content.split('\n'):
                    match = re.match(import_pattern, line.strip())
                    if match:
                        dep = match.group(1) or match.group(2)
                        dependencies.add(dep.split('.')[0])
        
        except Exception:
            pass
        
        return dependencies
    
    def _extract_js_dependencies(self, file_path: Path) -> Set[str]:
        """Extract JavaScript/TypeScript import dependencies."""
        dependencies = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract import statements
            import_patterns = [
                r"import\s+.*\s+from\s+['\"]([^'\"]+)['\"]",
                r"require\(['\"]([^'\"]+)['\"]\)",
                r"import\(['\"]([^'\"]+)['\"]\)"
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    # Remove relative path indicators and get module name
                    dep = match.replace('./', '').replace('../', '').split('/')[0]
                    if dep and not dep.startswith('.'):
                        dependencies.add(dep)
        
        except Exception:
            pass
        
        return dependencies
    
    def _load_complexity_weights(self) -> Dict[str, float]:
        """Load complexity weights for different file types and patterns."""
        return {
            'file_types': {
                '.py': 1.0,
                '.js': 1.0,
                '.ts': 1.1,
                '.java': 1.2,
                '.cpp': 1.3,
                '.go': 0.9,
                '.rs': 1.1
            },
            'patterns': {
                'test': 0.5,
                'config': 0.3,
                'migration': 1.5,
                'schema': 1.4,
                'api': 1.3,
                'database': 1.4,
                'security': 1.5,
                'auth': 1.4
            },
            'change_types': {
                'added': 1.2,
                'modified': 1.0,
                'deleted': 0.8,
                'renamed': 0.6
            }
        }
    
    def _load_historical_data(self) -> Dict[str, Any]:
        """Load historical data about file change impacts."""
        history_file = '.claude/data/change-impact-history.json'
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {'file_risk_scores': {}, 'module_stability': {}}
    
    def analyze_pr_impact(self, pr_number: int) -> Optional[ImpactAnalysis]:
        """Analyze impact of a specific PR."""
        try:
            # Get PR information and file changes
            cmd = ['gh', 'pr', 'view', str(pr_number), '--json', 
                   'headRefOid,baseRefOid,files,title']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            pr_data = json.loads(result.stdout)
            
            # Get detailed diff information
            head_sha = pr_data.get('headRefOid', '')
            base_sha = pr_data.get('baseRefOid', '')
            commit_range = f"{base_sha}..{head_sha}"
            
            file_changes = self._analyze_file_changes(pr_data.get('files', []))
            
            return self._create_impact_analysis(
                pr_number=pr_number,
                commit_range=commit_range,
                file_changes=file_changes
            )
            
        except Exception as e:
            print(f"Failed to analyze PR {pr_number}: {e}")
            return None
    
    def analyze_commit_range(self, commit_range: str) -> ImpactAnalysis:
        """Analyze impact of a commit range."""
        try:
            # Get file changes in the commit range
            cmd = ['git', 'diff', '--name-status', commit_range]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            file_changes = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[0]
                    file_path = parts[1]
                    
                    # Get detailed change information
                    change = self._analyze_single_file_change(file_path, status, commit_range)
                    if change:
                        file_changes.append(change)
            
            return self._create_impact_analysis(
                pr_number=None,
                commit_range=commit_range,
                file_changes=file_changes
            )
            
        except Exception as e:
            print(f"Failed to analyze commit range {commit_range}: {e}")
            return ImpactAnalysis(
                analysis_timestamp=datetime.now().isoformat(),
                pr_number=None,
                commit_range=commit_range,
                total_files_changed=0,
                file_changes=[],
                module_impacts=[],
                test_recommendations=[],
                overall_risk_score=0.0,
                regression_probability=0.0,
                recommended_test_strategy='full',
                estimated_test_time_minutes=60
            )
    
    def _analyze_file_changes(self, files_data: List[Dict[str, Any]]) -> List[FileChange]:
        """Analyze file changes from GitHub API data."""
        file_changes = []
        
        for file_info in files_data:
            file_path = file_info.get('path', '')
            additions = file_info.get('additions', 0)
            deletions = file_info.get('deletions', 0)
            status = file_info.get('status', 'modified')
            
            change = FileChange(
                file_path=file_path,
                change_type=status,
                lines_added=additions,
                lines_deleted=deletions,
                complexity_score=self._calculate_file_complexity(file_path, additions, deletions),
                risk_level=self._assess_file_risk(file_path, status, additions, deletions),
                affected_functions=self._extract_affected_functions(file_path),
                affected_classes=self._extract_affected_classes(file_path),
                test_files=self.test_mappings.get(file_path, [])
            )
            
            file_changes.append(change)
        
        return file_changes
    
    def _analyze_single_file_change(self, file_path: str, status: str, 
                                   commit_range: str) -> Optional[FileChange]:
        """Analyze a single file change from git diff."""
        try:
            # Get line change statistics
            cmd = ['git', 'diff', '--numstat', commit_range, '--', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            additions, deletions = 0, 0
            if result.stdout.strip():
                parts = result.stdout.strip().split('\t')
                if len(parts) >= 2:
                    try:
                        additions = int(parts[0]) if parts[0] != '-' else 0
                        deletions = int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        pass
            
            return FileChange(
                file_path=file_path,
                change_type=self._normalize_git_status(status),
                lines_added=additions,
                lines_deleted=deletions,
                complexity_score=self._calculate_file_complexity(file_path, additions, deletions),
                risk_level=self._assess_file_risk(file_path, status, additions, deletions),
                affected_functions=self._extract_affected_functions(file_path),
                affected_classes=self._extract_affected_classes(file_path),
                test_files=self.test_mappings.get(file_path, [])
            )
            
        except Exception:
            return None
    
    def _normalize_git_status(self, status: str) -> str:
        """Normalize git status to standard change types."""
        status_map = {
            'A': 'added',
            'M': 'modified',
            'D': 'deleted',
            'R': 'renamed',
            'C': 'copied',
            'T': 'type_changed'
        }
        return status_map.get(status[0], 'modified')
    
    def _calculate_file_complexity(self, file_path: str, additions: int, deletions: int) -> int:
        """Calculate complexity score for a file change."""
        base_score = additions + deletions
        
        # File type multiplier
        file_ext = Path(file_path).suffix
        type_weight = self.complexity_weights['file_types'].get(file_ext, 1.0)
        
        # Pattern-based multiplier
        path_lower = file_path.lower()
        pattern_weight = 1.0
        for pattern, weight in self.complexity_weights['patterns'].items():
            if pattern in path_lower:
                pattern_weight = max(pattern_weight, weight)
        
        return int(base_score * type_weight * pattern_weight)
    
    def _assess_file_risk(self, file_path: str, change_type: str, 
                         additions: int, deletions: int) -> str:
        """Assess risk level of a file change."""
        # Historical risk score
        historical_risk = self.historical_data['file_risk_scores'].get(file_path, 0.5)
        
        # Size-based risk
        change_size = additions + deletions
        if change_size > 500:
            size_risk = 'high'
        elif change_size > 100:
            size_risk = 'medium'
        else:
            size_risk = 'low'
        
        # Pattern-based risk
        path_lower = file_path.lower()
        pattern_risk = 'low'
        for pattern in ['migration', 'schema', 'auth', 'security', 'payment']:
            if pattern in path_lower:
                pattern_risk = 'high'
                break
        
        # Combine risk factors
        risk_factors = [historical_risk, size_risk, pattern_risk]
        if 'high' in risk_factors or historical_risk > 0.7:
            return 'high'
        elif 'medium' in risk_factors or historical_risk > 0.4:
            return 'medium'
        else:
            return 'low'
    
    def _extract_affected_functions(self, file_path: str) -> List[str]:
        """Extract function names that might be affected by changes."""
        functions = []
        
        try:
            if not os.path.exists(file_path):
                return functions
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract function definitions based on file type
            file_ext = Path(file_path).suffix
            
            if file_ext == '.py':
                # Python function pattern
                pattern = r'^def\s+(\w+)\s*\('
                functions = re.findall(pattern, content, re.MULTILINE)
            elif file_ext in ['.js', '.ts']:
                # JavaScript function patterns
                patterns = [
                    r'function\s+(\w+)\s*\(',
                    r'(\w+)\s*:\s*function\s*\(',
                    r'(\w+)\s*=\s*\([^)]*\)\s*=>'
                ]
                for pattern in patterns:
                    functions.extend(re.findall(pattern, content, re.MULTILINE))
            elif file_ext == '.java':
                # Java method pattern
                pattern = r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\('
                functions = re.findall(pattern, content, re.MULTILINE)
        
        except Exception:
            pass
        
        return functions[:10]  # Limit to first 10 functions
    
    def _extract_affected_classes(self, file_path: str) -> List[str]:
        """Extract class names that might be affected by changes."""
        classes = []
        
        try:
            if not os.path.exists(file_path):
                return classes
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract class definitions based on file type
            file_ext = Path(file_path).suffix
            
            if file_ext == '.py':
                pattern = r'^class\s+(\w+)\s*[:\(]'
                classes = re.findall(pattern, content, re.MULTILINE)
            elif file_ext in ['.js', '.ts']:
                pattern = r'class\s+(\w+)\s*[{extends]'
                classes = re.findall(pattern, content)
            elif file_ext == '.java':
                pattern = r'(?:public|private)?\s*class\s+(\w+)\s*[{extends]'
                classes = re.findall(pattern, content)
        
        except Exception:
            pass
        
        return classes[:5]  # Limit to first 5 classes
    
    def _create_impact_analysis(self, pr_number: Optional[int], commit_range: str,
                               file_changes: List[FileChange]) -> ImpactAnalysis:
        """Create comprehensive impact analysis."""
        # Analyze module impacts
        module_impacts = self._analyze_module_impacts(file_changes)
        
        # Generate test recommendations
        test_recommendations = self._generate_test_recommendations(file_changes, module_impacts)
        
        # Calculate overall risk score
        overall_risk_score = self._calculate_overall_risk_score(file_changes, module_impacts)
        
        # Calculate regression probability
        regression_probability = self._calculate_regression_probability(file_changes)
        
        # Determine test strategy
        test_strategy = self._determine_test_strategy(overall_risk_score, regression_probability)
        
        # Estimate test time
        estimated_time = sum(rec.estimated_duration_minutes for rec in test_recommendations)
        
        return ImpactAnalysis(
            analysis_timestamp=datetime.now().isoformat(),
            pr_number=pr_number,
            commit_range=commit_range,
            total_files_changed=len(file_changes),
            file_changes=file_changes,
            module_impacts=module_impacts,
            test_recommendations=test_recommendations,
            overall_risk_score=overall_risk_score,
            regression_probability=regression_probability,
            recommended_test_strategy=test_strategy,
            estimated_test_time_minutes=estimated_time
        )
    
    def _analyze_module_impacts(self, file_changes: List[FileChange]) -> List[ModuleImpact]:
        """Analyze impact at the module level."""
        module_groups = {}
        
        # Group files by module/directory
        for change in file_changes:
            module_name = str(Path(change.file_path).parent)
            if module_name == '.':
                module_name = 'root'
            
            if module_name not in module_groups:
                module_groups[module_name] = []
            module_groups[module_name].append(change)
        
        module_impacts = []
        for module_name, changes in module_groups.items():
            # Calculate module risk score
            risk_scores = [self._risk_level_to_score(change.risk_level) for change in changes]
            avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0.0
            
            # Find dependent modules
            dependent_modules = self._find_dependent_modules(module_name, changes)
            
            # Determine test types needed
            test_types = self._recommend_module_test_types(changes)
            
            # Assess regression risk
            regression_risk = self._assess_module_regression_risk(changes, avg_risk_score)
            
            impact = ModuleImpact(
                module_name=module_name,
                files_changed=[change.file_path for change in changes],
                risk_score=avg_risk_score,
                dependent_modules=dependent_modules,
                test_coverage_percentage=self._estimate_module_coverage(module_name),
                recommended_test_types=test_types,
                regression_risk=regression_risk
            )
            
            module_impacts.append(impact)
        
        return module_impacts
    
    def _risk_level_to_score(self, risk_level: str) -> float:
        """Convert risk level string to numeric score."""
        return {'low': 0.3, 'medium': 0.6, 'high': 0.9}.get(risk_level, 0.5)
    
    def _find_dependent_modules(self, module_name: str, changes: List[FileChange]) -> List[str]:
        """Find modules that depend on the changed module."""
        dependents = set()
        
        for change in changes:
            file_path = change.file_path
            # Look through dependency graph for files that import this one
            for dependent_file, deps in self.dependency_graph.items():
                if any(dep in file_path for dep in deps):
                    dependent_module = str(Path(dependent_file).parent)
                    if dependent_module != module_name:
                        dependents.add(dependent_module)
        
        return list(dependents)[:5]  # Limit to top 5 dependents
    
    def _recommend_module_test_types(self, changes: List[FileChange]) -> List[str]:
        """Recommend test types for a module based on changes."""
        test_types = set()
        
        for change in changes:
            # Based on file patterns and change characteristics
            path_lower = change.file_path.lower()
            
            if any(pattern in path_lower for pattern in ['api', 'endpoint', 'router']):
                test_types.add('integration')
            if any(pattern in path_lower for pattern in ['database', 'model', 'schema']):
                test_types.add('database')
            if any(pattern in path_lower for pattern in ['auth', 'security', 'permission']):
                test_types.add('security')
            if any(pattern in path_lower for pattern in ['ui', 'component', 'view']):
                test_types.add('e2e')
            if change.lines_added + change.lines_deleted > 50:
                test_types.add('performance')
            
            # Always recommend unit tests
            test_types.add('unit')
        
        return list(test_types)
    
    def _assess_module_regression_risk(self, changes: List[FileChange], risk_score: float) -> str:
        """Assess regression risk for a module."""
        high_risk_count = sum(1 for change in changes if change.risk_level == 'high')
        total_complexity = sum(change.complexity_score for change in changes)
        
        if high_risk_count > 0 or risk_score > 0.7 or total_complexity > 1000:
            return 'high'
        elif risk_score > 0.4 or total_complexity > 300:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_module_coverage(self, module_name: str) -> float:
        """Estimate test coverage for a module."""
        # This would ideally integrate with coverage tools
        # For now, provide estimates based on test file presence
        
        module_path = Path(module_name) if module_name != 'root' else Path('.')
        source_files = list(module_path.rglob('*.py')) + list(module_path.rglob('*.js')) + list(module_path.rglob('*.ts'))
        
        if not source_files:
            return 0.0
        
        # Count test files
        test_files = []
        for source_file in source_files:
            test_files.extend(self.test_mappings.get(str(source_file), []))
        
        # Rough estimate based on test file ratio
        if not test_files:
            return 20.0  # Default low coverage
        
        coverage_ratio = len(test_files) / len(source_files)
        return min(95.0, coverage_ratio * 80 + 20)  # Scale to 20-95% range
    
    def _generate_test_recommendations(self, file_changes: List[FileChange],
                                     module_impacts: List[ModuleImpact]) -> List[TestRecommendation]:
        """Generate specific test execution recommendations."""
        recommendations = []
        
        # Unit test recommendations
        unit_test_paths = []
        for change in file_changes:
            unit_test_paths.extend(change.test_files)
        
        if unit_test_paths:
            recommendations.append(TestRecommendation(
                test_type='unit',
                test_paths=list(set(unit_test_paths)),
                priority='high',
                estimated_duration_minutes=len(unit_test_paths) * 2,
                rationale='Direct test coverage for changed files',
                required=True
            ))
        
        # Integration test recommendations
        high_risk_modules = [m for m in module_impacts if m.regression_risk == 'high']
        if high_risk_modules:
            integration_paths = self._find_integration_tests(high_risk_modules)
            if integration_paths:
                recommendations.append(TestRecommendation(
                    test_type='integration',
                    test_paths=integration_paths,
                    priority='high',
                    estimated_duration_minutes=len(integration_paths) * 5,
                    rationale='High-risk modules require integration testing',
                    required=True
                ))
        
        # E2E test recommendations
        ui_changes = [c for c in file_changes if 'ui' in c.file_path.lower() or 'component' in c.file_path.lower()]
        if ui_changes:
            e2e_paths = self._find_e2e_tests()
            if e2e_paths:
                recommendations.append(TestRecommendation(
                    test_type='e2e',
                    test_paths=e2e_paths[:5],  # Limit to 5 most important E2E tests
                    priority='medium',
                    estimated_duration_minutes=30,
                    rationale='UI changes require end-to-end validation',
                    required=False
                ))
        
        # Performance test recommendations
        perf_critical_changes = [c for c in file_changes 
                               if c.complexity_score > 100 or 'performance' in c.file_path.lower()]
        if perf_critical_changes:
            recommendations.append(TestRecommendation(
                test_type='performance',
                test_paths=['tests/performance'],
                priority='medium',
                estimated_duration_minutes=20,
                rationale='Complex changes may impact performance',
                required=False
            ))
        
        # Security test recommendations
        security_changes = [c for c in file_changes 
                          if any(pattern in c.file_path.lower() 
                                for pattern in ['auth', 'security', 'permission', 'login'])]
        if security_changes:
            recommendations.append(TestRecommendation(
                test_type='security',
                test_paths=['tests/security'],
                priority='high',
                estimated_duration_minutes=15,
                rationale='Security-related changes require security validation',
                required=True
            ))
        
        return recommendations
    
    def _find_integration_tests(self, high_risk_modules: List[ModuleImpact]) -> List[str]:
        """Find integration tests relevant to high-risk modules."""
        integration_paths = []
        
        # Look for integration test directories
        for test_dir in self.project_structure.get('test_directories', []):
            if 'integration' in test_dir.lower():
                integration_paths.append(test_dir)
        
        # Look for specific integration test patterns
        for pattern in ['*integration*', '*api*', '*e2e*']:
            integration_paths.extend(str(p) for p in Path('.').rglob(pattern) if 'test' in str(p))
        
        return list(set(integration_paths))[:10]
    
    def _find_e2e_tests(self) -> List[str]:
        """Find end-to-end test files."""
        e2e_paths = []
        
        patterns = ['*e2e*', '*end-to-end*', '*selenium*', '*cypress*', '*playwright*']
        for pattern in patterns:
            e2e_paths.extend(str(p) for p in Path('.').rglob(pattern) if 'test' in str(p))
        
        return list(set(e2e_paths))
    
    def _calculate_overall_risk_score(self, file_changes: List[FileChange],
                                    module_impacts: List[ModuleImpact]) -> float:
        """Calculate overall risk score for the change set."""
        if not file_changes:
            return 0.0
        
        # File-level risk
        file_risk_scores = [self._risk_level_to_score(change.risk_level) for change in file_changes]
        avg_file_risk = sum(file_risk_scores) / len(file_risk_scores)
        
        # Module-level risk
        module_risk_scores = [impact.risk_score for impact in module_impacts]
        avg_module_risk = sum(module_risk_scores) / len(module_risk_scores) if module_risk_scores else 0.0
        
        # Size-based risk
        total_changes = sum(change.lines_added + change.lines_deleted for change in file_changes)
        size_risk = min(1.0, total_changes / 1000)  # Normalize to 0-1 based on 1000 lines
        
        # Combine risk factors
        overall_risk = (avg_file_risk * 0.4 + avg_module_risk * 0.4 + size_risk * 0.2)
        
        return min(1.0, overall_risk)
    
    def _calculate_regression_probability(self, file_changes: List[FileChange]) -> float:
        """Calculate probability of regression based on historical data and change analysis."""
        if not file_changes:
            return 0.0
        
        # Historical regression rates for files
        historical_rates = []
        for change in file_changes:
            file_history = self.historical_data.get('file_risk_scores', {})
            historical_rates.append(file_history.get(change.file_path, 0.1))
        
        base_probability = sum(historical_rates) / len(historical_rates) if historical_rates else 0.1
        
        # Adjust based on change characteristics
        high_risk_changes = sum(1 for change in file_changes if change.risk_level == 'high')
        risk_multiplier = 1.0 + (high_risk_changes * 0.2)
        
        # Adjust based on test coverage
        test_coverage = sum(1 for change in file_changes if change.test_files) / len(file_changes)
        coverage_reducer = 1.0 - (test_coverage * 0.3)
        
        final_probability = base_probability * risk_multiplier * coverage_reducer
        
        return min(1.0, final_probability)
    
    def _determine_test_strategy(self, risk_score: float, regression_probability: float) -> str:
        """Determine the recommended test strategy based on risk analysis."""
        if risk_score > 0.7 or regression_probability > 0.6:
            return 'comprehensive'
        elif risk_score > 0.4 or regression_probability > 0.3:
            return 'targeted'
        elif risk_score > 0.2 or regression_probability > 0.1:
            return 'focused'
        else:
            return 'minimal'


def main():
    parser = argparse.ArgumentParser(description='Analyze PR impact and generate smart test recommendations')
    parser.add_argument('--pr-number', '-p', type=int,
                       help='GitHub PR number to analyze')
    parser.add_argument('--commit-range', '-r',
                       help='Git commit range to analyze (e.g., main..feature-branch)')
    parser.add_argument('--format', '-f', default='markdown',
                       choices=['json', 'markdown', 'summary'],
                       help='Output format (default: markdown)')
    parser.add_argument('--output', '-o',
                       help='Output file path (default: stdout)')
    parser.add_argument('--test-plan-only', action='store_true',
                       help='Output only the test execution plan')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if not any([args.pr_number, args.commit_range]):
        print("Error: Must specify either --pr-number or --commit-range")
        sys.exit(1)
    
    try:
        analyzer = ImpactAnalyzer()
        
        # Analyze based on input type
        if args.pr_number:
            if args.verbose:
                print(f"Analyzing PR #{args.pr_number}...")
            analysis = analyzer.analyze_pr_impact(args.pr_number)
        else:
            if args.verbose:
                print(f"Analyzing commit range {args.commit_range}...")
            analysis = analyzer.analyze_commit_range(args.commit_range)
        
        if not analysis:
            print("Error: Could not analyze changes")
            sys.exit(1)
        
        # Generate output
        if args.test_plan_only:
            output = generate_test_plan_only(analysis)
        elif args.format == 'json':
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
    
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def generate_markdown_report(analysis: ImpactAnalysis) -> str:
    """Generate markdown report from impact analysis."""
    report = f"""# 🎯 PR Impact Analysis Report

**Analysis Date:** {analysis.analysis_timestamp}
**PR:** #{analysis.pr_number if analysis.pr_number else 'N/A'}
**Commit Range:** {analysis.commit_range}

## 📊 Impact Summary

- **Files Changed:** {analysis.total_files_changed}
- **Overall Risk Score:** {analysis.overall_risk_score:.2f}/1.0
- **Regression Probability:** {analysis.regression_probability:.1%}
- **Recommended Strategy:** {analysis.recommended_test_strategy.upper()}
- **Estimated Test Time:** {analysis.estimated_test_time_minutes} minutes

## 📁 File Changes

"""
    
    # Group files by risk level
    for risk_level in ['high', 'medium', 'low']:
        risk_files = [f for f in analysis.file_changes if f.risk_level == risk_level]
        if risk_files:
            report += f"### {risk_level.upper()} Risk Files\n\n"
            for file_change in risk_files:
                report += f"**{file_change.file_path}** ({file_change.change_type})\n"
                report += f"- Lines: +{file_change.lines_added}/-{file_change.lines_deleted}\n"
                report += f"- Complexity: {file_change.complexity_score}\n"
                if file_change.affected_functions:
                    report += f"- Functions: {', '.join(file_change.affected_functions[:3])}\n"
                if file_change.test_files:
                    report += f"- Test Files: {len(file_change.test_files)}\n"
                report += "\n"
    
    report += "## 🏗️ Module Impacts\n\n"
    for module in analysis.module_impacts:
        risk_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(module.regression_risk, '⚪')
        
        report += f"### {module.module_name} {risk_emoji}\n\n"
        report += f"- **Risk Score:** {module.risk_score:.2f}\n"
        report += f"- **Regression Risk:** {module.regression_risk}\n"
        report += f"- **Test Coverage:** {module.test_coverage_percentage:.1f}%\n"
        report += f"- **Files Changed:** {len(module.files_changed)}\n"
        if module.dependent_modules:
            report += f"- **Dependents:** {', '.join(module.dependent_modules[:3])}\n"
        report += f"- **Recommended Tests:** {', '.join(module.recommended_test_types)}\n\n"
    
    report += "## 🧪 Test Recommendations\n\n"
    for recommendation in analysis.test_recommendations:
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(recommendation.priority, '⚪')
        required_text = ' (Required)' if recommendation.required else ' (Optional)'
        
        report += f"### {recommendation.test_type.title()} Tests {priority_emoji}{required_text}\n\n"
        report += f"- **Priority:** {recommendation.priority}\n"
        report += f"- **Duration:** {recommendation.estimated_duration_minutes} minutes\n"
        report += f"- **Rationale:** {recommendation.rationale}\n"
        report += f"- **Paths:** {len(recommendation.test_paths)} test files/directories\n\n"
    
    report += f"## 📋 Execution Plan\n\n"
    report += f"**Strategy:** {analysis.recommended_test_strategy}\n"
    report += f"**Total Estimated Time:** {analysis.estimated_test_time_minutes} minutes\n\n"
    
    # Test execution order
    required_tests = [r for r in analysis.test_recommendations if r.required]
    optional_tests = [r for r in analysis.test_recommendations if not r.required]
    
    if required_tests:
        report += "**Required Tests (in order):**\n"
        for i, test in enumerate(required_tests, 1):
            report += f"{i}. {test.test_type.title()} ({test.estimated_duration_minutes}min)\n"
    
    if optional_tests:
        report += "\n**Optional Tests:**\n"
        for test in optional_tests:
            report += f"- {test.test_type.title()} ({test.estimated_duration_minutes}min)\n"
    
    return report


def generate_summary_report(analysis: ImpactAnalysis) -> str:
    """Generate concise summary report."""
    required_tests = [r for r in analysis.test_recommendations if r.required]
    
    return f"""Impact Analysis Summary ({analysis.analysis_timestamp})

Files Changed: {analysis.total_files_changed}
Risk Score: {analysis.overall_risk_score:.2f}/1.0
Regression Probability: {analysis.regression_probability:.1%}

Test Strategy: {analysis.recommended_test_strategy}
Required Tests: {len(required_tests)}
Estimated Time: {analysis.estimated_test_time_minutes} minutes

High Risk Files: {len([f for f in analysis.file_changes if f.risk_level == 'high'])}
High Risk Modules: {len([m for m in analysis.module_impacts if m.regression_risk == 'high'])}
"""


def generate_test_plan_only(analysis: ImpactAnalysis) -> str:
    """Generate test execution plan only."""
    plan = "# Test Execution Plan\n\n"
    
    required_tests = [r for r in analysis.test_recommendations if r.required]
    optional_tests = [r for r in analysis.test_recommendations if not r.required]
    
    if required_tests:
        plan += "## Required Tests\n\n"
        for test in required_tests:
            plan += f"### {test.test_type.title()}\n"
            plan += f"**Duration:** {test.estimated_duration_minutes} minutes\n"
            plan += f"**Paths:**\n"
            for path in test.test_paths[:10]:  # Limit to 10 paths
                plan += f"- {path}\n"
            plan += "\n"
    
    if optional_tests:
        plan += "## Optional Tests\n\n"
        for test in optional_tests:
            plan += f"### {test.test_type.title()}\n"
            plan += f"**Duration:** {test.estimated_duration_minutes} minutes\n"
            plan += f"**Rationale:** {test.rationale}\n\n"
    
    plan += f"**Total Estimated Time:** {analysis.estimated_test_time_minutes} minutes\n"
    
    return plan


if __name__ == "__main__":
    main()