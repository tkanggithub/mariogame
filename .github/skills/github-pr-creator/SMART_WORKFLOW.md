# Smart GitHub PR Workflow - Quick Reference

## One Command, Infinite Scenarios

```bash
python .github/skills/github-pr-creator/create_pr.py
```

This **single command** handles everything:

---

## Scenario 1: You're on `main` or `master`

### What Happens ✨
```
✅ Script detects you're on production branch
✅ Protects main by creating feature branch instead
✅ Asks for feature branch name
✅ Creates and pushes branch to GitHub
✅ Ready for you to code!
```

### Example Run
```
🚀 GitHub PR Creator - Smart Workflow
📌 Current branch: main
📌 Main branch detected: main

🎯 You are on the main branch!
💡 For production safety, let's create a feature branch instead.

📝 Enter new branch name (e.g., feature/my-feature): feature/add-ruuvi-support
⏳ Creating branch 'feature/add-ruuvi-support'...
✅ Branch "feature/add-ruuvi-support" created and pushed

💡 Now make your changes and commit them.
   Then run this tool again to create a PR.
```

**Result:** 
- ✅ You're now on the new branch
- ✅ Ready to make changes
- ✅ Changes are safe from main

---

## Scenario 2: You're on a `feature/` or `bugfix/` branch

### What Happens ✨
```
✅ Script detects you're on feature branch
✅ Compares your branch to main (shows you what changed)
✅ Shows git log comparison
✅ Asks for PR title and description
✅ Creates PR automatically with comparison data
```

### Example Run
```
🚀 GitHub PR Creator - Smart Workflow
📌 Current branch: feature/add-ruuvi-support
📌 Main branch detected: main

🔀 Creating PR from feature/add-ruuvi-support → main

📊 Getting branch information...

📊 Branch Comparison: feature/add-ruuvi-support → main
======================================================================

🚀 feature/add-ruuvi-support is 4 commit(s) ahead:
   • 1a2b3c4 feat: add RuuviTagGameIntegration class
   • 5d6e7f8 feat: implement motion-based controls
   • 9a0b1c2 docs: add Ruuvi integration guide
   • 3d4e5f6 test: verify sensor data polling

📝 PR Title: Add Ruuvi Tag IoT sensor integration for motion controls
📄 PR Description (press Enter twice to finish):
Enables team members to control Mario game with Ruuvi Tag motion sensors.

Includes:
- Motion-based player controls (accelerometer)
- Environmental difficulty scaling (temperature/humidity)
- Real-time sensor telemetry display
- Backstage integration ready for team coordination

----------

✅ PR created successfully!
🔗 PR URL: https://github.com/tkanggithub/mariogame/pull/6
```

**Result:**
- ✅ PR created with branch comparison data
- ✅ Reviewers can see exactly what changed
- ✅ Ready for code review

---

## The Smart Detection Logic

```
┌─ Run: python create_pr.py
│
├─ [Check Current Branch]
│  │
│  ├─ Is it main or master? ──YES──> [Branch Protection Mode]
│  │                              └─> Create feature branch
│  │                              └─> Push to GitHub
│  │                              └─> Prompt to make changes
│  │
│  └─ Is it feature/bugfix? ──YES──> [PR Creation Mode]
│                              └─> Compare with main (ahead/behind)
│                              └─> Show git log comparison
│                              └─> Ask for PR title/description
│                              └─> Create PR with context
│                              └─> Show PR URL
│
└─ Done! ✅
```

---

## Key Commands Under the Hood

### Auto-Detect Main Branch
```python
main_branch = creator.get_main_branch()  # Returns 'main' or 'master'
```

### Compare Branches
```python
comparison = creator.compare_branches('feature/my-feature', 'main')
# Returns: {
#     'ahead': 3,
#     'ahead_commits': ['abc123 feat: ...', ...],
#     'behind': 1,
#     'behind_commits': ['def456 fix: ...']
# }
```

### Compare Git Logs
```python
logs = creator.compare_logs('feature/my-feature', 'main', num_commits=10)
# Returns: {
#     'feature/my-feature_commits': [...],
#     'main_commits': [...]
# }
```

### Create Branch Programmatically
```python
result = creator.create_new_branch('feature/awesome-feature', base_branch='main')
# Returns: {
#     'success': True,
#     'branch': 'feature/awesome-feature',
#     'message': '✅ Branch created and pushed'
# }
```

---

## Workflow Patterns

### Pattern 1: Fresh Feature Development
```
1. On main branch
2. Run: python create_pr.py
3. Create feature/my-feature
4. Make changes and commit
5. Run: python create_pr.py again
6. Create PR automatically
```

### Pattern 2: Bug Fix Quick Path
```
1. On main branch  
2. Run: python create_pr.py
3. Create bugfix/critical-issue
4. Add 1-2 commits
5. Run: python create_pr.py
6. Fast-track PR with comparison
```

### Pattern 3: Collaborative Feature
```
1. Team member A creates feature/shared-feature
2. Team member B checks out same branch
3. Both commit their changes
4. Team member A runs: python create_pr.py
5. PR shows all contributor commits
6. Complete branch comparison for reviewers
```

---

## Branch Names Best Practices

| Type | Prefix | Example |
|------|--------|---------|
| New Feature | `feature/` | `feature/add-ruuvi-integration` |
| Bug Fix | `bugfix/` | `bugfix/jump-physics-issue` |
| Refactoring | `refactor/` | `refactor/game-loop-cleanup` |
| Documentation | `docs/` | `docs/update-readme` |
| Testing | `test/` | `test/add-physics-tests` |

---

## Error Handling

### "Could not detect main branch"
- Check remote has `main` or `master`: `git branch -r`
- If using different name, create tracking: `git push -u origin master`

### "Branch already exists"
- Use different name: `feature/add-ruuvi-support-v2`
- Or delete existing: `git branch -D feature/name && git push -d origin feature/name`

### "PR creation failed"
- Check GitHub credentials: `gh auth status`
- Verify GITHUB_TOKEN: `echo $GITHUB_TOKEN`
- Ensure branch is pushed: `git push -u origin branch-name`

---

## Environment Setup

### One-Time Setup
```bash
# Install GitHub CLI
brew install gh  # macOS
# or
sudo apt-get install gh  # Ubuntu/Debian

# Authenticate
gh auth login

# Optionally set token
export GITHUB_TOKEN="ghp_your_token_here"
```

### Verify Setup
```bash
gh auth status  # Should show you're logged in
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Customization

### Use Different Base Branch
Edit the script's default base branch:
```python
# In create_pr() method, change:
base=main_branch  # Modify to use custom branch
```

### Skip Comparison Info
Remove these lines to skip branch/log comparison:
```python
comparison = creator.compare_branches(current_branch, main_branch)
creator.display_branch_comparison(comparison)
```

### Auto-Generate PR Description
Extend the PR body with custom template:
```python
body += f"""
## Testing Done
- [ ] Manual testing
- [ ] Unit tests added
- [ ] Integration tests passed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for clarity
"""
```

---

## Integration with CI/CD

### GitHub Actions Integration
```yaml
name: Auto-Create PR
on:
  push:
    branches:
      - feature/*
jobs:
  pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create PR with script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python .github/skills/github-pr-creator/create_pr.py
```

### Backstage Integration
The PR creator can be invoked from Backstage:
```yaml
# backstage/app-config.yaml integration
scaffolder:
  actions:
    github-pr-creator:
      - name: Create Feature Branch
        action: github:pr-creator:create-branch
```

---

## Support

For issues:
1. Check branch exists: `git branch -a`
2. Check commit history: `git log --oneline -5`
3. Test comparison: `git log main..feature/name --oneline`
4. Verify GitHub access: `gh repo view`

---

**Smart PR Workflow Ready! 🚀**
