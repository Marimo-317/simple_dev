#!/bin/bash

# Setup script for devcontainer
echo "🚀 Setting up development environment..."

# Configure git delta if available
if command -v delta >/dev/null 2>&1; then
  echo "📝 Configuring git delta..."
  git config --global core.pager delta
  git config --global interactive.diffFilter 'delta --color-only'
  git config --global delta.navigate true
  git config --global delta.light false
  git config --global merge.conflictstyle diff3
  git config --global diff.colorMoved default
fi

# Install zsh-in-docker for better shell experience
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "🐚 Installing Oh My Zsh..."
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Set up Node.js global packages directory
if command -v npm >/dev/null 2>&1; then
  echo "📦 Configuring npm..."
  npm config set prefix /usr/local/share/npm-global
  echo 'export PATH="/usr/local/share/npm-global/bin:$PATH"' >> ~/.bashrc
  echo 'export PATH="/usr/local/share/npm-global/bin:$PATH"' >> ~/.zshrc
fi

# Set up Python virtual environment if Python is available
if command -v python3 >/dev/null 2>&1; then
  echo "🐍 Setting up Python virtual environment..."
  python3 -m venv /workspace/.venv
  echo 'source /workspace/.venv/bin/activate' >> ~/.bashrc
  echo 'source /workspace/.venv/bin/activate' >> ~/.zshrc
fi

echo "✅ Development environment setup complete!"