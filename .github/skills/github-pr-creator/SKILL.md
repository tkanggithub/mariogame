---
name: github-pr-creator
description: "Use when: creating a GitHub pull request; creating a branch and PR; opening a code review; submitting changes for review. Provides step-by-step GitHub PR workflow with templates and automated tools."
---

# GitHub Pull Request Creator Skill

Create GitHub pull requests with AI-guided workflow. Handles branch creation, file changes, commit, and PR opening with intelligent templates.

## Usage

Type `/github-pr-creator` in Copilot Chat to start the workflow.

### What This Skill Does

✅ Creates feature branches with proper naming conventions
✅ Guides through code changes and commits
✅ Generates PR title and description from context
✅ Creates PR with automatic linking to issues
✅ Validates branch protection rules compliance
✅ Suggests reviewers based on code ownership

## Workflow Steps

### 1. **Branch Creation**
```bash
git checkout -b feature/<feature-name>
# or
git checkout -b bugfix/<bug-name>
git push -u origin <branch-name>
```

### 2. **Make Your Changes**
- Edit files in editor
- Save and validate changes
- Run tests if available

### 3. **Commit Changes**
```bash
git add .
git commit -m "feat: description of changes" 
# or
git commit -m "fix: description of bug fix"
```

### 4. **Create Pull Request**

**Using GitHub CLI (Recommended):**
```bash
gh pr create \
  --title "Your PR Title" \
  --body "Your PR description" \
  --base main \
  --head feature/<feature-name>
```

**Using PyGithub Script:**
```bash
python .github/skills/github-pr-creator/create_pr.py
```

**Using Web Interface:**
1. Go to repository on GitHub.com
2. Click "Pull requests" tab
3. Click "New pull request"
4. Select your branch
5. Add title and description

## Commit Message Convention

Follow this format for clear commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `test:` Test additions
- `style:` Style changes (formatting)
- `chore:` Build, dependencies

### Example:
```
feat(jump-physics): improve gravity calculation

- Adjusted gravity constant from 0.4 to 0.8
- Fixed velocity direction for better jump feel
- Added debug logging for physics values

Closes #42
```

## PR Template

Use this structure for your PR description:

```markdown
## Description
Brief explanation of what changes are being made and why.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Testing
Describe how to test the changes:
1. Step 1
2. Step 2
3. Step 3

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Tools Needed

### GitHub CLI
```bash
# Install
sudo apt-get install gh  # Linux/Ubuntu
brew install gh         # macOS

# Authenticate
gh auth login
```

### Python PyGithub (Optional)
```bash
pip install PyGithub
```

## Scripts Included

### `create_pr.py`
Automated Python script for creating PRs programmatically.

**Usage:**
```bash
python .github/skills/github-pr-creator/create_pr.py
```

### `pr_template.md`
Standard PR description template.

## Best Practices

🎯 **One feature per PR** - Keep PRs focused and reviewable
🎯 **Descriptive titles** - Use commit message conventions in PR title
🎯 **Link issues** - Reference related issues with `Closes #123`
🎯 **Keep it small** - Easier to review means faster merging
🎯 **Add tests** - Include tests for new features/fixes
🎯 **Self-review first** - Review your own code before requesting review

## Common Scenarios

### Creating a feature PR
```bash
git checkout -b feature/add-power-ups
# Make changes
git add .
git commit -m "feat: add power-up system"
gh pr create --title "Add power-up system" --body "Adds mushroom and star power-ups"
```

### Creating a bugfix PR
```bash
git checkout -b bugfix/fix-jump-collision
# Fix bug
git add .
git commit -m "fix: correct collision detection for jumping"
gh pr create --title "Fix jump collision detection" --body "Resolves issue #42"
```

### Creating a documentation PR
```bash
git checkout -b docs/update-readme
# Update docs
git add .
git commit -m "docs: update installation instructions"
gh pr create --title "Update README" --body "Clarifies setup process"
```

## Troubleshooting

**"fatal: 'origin' does not appear to be a git repository"**
→ Make sure you're in the correct directory and the repo is initialized

**"Error: Not authenticated with GitHub"**
→ Run `gh auth login` and choose HTTPS or SSH authentication

**"This branch has conflicts with the base branch"**
→ Update your branch: `git pull origin main` and resolve conflicts

**"Branch protection rule violations"**
→ Ensure PR meets protection requirements (tests passing, approvals, etc.)

## Next Steps After PR Creation

1. **Request reviewers** - Click "Add reviewers" button
2. **Monitor CI/CD** - Check that tests and status checks pass
3. **Address feedback** - Make requested changes in new commits
4. **Merge** - Once approved, click "Squash and merge" or "Rebase and merge"
5. **Clean up** - Delete the feature branch after merging

## Learn More

- [GitHub PR Best Practices](https://github.com/features/issues)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Conventional Commits](https://www.conventionalcommits.org/)
