# Development Container

This directory contains the configuration for a VS Code development container based on Claude Code's devcontainer setup.

## Features

- **Node.js 20**: For JavaScript/TypeScript development
- **Python 3.11**: For Python development
- **Git & GitHub CLI**: Version control and GitHub integration
- **Development Tools**: Essential command-line tools (fzf, jq, vim, etc.)
- **Oh My Zsh**: Enhanced terminal experience
- **Git Delta**: Better git diff visualization
- **VS Code Extensions**: Pre-configured extensions for development

## Usage

1. Install [VS Code](https://code.visualstudio.com/) and the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open this repository in VS Code
3. When prompted, click "Reopen in Container" or run the command "Remote-Containers: Reopen in Container"
4. Wait for the container to build and initialize

## Customization

- Modify `devcontainer.json` to add more VS Code extensions or settings
- Edit `Dockerfile` to install additional tools or packages
- Update `setup.sh` to add custom initialization scripts

## Volumes

- Command history is persisted across container rebuilds
- The workspace is mounted to `/workspace` in the container
