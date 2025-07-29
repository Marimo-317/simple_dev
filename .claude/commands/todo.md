---
name: todo
description: Manage project todos in todos.md file
---

# Project Todo Manager

Manage todos in a `todos.md` file at the root of your current project directory.

## Usage Examples:

- `/user:todo add "Fix navigation bug"`
- `/user:todo add "Fix navigation bug" [date/time/"tomorrow"/"next week"]` an optional 2nd parameter to set a due date
- `/user:todo complete 1`
- `/user:todo remove 2`
- `/user:todo list`
- `/user:todo undo 1`

## Instructions:

You are a todo manager for the current project. When this command is invoked:

1. **Determine the project root** by looking for common indicators (.git, package.json, etc.)
2. **Locate or create** `todos.md` in the project root
3. **Parse the command arguments** to determine the action:
   - `add "task description"` - Add a new todo
   - `add "task description" [tomorrow|next week|4 days|June 9|12-24-2025|etc...]` - Add a new todo with the provided due date
   - `due N [tomorrow|next week|4 days|June 9|12-24-2025|etc...]` - Mark todo N with the due date provided
   - `complete N` - Mark todo N as completed and move from the ##Active list to the ##Completed list
   - `remove N` - Remove todo N entirely
   - `undo N` - Mark completed todo N as incomplete
   - `list [N]` or no args - Show all (or N number of) todos in a user-friendly format, with each todo numbered for reference
   - `past due` - Show all of the tasks which are past due and still active
   - `next` - Shows the next active task in the list, this should respect Due dates, if there are any. If not, just show the first todo in the Active list

## Todo Format:

Use this markdown format in todos.md:

```markdown
# Project Todos

## Active

- [ ] Task description here | Due: MM-DD-YYYY (optional)
- [ ] Another active task

## Completed

- [x] Completed task description | Completed: MM-DD-YYYY
```

When adding todos, assign incremental numbers for reference (1, 2, 3, etc.).
When listing todos, show the number alongside each item for easy reference.
