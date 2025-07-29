#!/usr/bin/env python3
"""
Claude Task Runner MCP Server
Provides MCP interface for Claude Task Runner integration with existing Claude Code environment.
"""

import sys
import os
import subprocess
from typing import Dict, List, Any
from mcp.server import Server
from mcp.types import Tool, TextContent

# Add the task runner to the path
TASK_RUNNER_PATH = os.path.join(os.path.dirname(__file__), "task-runner", ".venv", "Scripts")
TASK_RUNNER_EXE = os.path.join(TASK_RUNNER_PATH, "task-runner.exe")

app = Server("claude-task-runner")

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available Claude Task Runner tools."""
    return [
        Tool(
            name="task_runner_create",
            description="Create a new task runner project from a task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project to create"
                    },
                    "task_list_path": {
                        "type": "string", 
                        "description": "Path to markdown file containing task list"
                    }
                },
                "required": ["project_name", "task_list_path"]
            }
        ),
        Tool(
            name="task_runner_run",
            description="Run tasks with Claude in isolated contexts",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "Name of the project to run"
                    },
                    "use_textual": {
                        "type": "boolean",
                        "description": "Use Textual dashboard for visual progress tracking",
                        "default": True
                    }
                },
                "required": ["project_name"]
            }
        ),
        Tool(
            name="task_runner_status",
            description="Show status of all task runner projects",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="task_runner_clean",
            description="Clean up any running task runner processes",
            inputSchema={
                "type": "object", 
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute Claude Task Runner commands."""
    
    if name == "task_runner_create":
        project_name = arguments["project_name"]
        task_list_path = arguments["task_list_path"]
        
        cmd = [TASK_RUNNER_EXE, "create", project_name, task_list_path]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        return [TextContent(
            type="text",
            text=f"Task Runner Project Creation:\n\nCommand: {' '.join(cmd)}\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}"
        )]
    
    elif name == "task_runner_run":
        project_name = arguments["project_name"]
        use_textual = arguments.get("use_textual", True) 
        
        cmd = [TASK_RUNNER_EXE, "run"]
        if use_textual:
            cmd.append("--textual-dashboard")
        cmd.append(project_name)
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        return [TextContent(
            type="text", 
            text=f"Task Runner Execution:\n\nCommand: {' '.join(cmd)}\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}"
        )]
    
    elif name == "task_runner_status":
        cmd = [TASK_RUNNER_EXE, "status"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        return [TextContent(
            type="text",
            text=f"Task Runner Status:\n\n{result.stdout}\n\nErrors:\n{result.stderr}"
        )]
    
    elif name == "task_runner_clean":
        cmd = [TASK_RUNNER_EXE, "clean"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        return [TextContent(
            type="text",
            text=f"Task Runner Cleanup:\n\n{result.stdout}\n\nErrors:\n{result.stderr}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(main())