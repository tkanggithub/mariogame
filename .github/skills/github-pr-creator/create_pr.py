#!/usr/bin/env python3
"""
GitHub PR Creator Script
Automated pull request creation with AI-guided workflow
- Smart branch detection (main/master vs feature branches)
- Git branch and log comparison
- Automatic branch creation when on main/master
- Intelligent PR creation for feature branches
"""

import os
import subprocess
import json
from typing import Optional, List, Dict, Tuple

try:
    from github import Github
    HAS_PYGITHUB = True
except ImportError:
    HAS_PYGITHUB = False
    print("⚠️  PyGithub not installed. Install with: pip install PyGithub")


class GitHubPRCreator:
    """Create GitHub pull requests programmatically with intelligent branching"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize with GitHub token
        
        Args:
            token: GitHub personal access token. If None, uses gh CLI.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.use_cli = not HAS_PYGITHUB or not self.token
        
        if self.token and HAS_PYGITHUB:
            self.github = Github(self.token)
        
        # Cache for git information
        self._main_branch = None
    
    def get_main_branch(self) -> str:
        """
        Detect main branch (main or master)
        
        Returns:
            String: 'main' or 'master'
        """
        if self._main_branch:
            return self._main_branch
        
        # Check remote branches
        try:
            result = subprocess.run(
                ['git', 'branch', '-r'],
                capture_output=True,
                text=True,
                check=True
            )
            branches = result.stdout.strip().split('\n')
            
            for branch in branches:
                branch = branch.strip()
                if 'origin/main' in branch:
                    self._main_branch = 'main'
                    return 'main'
                elif 'origin/master' in branch:
                    self._main_branch = 'master'
                    return 'master'
        except subprocess.CalledProcessError:
            pass
        
        # Default to main
        self._main_branch = 'main'
        return 'main'
    
    def is_main_branch(self, branch_name: str) -> bool:
        """
        Check if branch is the main/master branch
        
        Args:
            branch_name: Name to check
        
        Returns:
            True if branch is main or master
        """
        return branch_name in ['main', 'master']
    
    def get_all_branches(self) -> Dict[str, List[str]]:
        """
        Get all local and remote branches
        
        Returns:
            Dictionary with 'local' and 'remote' branch lists
        """
        try:
            # Get local branches
            local_result = subprocess.run(
                ['git', 'branch'],
                capture_output=True,
                text=True,
                check=True
            )
            local_branches = [b.strip().lstrip('* ') for b in local_result.stdout.strip().split('\n') if b.strip()]
            
            # Get remote branches
            remote_result = subprocess.run(
                ['git', 'branch', '-r'],
                capture_output=True,
                text=True,
                check=True
            )
            remote_branches = [b.strip().lstrip('* ') for b in remote_result.stdout.strip().split('\n') if b.strip()]
            
            return {
                'local': local_branches,
                'remote': remote_branches
            }
        except subprocess.CalledProcessError as e:
            return {'local': [], 'remote': []}
    
    def compare_branches(self, branch1: str, branch2: str) -> Dict:
        """
        Compare two branches, showing commits ahead/behind
        
        Args:
            branch1: First branch to compare
            branch2: Second branch to compare
        
        Returns:
            Dictionary with comparison results
        """
        try:
            # Commits in branch1 but not in branch2
            ahead_result = subprocess.run(
                ['git', 'log', f'{branch2}..{branch1}', '--oneline'],
                capture_output=True,
                text=True,
                check=True
            )
            ahead_commits = ahead_result.stdout.strip().split('\n') if ahead_result.stdout.strip() else []
            
            # Commits in branch2 but not in branch1
            behind_result = subprocess.run(
                ['git', 'log', f'{branch1}..{branch2}', '--oneline'],
                capture_output=True,
                text=True,
                check=True
            )
            behind_commits = behind_result.stdout.strip().split('\n') if behind_result.stdout.strip() else []
            
            return {
                'branch1': branch1,
                'branch2': branch2,
                'ahead': len([c for c in ahead_commits if c]),
                'ahead_commits': [c for c in ahead_commits if c],
                'behind': len([c for c in behind_commits if c]),
                'behind_commits': [c for c in behind_commits if c]
            }
        except subprocess.CalledProcessError as e:
            return {
                'error': str(e),
                'message': f'Could not compare branches {branch1} and {branch2}'
            }
    
    def compare_logs(self, branch1: str, branch2: str, num_commits: int = 10) -> Dict:
        """
        Compare commit history between two branches
        
        Args:
            branch1: First branch
            branch2: Second branch
            num_commits: Number of recent commits to show
        
        Returns:
            Dictionary with commit history
        """
        try:
            # Get commits from branch1
            log1_result = subprocess.run(
                ['git', 'log', f'{branch1}', f'--oneline', f'-{num_commits}'],
                capture_output=True,
                text=True,
                check=True
            )
            commits1 = [c.strip() for c in log1_result.stdout.strip().split('\n') if c.strip()]
            
            # Get commits from branch2
            log2_result = subprocess.run(
                ['git', 'log', f'{branch2}', f'--oneline', f'-{num_commits}'],
                capture_output=True,
                text=True,
                check=True
            )
            commits2 = [c.strip() for c in log2_result.stdout.strip().split('\n') if c.strip()]
            
            return {
                'branch1': branch1,
                'branch2': branch2,
                f'{branch1}_commits': commits1,
                f'{branch2}_commits': commits2
            }
        except subprocess.CalledProcessError as e:
            return {
                'error': str(e),
                'message': f'Could not get log for branches {branch1} and {branch2}'
            }
    
    def display_branch_comparison(self, comparison: Dict) -> None:
        """Display branch comparison in formatted output"""
        if 'error' in comparison:
            print(f"⚠️  {comparison.get('message', 'Unknown error')}")
            return
        
        print(f"\n📊 Branch Comparison: {comparison['branch1']} → {comparison['branch2']}")
        print("=" * 70)
        
        if comparison['ahead'] > 0:
            print(f"\n🚀 {comparison['branch1']} is {comparison['ahead']} commit(s) ahead:")
            for commit in comparison['ahead_commits'][:5]:  # Show first 5
                print(f"   • {commit}")
            if len(comparison['ahead_commits']) > 5:
                print(f"   ... and {len(comparison['ahead_commits']) - 5} more")
        
        if comparison['behind'] > 0:
            print(f"\n⏮️  {comparison['branch1']} is {comparison['behind']} commit(s) behind:")
            for commit in comparison['behind_commits'][:5]:  # Show first 5
                print(f"   • {commit}")
            if len(comparison['behind_commits']) > 5:
                print(f"   ... and {len(comparison['behind_commits']) - 5} more")
        
        if comparison['ahead'] == 0 and comparison['behind'] == 0:
            print("\n✅ Branches are identical")
        
        print()
    
    def create_new_branch(self, branch_name: str, base_branch: Optional[str] = None) -> Dict:
        """
        Create a new branch and push it
        
        Args:
            branch_name: Name for new branch
            base_branch: Branch to create from (default: current branch)
        
        Returns:
            Result dictionary
        """
        try:
            if base_branch:
                subprocess.run(
                    ['git', 'checkout', base_branch],
                    capture_output=True,
                    check=True
                )
            
            # Create new branch
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                capture_output=True,
                check=True
            )
            
            # Push to remote
            subprocess.run(
                ['git', 'push', '-u', 'origin', branch_name],
                capture_output=True,
                check=True
            )
            
            return {
                'success': True,
                'branch': branch_name,
                'message': f'✅ Branch "{branch_name}" created and pushed'
            }
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Failed to create branch "{branch_name}"'
            }
        """Get current git branch name"""
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    
    def get_repo_info(self) -> tuple[str, str]:
        """Get owner and repo name from git remote"""
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True
        )
        url = result.stdout.strip()
        
        # Handle both HTTPS and SSH URLs
        if 'github.com' in url:
            if url.startswith('git@'):
                parts = url.split(':')[1].replace('.git', '').split('/')
            else:
                parts = url.replace('https://github.com/', '').replace('.git', '').split('/')
            
            return parts[0], parts[1]
        
        raise ValueError(f"Could not parse repository from: {url}")
    
    def create_pr_with_cli(
        self,
        title: str,
        body: str,
        head: str,
        base: str = 'main'
    ) -> dict:
        """
        Create PR using GitHub CLI
        
        Args:
            title: PR title
            body: PR description
            head: Feature branch name
            base: Base branch (default: main)
        
        Returns:
            PR creation result
        """
        cmd = [
            'gh', 'pr', 'create',
            '--title', title,
            '--body', body,
            '--head', head,
            '--base', base
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': result.stderr,
                'message': 'Failed to create PR with GitHub CLI'
            }
        
        return {
            'success': True,
            'url': result.stdout.strip(),
            'message': 'PR created successfully!'
        }
    
    def create_pr_with_api(
        self,
        title: str,
        body: str,
        head: str,
        base: str = 'main'
    ) -> dict:
        """
        Create PR using PyGithub
        
        Args:
            title: PR title
            body: PR description
            head: Feature branch name
            base: Base branch (default: main)
        
        Returns:
            PR creation result
        """
        if not HAS_PYGITHUB:
            return {
                'success': False,
                'error': 'PyGithub not installed',
                'message': 'Install with: pip install PyGithub'
            }
        
        try:
            owner, repo_name = self.get_repo_info()
            repo = self.github.get_user(owner).get_repo(repo_name)
            
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head,
                base=base
            )
            
            return {
                'success': True,
                'url': pr.html_url,
                'number': pr.number,
                'message': f'PR #{pr.number} created successfully!'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create PR with PyGithub'
            }
    
    def create_pr(
        self,
        title: str,
        body: str,
        head: Optional[str] = None,
        base: str = 'main'
    ) -> dict:
        """
        Create a GitHub pull request
        
        Args:
            title: PR title
            body: PR description
            head: Feature branch (default: current branch)
            base: Base branch (default: main)
        
        Returns:
            Result dictionary with success status and URL
        """
        # Use current branch if not specified
        if not head:
            head = self.get_current_branch()
        
        print(f"📝 Creating PR:")
        print(f"   Title: {title}")
        print(f"   Branch: {head} → {base}")
        print()
        
        # Try CLI first, then API
        if self.use_cli:
            print("🔧 Using GitHub CLI...")
            return self.create_pr_with_cli(title, body, head, base)
        else:
            print("🔧 Using PyGithub API...")
            return self.create_pr_with_api(title, body, head, base)


def interactive_pr_creation():
    """Interactive PR creation workflow with intelligent branching"""
    print("\n" + "=" * 70)
    print("🚀 GitHub PR Creator - Smart Workflow")
    print("=" * 70)
    
    creator = GitHubPRCreator()
    
    # Get current branch
    try:
        current_branch = creator.get_current_branch()
        print(f"\n📌 Current branch: {current_branch}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Detect main branch
    main_branch = creator.get_main_branch()
    print(f"📌 Main branch detected: {main_branch}")
    
    print("\n" + "-" * 70)
    
    # Check if on main/master
    if creator.is_main_branch(current_branch):
        print(f"\n🎯 You are on the {current_branch} branch!")
        print("💡 For production safety, let's create a feature branch instead.\n")
        
        # Get new branch name
        branch_name = input("📝 Enter new branch name (e.g., feature/my-feature): ").strip()
        if not branch_name:
            print("❌ Branch name is required!")
            return
        
        # Create and push new branch
        print(f"\n⏳ Creating branch '{branch_name}'...")
        result = creator.create_new_branch(branch_name, base_branch=main_branch)
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"\n💡 Now make your changes and commit them.")
            print(f"   Then run this tool again to create a PR.\n")
        else:
            print(f"❌ {result['message']}")
            print(f"   Error: {result.get('error')}")
        
        return
    
    # We're on a feature branch - proceed with PR creation
    print(f"\n🔀 Creating PR from {current_branch} → {main_branch}")
    
    # Display branch comparison
    print("\n📊 Getting branch information...")
    comparison = creator.compare_branches(current_branch, main_branch)
    creator.display_branch_comparison(comparison)
    
    # Get PR details
    print("-" * 70)
    title = input("\n📝 PR Title: ").strip()
    if not title:
        print("❌ Title is required!")
        return
    
    print("\n📄 PR Description (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines and lines[-1] == "":
                lines.pop()
                break
        lines.append(line)
    
    body = "\n".join(lines) if lines else "No description provided"
    
    # Add comparison info to body
    if comparison.get('ahead'):
        body += f"\n\n## Changes\n- {comparison['ahead']} commit(s) ahead of {main_branch}"
    
    print()
    
    # Create PR
    print("⏳ Creating PR...")
    result = creator.create_pr(
        title=title,
        body=body,
        head=current_branch,
        base=main_branch
    )
    
    # Display result
    print()
    if result['success']:
        print("✅ " + result['message'])
        print(f"🔗 PR URL: {result['url']}")
    else:
        print("❌ " + result['message'])
        print(f"📋 Error: {result.get('error', 'Unknown error')}")


def smart_pr_workflow():
    """
    Smart PR workflow that automatically:
    1. Compares branches
    2. Compares logs
    3. Creates branch if on main/master
    4. Creates PR if on feature branch
    
    This is the main entry point for the skill.
    """
    interactive_pr_creation()


if __name__ == '__main__':
    smart_pr_workflow()
