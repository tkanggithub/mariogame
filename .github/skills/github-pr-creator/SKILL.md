---
name: github-pr-creator
description: "Smart GitHub PR workflow that compares branches/logs, auto-detects main branch, creates feature branches from main, and creates PRs from feature branches. Use when: creating PRs, managing branches, submitting code for review, comparing branches."
---

# GitHub Pull Request Creator Skill (Enhanced)

Intelligent GitHub pull request workflow with automatic branch detection, branch comparison, and smart PR creation.

## ✨ New Features

✨ **Smart Branch Detection** - Automatically detects main or master branch
✨ **Branch Comparison** - Shows commits ahead/behind between branches
✨ **Git Log Comparison** - Displays commit history from each branch
✨ **Auto-Branch Creation** - Creates new feature branch if you're on main/master
✨ **Automatic PR Creation** - Creates PR if you're on a feature branch
✨ **One-Command Workflow** - Single command handles all scenarios

## Usage

Type `/github-pr-creator` in Copilot Chat to start the smart workflow.

### What This Skill Does Per Scenario

#### Scenario 1: You're on Main/Master Branch
```
✅ Detects you're on main/master
✅ Shows main branch information
✅ Asks you to create a feature branch
✅ Creates and pushes the new branch
✅ Ready for you to make changes
```

**Command:**
```bash
python .github/skills/github-pr-creator/create_pr.py
```

**Output:**
```
🚀 GitHub PR Creator - Smart Workflow
📌 Current branch: main
📌 Main branch detected: main

🎯 You are on the main branch!
💡 For production safety, let's create a feature branch instead.

📝 Enter new branch name (e.g., feature/my-feature): feature/add-jump-physics
⏳ Creating branch 'feature/add-jump-physics'...
✅ Branch "feature/add-jump-physics" created and pushed

💡 Now make your changes and commit them.
   Then run this tool again to create a PR.
```

#### Scenario 2: You're on a Feature Branch
```
✅ Detects you're on a feature branch
✅ Compares your branch with main/master
✅ Shows commits ahead/behind
✅ Shows git log comparison
✅ Asks for PR title and description
✅ Creates PR automatically
```

**Command:**
```bash
python .github/skills/github-pr-creator/create_pr.py
```

**Output:**
```
🚀 GitHub PR Creator - Smart Workflow
📌 Current branch: feature/add-jump-physics
📌 Main branch detected: main

🔀 Creating PR from feature/add-jump-physics → main

📊 Getting branch information...

📊 Branch Comparison: feature/add-jump-physics → main
======================================================================

🚀 feature/add-jump-physics is 3 commit(s) ahead:
   • abc1234 fix: improve jump velocity calculation
   • def5678 feat: add gravity constant adjustment UI
   • ghi9012 test: verify jump physics

📝 PR Title: Improve jump physics and add gravity adjustment
📄 PR Description:
✅ PR created successfully!
🔗 PR URL: https://github.com/tkanggithub/mariogame/pull/5
```

## Features in Detail

### 1. **Branch Comparison**

Automatically compares your feature branch with the main branch:

```
📊 Branch Comparison: feature/add-feature → main
================================================

🚀 feature/add-feature is 3 commit(s) ahead:
   • abc1234 feat: add new feature
   • def5678 refactor: code cleanup
   • ghi9012 test: add unit tests

⏮️  feature/add-feature is 2 commit(s) behind:
   • jkl3456 fix: critical bug fix in main
   • mno7890 docs: update README
```

This helps you understand:
- ✅ How many new commits you've added
- ⚠️ What changes in main you need to merge
- 📊 Complete picture before creating PR

### 2. **Git Log Comparison**

View commit history from both branches side-by-side:
```
Branch 1: feature/add-feature         Branch 2: main
─────────────────────────────          ──────────────────
abc1234 feat: add new feature          jkl3456 fix: bug fix
def5678 refactor: code cleanup         mno7890 docs: update  
ghi9012 test: add unit tests           pqr1234 chore: deps
```

### 3. **Main Branch Auto-Detection**

Automatically determines which is your main branch:
```bash
git branch -r  # Looks for 'main' or 'master' in remote branches
```

Priority: `main` → `master`

### 4. **Feature Branch Auto-Creation**

If you're on main/master, creates a new feature branch:
```bash
git checkout -b feature/your-feature-name
git push -u origin feature/your-feature-name
```

Naming conventions supported:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Test additions

### 5. **Intelligent PR Creation**

If you're on a feature branch, creates PR automatically:
```bash
gh pr create \
  --title "Your PR Title" \
  --body "Include comparison data" \
  --base main \
  --head feature/your-feature-name
```

## Workflow Steps

### **Standard Workflow**

```
1. Start on main/master
   ↓
2. Run: python create_pr.py
   ↓
3. Gets detected: "You're on main branch"
   ↓
4. Creates new branch: feature/your-feature
   ↓
5. Branch pushed to origin
   ↓
6. Make your changes
   ↓
7. Commit changes
   ↓
8. Run: python create_pr.py again
   ↓
9. Gets detected: "You're on feature branch"
   ↓
10. Compares branches (shows diff)
    ↓
11. Gets comparison data and logs
    ↓
12. Asks for PR title/description
    ↓
13. Creates PR with comparison data
    ↓
14. Displays PR URL
```

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
- `chore:` Build, dependencies, tooling

### Example:
```
feat(jump-physics): improve gravity calculation

- Adjusted gravity constant from 0.4 to 0.8
- Fixed velocity direction for better jump feel
- Added debug logging for physics values

Closes #42
```

## API Reference

### GitHubPRCreator Class

#### Methods

**`get_main_branch()`**
```python
main = creator.get_main_branch()
# Returns: 'main' or 'master'
```

**`is_main_branch(branch_name)`**
```python
if creator.is_main_branch('main'):
    # Create feature branch
```

**`compare_branches(branch1, branch2)`**
```python
result = creator.compare_branches('feature/my-feature', 'main')
# Returns: {
#     'ahead': 3,
#     'ahead_commits': [...],
#     'behind': 2,
#     'behind_commits': [...]
# }
```

**`compare_logs(branch1, branch2, num_commits=10)`**
```python
logs = creator.compare_logs('feature/my-feature', 'main', num_commits=5)
# Returns: {
#     'feature/my-feature_commits': [...],
#     'main_commits': [...]
# }
```

**`create_new_branch(branch_name, base_branch=None)`**
```python
result = creator.create_new_branch('feature/new-feature', base_branch='main')
# Returns: {'success': True/False, 'branch': '...', 'message': '...'}
```

**`create_pr(title, body, head, base='main')`**
```python
result = creator.create_pr(
    title='Add new feature',
    body='Description of changes',
    head='feature/new-feature',
    base='main'
)
# Returns: {'success': True/False, 'url': '...', 'message': '...'}
```

## Requirements

### For Interactive Mode (Recommended)
- Git installed and configured
- GitHub CLI (`gh`) installed
- Authenticated with GitHub

### For API Mode (Alternative)
- Git installed and configured
- PyGithub: `pip install PyGithub`
- GitHub token: Set `GITHUB_TOKEN` environment variable

## Installation

```bash
# Install GitHub CLI (for interactive mode)
# MacOS:
brew install gh

# Ubuntu/Debian:
sudo apt-get install gh

# Or use PyGithub (for API mode)
pip install PyGithub
```

## Environment Variables

```bash
# Set GitHub token (optional, defaults to gh CLI)
export GITHUB_TOKEN="ghp_your_personal_access_token"

# Run the script
python .github/skills/github-pr-creator/create_pr.py
```

## Troubleshooting

### "Could not detect main branch"
```bash
git branch -r  # Check what main branch exists
# If only 'master' exists, it will use that
# If you don't see either, create one:
git push -u origin master  # or main
```

### "Branch creation failed"
```bash
git status                      # Check current state
git checkout main              # Ensure on valid base branch
python create_pr.py            # Try again
```

### "PR creation failed"
```bash
# Check authentication
gh auth status

# Or set token
export GITHUB_TOKEN="ghp_..."
python create_pr.py
```

## Examples

### Example 1: Create Feature Branch from Main
```bash
$ python .github/skills/github-pr-creator/create_pr.py

📌 Current branch: main
🎯 You are on the main branch!
📝 Enter new branch name: feature/ruuvi-integration
✅ Branch "feature/ruuvi-integration" created and pushed
```

### Example 2: Quick PR from Feature Branch
```bash
$ python .github/skills/github-pr-creator/create_pr.py

📌 Current branch: feature/ruuvi-integration
📊 Branch Comparison: feature/ruuvi-integration → main
   🚀 5 commit(s) ahead
   ⏮️ 0 commit(s) behind

📝 PR Title: Add Ruuvi Tag IoT sensor integration
📄 PR Description: [Multi-line input...]
✅ PR #12 created successfully!
🔗 PR URL: https://github.com/username/repo/pull/12
```

---

**Smart PR Creation Made Easy! 🚀**


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
