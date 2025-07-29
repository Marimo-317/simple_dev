# Hooks Management Command

Manage Claude Code hooks for automated development workflows.

## Available Hook Types

- **PreToolUse**: Execute before Claude uses any tool (can block execution)
- **PostToolUse**: Execute after Claude completes a tool operation
- **Notification**: Trigger when Claude sends notifications
- **Stop**: Execute when Claude finishes generating a response

## Current Configured Hooks

### PostToolUse Hooks

1. **Code Formatting Hook** (Edit|MultiEdit|Write)
   - Automatically runs Prettier on JavaScript/TypeScript files
   - Graceful fallback if Prettier not available

2. **Python Formatting Hook** (Write)
   - Automatically runs Black on Python files
   - Graceful fallback if Black not installed

### Stop Hooks

1. **Session Logging** (\*)
   - Logs completion time of Claude Code sessions

## Hook Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$file_path\""
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

- `"Edit|Write"` - File editing operations
- `"Bash"` - Shell command execution
- `"*"` - All tool operations

## Environment Variables

- `$file_path` - Path of the file being operated on
- `$CLAUDE_FILE_PATHS` - Space-separated list of files
- Standard shell environment variables

## Usage Examples

### Add Test Running Hook

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "npm test -- --testPathPattern=$file_path"
        }
      ]
    }
  ]
}
```

### Add Linting Hook

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "npx eslint --fix \"$file_path\""
        }
      ]
    }
  ]
}
```

### Add Git Auto-commit Hook

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "git add . && git commit -m 'Auto-commit via Claude Code hook'"
        }
      ]
    }
  ]
}
```

## Security Considerations

- Hooks run with your current environment credentials
- Always review hook commands before implementation
- Use specific matchers rather than wildcards when possible
- Test hooks in safe environments first
