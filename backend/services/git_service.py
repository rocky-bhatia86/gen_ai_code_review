"""
GitHub Integration Service
Handles GitHub API calls, webhook processing, and PR reviews
"""
import requests
import json
import hashlib
import hmac
from typing import Dict, List, Optional
from config import settings
from models import ReviewComment

class GitHubService:
    """Service for GitHub API integration"""
    
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.webhook_secret = settings.GITHUB_WEBHOOK_SECRET
        self.base_url = "https://api.github.com"
        
        # Headers for GitHub API requests
        self.headers = {
            "Authorization": f"token {self.token}" if self.token else "",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def verify_webhook_signature(self, payload_body: bytes, signature_header: str) -> bool:
        """
        Verify GitHub webhook signature for security
        
        Args:
            payload_body: Raw webhook payload
            signature_header: X-Hub-Signature-256 header from GitHub
            
        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            return True  # Skip verification if no secret configured
        
        expected_signature = "sha256=" + hmac.new(
            self.webhook_secret.encode(),
            payload_body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature_header)
    
    def get_pr_diff(self, repo_owner: str, repo_name: str, pr_number: int) -> Optional[str]:
        """
        Get the diff content of a pull request
        
        Args:
            repo_owner: GitHub repository owner
            repo_name: GitHub repository name  
            pr_number: Pull request number
            
        Returns:
            Diff content as string or None if error
        """
        if not self.token:
            return None
            
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
        
        try:
            # Get PR diff in unified format
            headers = self.headers.copy()
            headers["Accept"] = "application/vnd.github.v3.diff"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.text
            
        except requests.RequestException as e:
            print(f"Error fetching PR diff: {e}")
            return None
    
    def get_pr_files(self, repo_owner: str, repo_name: str, pr_number: int) -> List[Dict]:
        """
        Get list of files changed in a pull request
        
        Returns:
            List of file objects with filename, status, changes, etc.
        """
        if not self.token:
            return []
            
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            print(f"Error fetching PR files: {e}")
            return []
    
    def post_pr_comment(self, repo_owner: str, repo_name: str, pr_number: int, 
                       comment_body: str) -> bool:
        """
        Post a general comment to a pull request
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name
            pr_number: PR number
            comment_body: Comment text
            
        Returns:
            True if successful
        """
        if not self.token:
            return False
            
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        
        data = {"body": comment_body}
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
            
        except requests.RequestException as e:
            print(f"Error posting PR comment: {e}")
            return False
    
    def post_pr_review(self, repo_owner: str, repo_name: str, pr_number: int,
                      review_body: str, comments: List[ReviewComment] = None) -> bool:
        """
        Post a review with inline comments to a pull request
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name  
            pr_number: PR number
            review_body: Overall review summary
            comments: List of inline comments
            
        Returns:
            True if successful
        """
        if not self.token:
            return False
            
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/reviews"
        
        data = {
            "body": review_body,
            "event": "COMMENT",  # COMMENT, APPROVE, or REQUEST_CHANGES
            "comments": [comment.dict() for comment in (comments or [])]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
            
        except requests.RequestException as e:
            print(f"Error posting PR review: {e}")
            return False
    
    def parse_webhook_pr(self, webhook_data: Dict) -> Optional[Dict]:
        """
        Parse GitHub webhook data for pull request events
        
        Returns:
            Dictionary with PR info or None if not a PR event
        """
        if "pull_request" not in webhook_data:
            return None
            
        pr = webhook_data["pull_request"]
        repo = webhook_data["repository"]
        
        return {
            "action": webhook_data.get("action"),
            "pr_number": pr["number"],
            "pr_title": pr["title"],
            "pr_url": pr["html_url"],
            "repo_owner": repo["owner"]["login"],
            "repo_name": repo["name"],
            "repo_full_name": repo["full_name"],
            "author": pr["user"]["login"],
            "branch": pr["head"]["ref"],
            "base_branch": pr["base"]["ref"]
        }

# Global service instance  
github_service = GitHubService() 