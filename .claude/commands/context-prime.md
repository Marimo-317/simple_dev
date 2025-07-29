# Context Priming Command

Primes Claude with comprehensive project understanding for better assistance.

## Behavior

- Loads repository structure and file listing
- Reads project documentation (README.md)
- Establishes development context and project goals
- Sets up collaboration parameters for effective AI assistance

## Process

1. **Repository Analysis**
   - Execute `git ls-files` to get tracked files
   - Respect `.cursorignore` and `.gitignore` patterns
   - Provide structured file tree overview
   - Identify key project files and directories

2. **Documentation Loading**
   - Read README.md for project overview
   - Parse package.json/pyproject.toml for dependencies
   - Identify project type and tech stack
   - Understand build tools and scripts

3. **Context Establishment**
   - Set project goals and objectives
   - Understand development workflow
   - Identify coding standards and conventions
   - Establish collaboration preferences

## Information Gathered

- **Project Structure**: Directory layout and organization
- **Technology Stack**: Languages, frameworks, tools used
- **Dependencies**: External libraries and packages
- **Build System**: Scripts, configuration, deployment
- **Documentation**: Project description, setup instructions
- **Development Workflow**: Git workflow, testing approach

## Output Format

Provides a structured summary including:

- Project overview and purpose
- Key directories and their roles
- Important configuration files
- Development setup instructions
- Coding standards and conventions
- Next steps for development

## Usage

Run this command at the beginning of a session or when switching contexts to ensure Claude has full understanding of your project structure and goals.
