#!/usr/bin/env python3
"""
GitHub PR Creator Script
Automated pull request creation with AI-guided workflow
"""

import os
import subprocess
import json
from typing import Optional

try:
    from github import Github
    HAS_PYGITHUB = True
except ImportError:
    HAS_PYGITHUB = False
    print("⚠️  PyGithub not installed. Install with: pip install PyGithub")


class GitHubPRCreator:
    """Create GitHub pull requests programmatically"""
    
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
    
    def get_current_branch(self) -> str:
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
    """Interactive PR creation workflow"""
    print("=" * 60)
    print("🚀 GitHub PR Creator")
    print("=" * 60)
    print()
    
    creator = GitHubPRCreator()
    
    # Get current branch
    try:
        current_branch = creator.get_current_branch()
        print(f"📌 Current branch: {current_branch}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print()
    
    # Get PR details
    title = input("📝 PR Title: ").strip()
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
    
    base = input("\n🔀 Base branch (default: main): ").strip() or "main"
    
    print()
    
    # Create PR
    result = creator.create_pr(
        title=title,
        body=body,
        head=current_branch,
        base=base
    )
    
    # Display result
    print()
    if result['success']:
        print("✅ " + result['message'])
        print(f"🔗 PR URL: {result['url']}")
    else:
        print("❌ " + result['message'])
        print(f"📋 Error: {result.get('error', 'Unknown error')}")


if __name__ == '__main__':
    interactive_pr_creation()
