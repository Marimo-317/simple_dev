#!/usr/bin/env python3
"""
Automatic GitHub Issue Creator

This script analyzes requirements documents and automatically creates GitHub issues
with proper formatting, labels, and metadata.

Usage:
    python auto-issue-creator.py --input requirements.md --priority high --assignee @username
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


class IssueCreator:
    def __init__(self):
        self.github_cli_available = self._check_github_cli()
        self.issue_templates = self._load_issue_templates()
        
    def _check_github_cli(self) -> bool:
        """Check if GitHub CLI is available."""
        try:
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _load_issue_templates(self) -> Dict[str, str]:
        """Load issue templates for different types."""
        return {
            'feature': '''## User Story
As a {user_type}, I want {goal} so that {benefit}.

## Acceptance Criteria
{acceptance_criteria}

## Technical Requirements
{technical_requirements}

## Definition of Done
- [ ] Feature implemented according to acceptance criteria
- [ ] Unit tests written and passing (>90% coverage)
- [ ] Integration tests added
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Performance impact assessed
- [ ] Security review passed

## Additional Notes
{additional_notes}
''',
            'bug': '''## Bug Report

**Describe the bug**
{description}

**Steps to Reproduce**
{steps_to_reproduce}

**Expected Behavior**
{expected_behavior}

**Actual Behavior**
{actual_behavior}

**Environment**
{environment_info}

**Additional Context**
{additional_context}
''',
            'enhancement': '''## Enhancement Request

**Problem Statement**
{problem_statement}

**Proposed Solution**
{proposed_solution}

**Alternative Solutions**
{alternative_solutions}

**Impact Assessment**
{impact_assessment}

**Acceptance Criteria**
{acceptance_criteria}
''',
            'task': '''## Task Description
{description}

## Requirements
{requirements}

## Implementation Notes
{implementation_notes}

## Definition of Done
{definition_of_done}
'''
        }
    
    def parse_requirements_document(self, file_path: str) -> List[Dict[str, any]]:
        """Parse requirements document and extract issues."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Extract user stories using regex patterns
        user_story_pattern = r'(?:##\s*|###\s*)?(?:User Story|Feature|Requirement):\s*(.+?)(?=##|###|$)'
        stories = re.findall(user_story_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for story in stories:
            issue = self._parse_user_story(story.strip())
            if issue:
                issues.append(issue)
        
        # Extract individual requirements
        requirement_pattern = r'-\s*(.+?)(?=\n-|\n\n|$)'
        requirements = re.findall(requirement_pattern, content, re.DOTALL)
        
        for req in requirements:
            if len(req.strip()) > 20:  # Filter out short items
                issue = self._create_requirement_issue(req.strip())
                issues.append(issue)
        
        return issues
    
    def _parse_user_story(self, story_text: str) -> Optional[Dict[str, any]]:
        """Parse individual user story into issue format."""
        lines = story_text.split('\n')
        title = lines[0] if lines else "Untitled Story"
        
        # Extract user story components
        as_match = re.search(r'As (?:a |an )?(.+?),', story_text, re.IGNORECASE)
        want_match = re.search(r'I want (.+?)(?:so that|$)', story_text, re.IGNORECASE)
        benefit_match = re.search(r'so that (.+?)(?:\.|$)', story_text, re.IGNORECASE)
        
        user_type = as_match.group(1) if as_match else "user"
        goal = want_match.group(1) if want_match else "achieve functionality"
        benefit = benefit_match.group(1) if benefit_match else "improve user experience"
        
        # Extract acceptance criteria
        criteria_match = re.search(r'Acceptance Criteria:(.+?)(?=\n\n|\n#|$)', 
                                 story_text, re.DOTALL | re.IGNORECASE)
        acceptance_criteria = self._format_acceptance_criteria(
            criteria_match.group(1) if criteria_match else ""
        )
        
        return {
            'title': title,
            'type': 'feature',
            'user_type': user_type,
            'goal': goal,
            'benefit': benefit,
            'acceptance_criteria': acceptance_criteria,
            'technical_requirements': self._extract_technical_requirements(story_text),
            'additional_notes': self._extract_additional_notes(story_text)
        }
    
    def _create_requirement_issue(self, requirement: str) -> Dict[str, any]:
        """Create issue from a single requirement."""
        return {
            'title': f"Implement: {requirement[:50]}...",
            'type': 'task',
            'description': requirement,
            'requirements': [requirement],
            'implementation_notes': "",
            'definition_of_done': [
                "Requirement implemented",
                "Tests written and passing",
                "Code reviewed",
                "Documentation updated"
            ]
        }
    
    def _format_acceptance_criteria(self, criteria_text: str) -> str:
        """Format acceptance criteria as checkboxes."""
        lines = [line.strip() for line in criteria_text.split('\n') if line.strip()]
        formatted = []
        
        for line in lines:
            if line.startswith('-') or line.startswith('*'):
                line = line[1:].strip()
            if not line.startswith('- [ ]'):
                line = f"- [ ] {line}"
            formatted.append(line)
        
        return '\n'.join(formatted)
    
    def _extract_technical_requirements(self, text: str) -> str:
        """Extract technical requirements from text."""
        tech_pattern = r'(?:Technical|Implementation|Tech)\s*Requirements?:(.+?)(?=\n\n|\n#|$)'
        match = re.search(tech_pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_additional_notes(self, text: str) -> str:
        """Extract additional notes from text."""
        notes_pattern = r'(?:Notes?|Additional|Comments?):(.+?)(?=\n\n|\n#|$)'
        match = re.search(notes_pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def create_github_issue(self, issue_data: Dict[str, any], 
                           priority: str = "medium", 
                           assignee: Optional[str] = None,
                           milestone: Optional[str] = None) -> bool:
        """Create GitHub issue using gh CLI."""
        if not self.github_cli_available:
            print("GitHub CLI not available. Please install gh CLI.")
            return False
        
        # Format issue body using template
        template = self.issue_templates.get(issue_data['type'], self.issue_templates['task'])
        body = template.format(**issue_data)
        
        # Prepare gh CLI command
        cmd = ['gh', 'issue', 'create', 
               '--title', issue_data['title'],
               '--body', body]
        
        # Add labels
        labels = [f"type:{issue_data['type']}", f"priority:{priority}"]
        if issue_data['type'] == 'feature':
            labels.append('enhancement')
        elif issue_data['type'] == 'bug':
            labels.append('bug')
        
        cmd.extend(['--label', ','.join(labels)])
        
        # Add assignee if specified
        if assignee:
            cmd.extend(['--assignee', assignee])
        
        # Add milestone if specified
        if milestone:
            cmd.extend(['--milestone', milestone])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            issue_url = result.stdout.strip()
            print(f"Created issue: {issue_url}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create issue: {e.stderr}")
            return False
    
    def process_requirements_file(self, file_path: str, 
                                priority: str = "medium",
                                assignee: Optional[str] = None,
                                milestone: Optional[str] = None,
                                dry_run: bool = False) -> List[Dict[str, any]]:
        """Process requirements file and create issues."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Requirements file not found: {file_path}")
        
        issues = self.parse_requirements_document(file_path)
        created_issues = []
        
        print(f"Found {len(issues)} issues to create from {file_path}")
        
        for i, issue_data in enumerate(issues, 1):
            print(f"\nProcessing issue {i}/{len(issues)}: {issue_data['title']}")
            
            if dry_run:
                print("DRY RUN - Would create issue:")
                print(f"  Title: {issue_data['title']}")
                print(f"  Type: {issue_data['type']}")
                print(f"  Priority: {priority}")
                created_issues.append(issue_data)
            else:
                success = self.create_github_issue(issue_data, priority, assignee, milestone)
                if success:
                    created_issues.append(issue_data)
        
        return created_issues


def main():
    parser = argparse.ArgumentParser(description='Automatically create GitHub issues from requirements')
    parser.add_argument('--input', '-i', required=True, 
                       help='Input requirements file (markdown format)')
    parser.add_argument('--priority', '-p', default='medium',
                       choices=['low', 'medium', 'high', 'critical'],
                       help='Issue priority (default: medium)')
    parser.add_argument('--assignee', '-a', 
                       help='GitHub username to assign issues to')
    parser.add_argument('--milestone', '-m',
                       help='Milestone to assign issues to')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be created without actually creating issues')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        creator = IssueCreator()
        created_issues = creator.process_requirements_file(
            args.input, 
            args.priority, 
            args.assignee, 
            args.milestone,
            args.dry_run
        )
        
        print(f"\nSummary: {'Would create' if args.dry_run else 'Created'} {len(created_issues)} issues")
        
        if args.verbose:
            for issue in created_issues:
                print(f"  - {issue['title']} ({issue['type']})")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()