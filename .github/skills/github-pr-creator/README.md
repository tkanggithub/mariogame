# GitHub PR Creator Skill

A GitHub Copilot skill for creating pull requests with AI guidance and automation.

## Files

- **SKILL.md** - Complete skill documentation and workflow
- **create_pr.py** - Automated PR creation script
- **pr_template.md** - Standard PR description template

## Quick Start

### Option 1: Use in GitHub Copilot Chat

1. Open GitHub Copilot Chat in VS Code
2. Type: `/github-pr-creator`
3. Follow the interactive workflow

### Option 2: Use the Python Script

```bash
# Make script executable
chmod +x create_pr.py

# Run interactively
python .github/skills/github-pr-creator/create_pr.py
```

### Option 3: Use GitHub CLI

```bash
# Install GitHub CLI
sudo apt-get install gh

# Authenticate
gh auth login

# Create PR
gh pr create --title "Your Title" --body "Your description"
```

## Requirements

- Git repository initialized and connected to GitHub
- Either:
  - GitHub CLI installed (`gh`)
  - OR PyGithub installed (`pip install PyGithub`) with GitHub token

## Authentication

### GitHub CLI (Recommended)
```bash
gh auth login
# Choose HTTPS or SSH
# Paste your personal access token
```

### PyGithub
```bash
export GITHUB_TOKEN=your_token_here
python create_pr.py
```

Get a token at: https://github.com/settings/tokens

## Example Workflow

```bash
# 1. Create and checkout feature branch
git checkout -b feature/add-scoring-system

# 2. Make your changes
# (Edit files, add tests, etc.)

# 3. Commit changes
git add .
git commit -m "feat: add scoring system for completing levels"

# 4. Create PR
python .github/skills/github-pr-creator/create_pr.py

# 5. In the script, provide:
#    - Title: "Add scoring system"
#    - Description: "Players earn points by avoiding obstacles..."
#    - Base branch: main
```

## Features

✅ Interactive workflow in GitHub Copilot
✅ Automated branch creation
✅ Commit message conventions
✅ PR template with checklist
✅ Multiple creation methods (CLI, API, Web)
✅ Issue linking support
✅ Reviewer suggestions
✅ Validation checks

## Common Commands

```bash
# Create PR from current branch
gh pr create

# Create PR with custom title
gh pr create --title "My Feature"

# Create PR with template
gh pr create --body-file .github/skills/github-pr-creator/pr_template.md

# View PR status
gh pr status

# List all PRs
gh pr list
```

## Tips

- **Keep PRs small** - Easier to review = faster to merge
- **Use conventional commits** - Makes PR history clear
- **Link issues** - Write "Closes #42" in description
- **Request reviewers** - Use "Add reviewers" on GitHub
- **Self-review first** - Check your own changes before requesting review

## Troubleshooting

### "gh: command not found"
Install GitHub CLI: `https://cli.github.com/`

### "Not authenticated"
Run `gh auth login` and complete the authentication flow

### "PyGithub not found"
Install with: `pip install PyGithub`

### "Repository not found"
Make sure you're in a Git repository with proper remote setup

## More Information

See **SKILL.md** for complete documentation and best practices.
