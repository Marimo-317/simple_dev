#!/usr/bin/env python3
"""
Advanced Issue Parser with AI-powered Analysis

This script uses natural language processing and AI techniques to analyze GitHub issues,
extract actionable tasks, estimate complexity, and identify dependencies.

Usage:
    python issue-parser.py --issue-number 123 --output-format json
    python issue-parser.py --issue-url https://github.com/owner/repo/issues/123
"""

import os
import sys
import json
import argparse
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class TaskEstimate:
    """Task complexity estimation."""
    story_points: int
    hours_estimate: float
    confidence: float
    complexity_factors: List[str]


@dataclass
class TaskDependency:
    """Task dependency information."""
    depends_on: List[str]
    blocks: List[str]
    related_issues: List[str]
    external_dependencies: List[str]


@dataclass
class AgentAssignment:
    """Recommended agent assignment."""
    primary_agent: str
    secondary_agents: List[str]
    rationale: str
    required_skills: List[str]


@dataclass
class ParsedTask:
    """Parsed task with all analysis."""
    id: str
    title: str
    description: str
    type: str
    priority: str
    estimate: TaskEstimate
    dependencies: TaskDependency
    agent_assignment: AgentAssignment
    acceptance_criteria: List[str]
    technical_requirements: List[str]
    risks: List[str]


@dataclass
class IssueAnalysis:
    """Complete issue analysis result."""
    issue_number: int
    title: str
    original_content: str
    analysis_timestamp: str
    tasks: List[ParsedTask]
    overall_estimate: TaskEstimate
    critical_path: List[str]
    recommended_approach: str
    quality_score: float


class IssueParser:
    """Advanced issue parser with AI capabilities."""
    
    def __init__(self):
        self.agent_skills = self._load_agent_skills()
        self.complexity_patterns = self._load_complexity_patterns()
        self.dependency_keywords = self._load_dependency_keywords()
    
    def _load_agent_skills(self) -> Dict[str, Dict[str, Any]]:
        """Load agent skills mapping from agent files."""
        agent_skills = {}
        agents_dir = Path(".claude/agents")
        
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                agent_name = agent_file.stem
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract skills from agent description
                skills = self._extract_agent_skills(content)
                agent_skills[agent_name] = {
                    'skills': skills,
                    'focus_areas': self._extract_focus_areas(content),
                    'output_types': self._extract_output_types(content)
                }
        
        return agent_skills
    
    def _extract_agent_skills(self, content: str) -> List[str]:
        """Extract skills from agent markdown content."""
        skills = []
        
        # Look for focus areas, skills, or capabilities sections
        sections = re.findall(r'(?:Focus Areas|Skills|Capabilities):\s*\n(.*?)(?=\n##|\n---|\Z)', 
                             content, re.DOTALL | re.IGNORECASE)
        
        for section in sections:
            # Extract bulleted items
            items = re.findall(r'^\s*[-*]\s*(.+)', section, re.MULTILINE)
            skills.extend([item.strip() for item in items])
        
        return skills
    
    def _extract_focus_areas(self, content: str) -> List[str]:
        """Extract focus areas from agent content."""
        focus_match = re.search(r'## Focus Areas\s*\n(.*?)(?=\n##|\Z)', 
                               content, re.DOTALL)
        if focus_match:
            areas = re.findall(r'^\s*[-*]\s*(.+)', focus_match.group(1), re.MULTILINE)
            return [area.strip() for area in areas]
        return []
    
    def _extract_output_types(self, content: str) -> List[str]:
        """Extract output types from agent content."""
        output_match = re.search(r'## Output\s*\n(.*?)(?=\n##|\Z)', 
                                content, re.DOTALL)
        if output_match:
            outputs = re.findall(r'^\s*[-*]\s*(.+)', output_match.group(1), re.MULTILINE)
            return [output.strip() for output in outputs]
        return []
    
    def _load_complexity_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load patterns for complexity estimation."""
        return {
            'high_complexity': {
                'keywords': ['integration', 'migration', 'refactor', 'architecture', 
                           'security', 'performance', 'scalability', 'distributed'],
                'patterns': [r'multiple\s+(?:systems|services|components)',
                           r'cross-(?:cutting|platform|service)',
                           r'backward\s+compatibility',
                           r'(?:data|schema)\s+migration'],
                'multiplier': 2.0
            },
            'medium_complexity': {
                'keywords': ['api', 'database', 'authentication', 'validation', 
                           'testing', 'ui', 'frontend', 'backend'],
                'patterns': [r'new\s+(?:feature|component|service)',
                           r'(?:extend|enhance)\s+existing',
                           r'third-party\s+integration'],
                'multiplier': 1.5
            },
            'low_complexity': {
                'keywords': ['fix', 'update', 'change', 'modify', 'adjust'],
                'patterns': [r'(?:bug|issue)\s+fix',
                           r'minor\s+(?:change|update)',
                           r'configuration\s+change'],
                'multiplier': 1.0
            }
        }
    
    def _load_dependency_keywords(self) -> Dict[str, List[str]]:
        """Load keywords that indicate dependencies."""
        return {
            'blocking': ['depends on', 'requires', 'needs', 'blocked by', 'prerequisite'],
            'related': ['related to', 'similar to', 'part of', 'connected to'],
            'external': ['third-party', 'external', 'vendor', 'api', 'service']
        }
    
    def fetch_issue_content(self, issue_number: int) -> Optional[Dict[str, Any]]:
        """Fetch issue content using GitHub CLI."""
        try:
            # Get issue details
            cmd = ['gh', 'issue', 'view', str(issue_number), '--json', 
                   'title,body,labels,assignees,milestone,comments,state']
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  encoding='utf-8', check=True)
            
            if result.stdout:
                issue_data = json.loads(result.stdout)
                return issue_data
            else:
                print(f"No output received from gh command for issue {issue_number}")
                return None
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Failed to fetch issue {issue_number}: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Error details: {e.stderr}")
            return None
    
    def parse_issue_content(self, issue_data: Dict[str, Any]) -> IssueAnalysis:
        """Parse issue content and extract structured information."""
        content = issue_data.get('body', '')
        title = issue_data.get('title', '')
        issue_number = issue_data.get('number', 0)
        
        # Extract tasks from content
        tasks = self._extract_tasks_from_content(content, title)
        
        # Analyze dependencies
        self._analyze_dependencies(tasks, content)
        
        # Estimate complexity
        self._estimate_task_complexity(tasks, content)
        
        # Assign agents
        self._assign_agents_to_tasks(tasks)
        
        # Calculate overall metrics
        overall_estimate = self._calculate_overall_estimate(tasks)
        critical_path = self._identify_critical_path(tasks)
        quality_score = self._calculate_quality_score(tasks, content)
        
        return IssueAnalysis(
            issue_number=issue_number,
            title=title,
            original_content=content,
            analysis_timestamp=datetime.now().isoformat(),
            tasks=tasks,
            overall_estimate=overall_estimate,
            critical_path=critical_path,
            recommended_approach=self._generate_approach_recommendation(tasks),
            quality_score=quality_score
        )
    
    def _extract_tasks_from_content(self, content: str, title: str) -> List[ParsedTask]:
        """Extract individual tasks from issue content."""
        tasks = []
        
        # Look for explicit task lists
        task_patterns = [
            r'(?:##\s*|###\s*)?(?:Tasks?|To[- ]?Do|Implementation|Steps?):\s*\n(.*?)(?=\n##|\n---|\Z)',
            r'(?:##\s*|###\s*)?(?:Acceptance Criteria|Requirements?):\s*\n(.*?)(?=\n##|\n---|\Z)',
            r'^\s*[-*]\s*\[.\]\s*(.+)',  # Checkbox items
            r'^\s*\d+\.\s*(.+)'  # Numbered lists
        ]
        
        task_id_counter = 1
        
        for pattern in task_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
            
            for match in matches:
                if isinstance(match, str) and len(match.strip()) > 10:
                    # Extract individual items from the match
                    items = re.findall(r'^\s*[-*\d.]\s*(?:\[.\]\s*)?(.+)', 
                                     match, re.MULTILINE)
                    
                    for item in items:
                        if len(item.strip()) > 10:  # Filter out short items
                            task = self._create_task_from_text(
                                f"task-{task_id_counter}",
                                item.strip(),
                                content
                            )
                            tasks.append(task)
                            task_id_counter += 1
        
        # If no explicit tasks found, create one from the title/description
        if not tasks:
            task = self._create_task_from_text("task-1", title, content)
            tasks.append(task)
        
        return tasks
    
    def _create_task_from_text(self, task_id: str, text: str, full_content: str) -> ParsedTask:
        """Create a ParsedTask from text description."""
        # Determine task type
        task_type = self._classify_task_type(text, full_content)
        
        # Extract priority
        priority = self._extract_priority(text, full_content)
        
        # Create placeholder structures (will be filled by other methods)
        return ParsedTask(
            id=task_id,
            title=text[:100] + "..." if len(text) > 100 else text,
            description=text,
            type=task_type,
            priority=priority,
            estimate=TaskEstimate(0, 0.0, 0.0, []),
            dependencies=TaskDependency([], [], [], []),
            agent_assignment=AgentAssignment("", [], "", []),
            acceptance_criteria=self._extract_acceptance_criteria(text, full_content),
            technical_requirements=self._extract_technical_requirements(text, full_content),
            risks=self._identify_risks(text, full_content)
        )
    
    def _classify_task_type(self, text: str, full_content: str) -> str:
        """Classify task type based on content."""
        text_lower = text.lower()
        content_lower = full_content.lower()
        
        if any(word in text_lower for word in ['bug', 'fix', 'error', 'issue', 'broken']):
            return 'bug'
        elif any(word in text_lower for word in ['test', 'testing', 'spec', 'validation']):
            return 'testing'
        elif any(word in text_lower for word in ['doc', 'documentation', 'readme', 'guide']):
            return 'documentation'
        elif any(word in text_lower for word in ['refactor', 'cleanup', 'optimize', 'improve']):
            return 'refactoring'
        elif any(word in text_lower for word in ['feature', 'implement', 'add', 'create', 'build']):
            return 'feature'
        else:
            return 'task'
    
    def _extract_priority(self, text: str, full_content: str) -> str:
        """Extract priority from text content."""
        text_lower = text.lower()
        content_lower = full_content.lower()
        
        if any(word in content_lower for word in ['critical', 'urgent', 'blocker', 'p0']):
            return 'critical'
        elif any(word in content_lower for word in ['high', 'important', 'p1']):
            return 'high'
        elif any(word in content_lower for word in ['low', 'nice to have', 'p3']):
            return 'low'
        else:
            return 'medium'
    
    def _extract_acceptance_criteria(self, text: str, full_content: str) -> List[str]:
        """Extract acceptance criteria from content."""
        criteria = []
        
        # Look for acceptance criteria sections
        ac_pattern = r'(?:Acceptance Criteria|AC|Definition of Done):\s*\n(.*?)(?=\n##|\n---|\Z)'
        match = re.search(ac_pattern, full_content, re.DOTALL | re.IGNORECASE)
        
        if match:
            items = re.findall(r'^\s*[-*]\s*(?:\[.\]\s*)?(.+)', match.group(1), re.MULTILINE)
            criteria.extend([item.strip() for item in items])
        
        return criteria
    
    def _extract_technical_requirements(self, text: str, full_content: str) -> List[str]:
        """Extract technical requirements from content."""
        requirements = []
        
        # Look for technical sections
        tech_pattern = r'(?:Technical|Implementation|Tech)\s*(?:Requirements?|Details?):\s*\n(.*?)(?=\n##|\n---|\Z)'
        match = re.search(tech_pattern, full_content, re.DOTALL | re.IGNORECASE)
        
        if match:
            items = re.findall(r'^\s*[-*]\s*(.+)', match.group(1), re.MULTILINE)
            requirements.extend([item.strip() for item in items])
        
        return requirements
    
    def _identify_risks(self, text: str, full_content: str) -> List[str]:
        """Identify potential risks from content."""
        risks = []
        text_lower = text.lower()
        
        # Risk indicators
        risk_patterns = {
            'integration': 'Integration complexity with external systems',
            'performance': 'Performance impact on existing systems',
            'security': 'Security implications and vulnerabilities',
            'data': 'Data migration and consistency risks',
            'backward compatibility': 'Breaking changes for existing users',
            'dependency': 'External dependency risks'
        }
        
        for pattern, risk in risk_patterns.items():
            if pattern in text_lower:
                risks.append(risk)
        
        return risks
    
    def _estimate_task_complexity(self, tasks: List[ParsedTask], content: str) -> None:
        """Estimate complexity for all tasks."""
        for task in tasks:
            complexity_score = 1.0
            factors = []
            
            text = (task.description + " " + content).lower()
            
            # Apply complexity patterns
            for complexity_level, data in self.complexity_patterns.items():
                matches = 0
                
                # Check keywords
                for keyword in data['keywords']:
                    if keyword in text:
                        matches += 1
                
                # Check patterns
                for pattern in data['patterns']:
                    if re.search(pattern, text, re.IGNORECASE):
                        matches += 1
                
                if matches > 0:
                    complexity_score *= data['multiplier']
                    factors.append(f"{complexity_level}: {matches} indicators")
            
            # Convert to story points (1-13 scale)
            story_points = min(13, max(1, int(complexity_score * 3)))
            
            # Estimate hours (rough conversion)
            hours_estimate = story_points * 4.0  # 4 hours per story point
            
            # Confidence based on amount of information available
            info_score = len(task.acceptance_criteria) + len(task.technical_requirements)
            confidence = min(100.0, max(20.0, info_score * 10))
            
            task.estimate = TaskEstimate(
                story_points=story_points,
                hours_estimate=hours_estimate,
                confidence=confidence,
                complexity_factors=factors
            )
    
    def _analyze_dependencies(self, tasks: List[ParsedTask], content: str) -> None:
        """Analyze dependencies between tasks and external systems."""
        content_lower = content.lower()
        
        for task in tasks:
            depends_on = []
            blocks = []
            related_issues = []
            external_deps = []
            
            # Look for dependency keywords in task description and full content
            text = (task.description + " " + content).lower()
            
            for dep_type, keywords in self.dependency_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        if dep_type == 'blocking':
                            # Extract what this depends on
                            pattern = f"{keyword}\\s+([^.\\n]+)"
                            matches = re.findall(pattern, text, re.IGNORECASE)
                            depends_on.extend(matches)
                        elif dep_type == 'external':
                            external_deps.append(f"External dependency: {keyword}")
                        elif dep_type == 'related':
                            # Look for issue numbers
                            issue_pattern = r'#(\d+)'
                            issue_matches = re.findall(issue_pattern, text)
                            related_issues.extend([f"#{num}" for num in issue_matches])
            
            task.dependencies = TaskDependency(
                depends_on=depends_on[:5],  # Limit to 5 most relevant
                blocks=blocks,
                related_issues=list(set(related_issues)),
                external_dependencies=external_deps[:3]  # Limit to 3 most relevant
            )
    
    def _assign_agents_to_tasks(self, tasks: List[ParsedTask]) -> None:
        """Assign appropriate agents to tasks based on content analysis."""
        for task in tasks:
            best_agent = ""
            best_score = 0.0
            secondary_agents = []
            required_skills = []
            
            text = task.description.lower()
            
            # Score each agent based on skill match
            for agent_name, agent_data in self.agent_skills.items():
                score = 0.0
                
                # Check focus areas
                for focus_area in agent_data['focus_areas']:
                    if any(word in text for word in focus_area.lower().split()):
                        score += 2.0
                
                # Check skills
                for skill in agent_data['skills']:
                    if any(word in text for word in skill.lower().split()):
                        score += 1.0
                
                # Task type matching
                if task.type == 'bug' and 'debug' in agent_name.lower():
                    score += 3.0
                elif task.type == 'testing' and 'test' in agent_name.lower():
                    score += 3.0
                elif task.type == 'feature' and any(word in agent_name.lower() 
                                                  for word in ['architect', 'developer']):
                    score += 2.0
                
                if score > best_score:
                    if best_agent:
                        secondary_agents.append(best_agent)
                    best_agent = agent_name
                    best_score = score
                elif score > 1.0:
                    secondary_agents.append(agent_name)
            
            # Extract required skills from task
            skill_indicators = ['api', 'database', 'frontend', 'backend', 'security', 
                               'performance', 'testing', 'documentation']
            for indicator in skill_indicators:
                if indicator in text:
                    required_skills.append(indicator)
            
            # Generate rationale
            rationale = f"Selected based on {best_score:.1f} skill match score. "
            if task.type == 'feature':
                rationale += "Primary development task. "
            elif task.type == 'bug':
                rationale += "Debugging and troubleshooting focus. "
            elif task.type == 'testing':
                rationale += "Testing and quality assurance focus."
            
            task.agent_assignment = AgentAssignment(
                primary_agent=best_agent or "general-purpose",
                secondary_agents=secondary_agents[:3],  # Limit to top 3
                rationale=rationale,
                required_skills=required_skills
            )
    
    def _calculate_overall_estimate(self, tasks: List[ParsedTask]) -> TaskEstimate:
        """Calculate overall project estimate."""
        total_points = sum(task.estimate.story_points for task in tasks)
        total_hours = sum(task.estimate.hours_estimate for task in tasks)
        avg_confidence = sum(task.estimate.confidence for task in tasks) / len(tasks) if tasks else 0
        
        all_factors = []
        for task in tasks:
            all_factors.extend(task.estimate.complexity_factors)
        
        return TaskEstimate(
            story_points=total_points,
            hours_estimate=total_hours,
            confidence=avg_confidence,
            complexity_factors=list(set(all_factors))  # Unique factors
        )
    
    def _identify_critical_path(self, tasks: List[ParsedTask]) -> List[str]:
        """Identify critical path through task dependencies."""
        # Simple critical path identification based on dependencies and estimates
        critical_tasks = []
        
        # Find tasks with no dependencies (starting points)
        starting_tasks = [task for task in tasks if not task.dependencies.depends_on]
        
        # Find highest impact tasks
        high_impact_tasks = sorted(tasks, 
                                 key=lambda t: t.estimate.story_points * 
                                             (1 if t.priority == 'low' else 
                                              2 if t.priority == 'medium' else 
                                              3 if t.priority == 'high' else 4),
                                 reverse=True)
        
        # Take top 3-5 most critical tasks
        critical_tasks = [task.id for task in high_impact_tasks[:5]]
        
        return critical_tasks
    
    def _calculate_quality_score(self, tasks: List[ParsedTask], content: str) -> float:
        """Calculate overall quality score for the issue analysis."""
        score = 0.0
        max_score = 100.0
        
        # Completeness score (40 points)
        completeness = 0
        if tasks:
            completeness += 10  # Has tasks
        
        avg_ac = sum(len(task.acceptance_criteria) for task in tasks) / len(tasks) if tasks else 0
        completeness += min(15, avg_ac * 3)  # Acceptance criteria
        
        avg_tech = sum(len(task.technical_requirements) for task in tasks) / len(tasks) if tasks else 0
        completeness += min(15, avg_tech * 3)  # Technical requirements
        
        score += completeness
        
        # Clarity score (30 points)
        clarity = 0
        avg_desc_length = sum(len(task.description) for task in tasks) / len(tasks) if tasks else 0
        clarity += min(15, avg_desc_length / 10)  # Description length
        
        if any('user story' in content.lower() or 'as a' in content.lower() for task in tasks):
            clarity += 15  # Has user story format
        
        score += clarity
        
        # Feasibility score (30 points)
        feasibility = 30  # Start with full points
        for task in tasks:
            if len(task.risks) > 3:
                feasibility -= 5  # Deduct for high risk
            if task.estimate.story_points > 8:
                feasibility -= 5  # Deduct for very high complexity
        
        score += max(0, feasibility)
        
        return min(100.0, score)
    
    def _generate_approach_recommendation(self, tasks: List[ParsedTask]) -> str:
        """Generate recommended implementation approach."""
        if not tasks:
            return "No tasks identified. Consider breaking down the issue further."
        
        total_points = sum(task.estimate.story_points for task in tasks)
        high_priority_count = sum(1 for task in tasks if task.priority in ['high', 'critical'])
        
        recommendations = []
        
        if total_points > 20:
            recommendations.append("Consider breaking this into multiple smaller issues.")
        
        if high_priority_count > len(tasks) * 0.7:
            recommendations.append("High priority issue - consider immediate assignment.")
        
        # Agent diversity
        agents = set(task.agent_assignment.primary_agent for task in tasks)
        if len(agents) > 3:
            recommendations.append("Multi-disciplinary effort - coordinate across teams.")
        
        # Dependencies
        dep_count = sum(len(task.dependencies.depends_on) for task in tasks)
        if dep_count > 0:
            recommendations.append("Has dependencies - plan sequencing carefully.")
        
        if not recommendations:
            recommendations.append("Standard implementation approach suitable.")
        
        return " ".join(recommendations)


def main():
    parser = argparse.ArgumentParser(description='Analyze GitHub issues with AI-powered parsing')
    parser.add_argument('--issue-number', '-n', type=int,
                       help='GitHub issue number to analyze')
    parser.add_argument('--issue-url', '-u',
                       help='GitHub issue URL to analyze')
    parser.add_argument('--output-format', '-f', default='json',
                       choices=['json', 'markdown', 'summary'],
                       help='Output format (default: json)')
    parser.add_argument('--output-file', '-o',
                       help='Output file path (default: stdout)')
    parser.add_argument('--create-subtasks', action='store_true',
                       help='Create GitHub sub-issues for complex tasks')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if not args.issue_number and not args.issue_url:
        print("Error: Must specify either --issue-number or --issue-url")
        sys.exit(1)
    
    # Extract issue number from URL if provided
    issue_number = args.issue_number
    if args.issue_url and not issue_number:
        url_match = re.search(r'/issues/(\d+)', args.issue_url)
        if url_match:
            issue_number = int(url_match.group(1))
        else:
            print("Error: Could not extract issue number from URL")
            sys.exit(1)
    
    try:
        parser = IssueParser()
        
        # Fetch issue data
        if args.verbose:
            print(f"Fetching issue #{issue_number}...")
        
        issue_data = parser.fetch_issue_content(issue_number)
        if not issue_data:
            print(f"Error: Could not fetch issue #{issue_number}")
            sys.exit(1)
        
        # Parse and analyze
        if args.verbose:
            print("Analyzing issue content...")
        
        analysis = parser.parse_issue_content(issue_data)
        
        # Generate output
        if args.output_format == 'json':
            output = json.dumps(asdict(analysis), indent=2)
        elif args.output_format == 'markdown':
            output = generate_markdown_report(analysis)
        else:  # summary
            output = generate_summary_report(analysis)
        
        # Write output
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Analysis saved to {args.output_file}")
        else:
            print(output)
        
        # Create sub-tasks if requested
        if args.create_subtasks and len(analysis.tasks) > 1:
            if args.verbose:
                print(f"Creating {len(analysis.tasks)} sub-issues...")
            create_subtasks(analysis)
    
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def generate_markdown_report(analysis: IssueAnalysis) -> str:
    """Generate markdown report from analysis."""
    report = f"""# Issue Analysis Report: #{analysis.issue_number}

**Title:** {analysis.title}
**Analysis Date:** {analysis.analysis_timestamp}
**Quality Score:** {analysis.quality_score:.1f}/100

## Summary

- **Total Tasks:** {len(analysis.tasks)}
- **Overall Estimate:** {analysis.overall_estimate.story_points} story points ({analysis.overall_estimate.hours_estimate:.1f} hours)
- **Confidence:** {analysis.overall_estimate.confidence:.1f}%
- **Recommended Approach:** {analysis.recommended_approach}

## Task Breakdown

"""
    
    for i, task in enumerate(analysis.tasks, 1):
        report += f"""### Task {i}: {task.title}

- **Type:** {task.type}
- **Priority:** {task.priority}
- **Estimate:** {task.estimate.story_points} points ({task.estimate.hours_estimate:.1f}h)
- **Assigned Agent:** {task.agent_assignment.primary_agent}
- **Required Skills:** {', '.join(task.agent_assignment.required_skills)}

**Description:** {task.description}

**Acceptance Criteria:**
{chr(10).join(f'- [ ] {criteria}' for criteria in task.acceptance_criteria)}

**Technical Requirements:**
{chr(10).join(f'- {req}' for req in task.technical_requirements)}

**Risks:**
{chr(10).join(f'- {risk}' for risk in task.risks)}

---

"""
    
    report += f"""## Critical Path

{chr(10).join(f'- {task_id}' for task_id in analysis.critical_path)}

## Complexity Factors

{chr(10).join(f'- {factor}' for factor in analysis.overall_estimate.complexity_factors)}
"""
    
    return report


def generate_summary_report(analysis: IssueAnalysis) -> str:
    """Generate concise summary report."""
    return f"""Issue #{analysis.issue_number}: {analysis.title}

Summary:
- {len(analysis.tasks)} tasks identified
- {analysis.overall_estimate.story_points} story points total
- {analysis.overall_estimate.hours_estimate:.1f} hours estimated
- Quality score: {analysis.quality_score:.1f}/100

Top recommendations:
- {analysis.recommended_approach}

Primary agents needed:
{chr(10).join(f'- {task.agent_assignment.primary_agent}' for task in analysis.tasks[:3])}
"""


def create_subtasks(analysis: IssueAnalysis) -> None:
    """Create GitHub sub-issues for complex tasks."""
    for task in analysis.tasks:
        if task.estimate.story_points > 3:  # Only create sub-issues for larger tasks
            # This would integrate with the auto-issue-creator
            print(f"Would create sub-issue: {task.title}")


if __name__ == "__main__":
    main()