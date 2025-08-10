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
        """Verify GitHub webhook signature for security"""
        if not self.webhook_secret:
            return True  # Skip verification if no secret configured
        
        expected_signature = "sha256=" + hmac.new(
            self.webhook_secret.encode(),
            payload_body,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature_header)
    
    def get_pr_diff(self, repo_owner: str, repo_name: str, pr_number: int) -> Optional[str]:
        """Get the diff content of a pull request"""
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
        """Get list of files changed in a pull request"""
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
    
    def post_pr_review(self, repo_owner: str, repo_name: str, pr_number: int,
                      review_body: str, comments: List[ReviewComment] = None) -> bool:
        """Post a review with inline comments to a pull request"""
        if not self.token:
            return False
            
        url = f"{self.base_url}/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/reviews"
        
        data = {
            "body": review_body,
            "event": "COMMENT",
            "comments": [comment.dict() for comment in (comments or [])]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return True
            
        except requests.RequestException as e:
            print(f"Error posting PR review: {e}")
            return False
    
    def post_pr_comment(self, repo_owner: str, repo_name: str, pr_number: int, 
                       comment_body: str) -> bool:
        """Post a general comment to a pull request"""
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
    
    def parse_webhook_pr(self, webhook_data: Dict) -> Optional[Dict]:
        """Parse GitHub webhook data for pull request events"""
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

    def create_inline_comments(self, ai_review_result: Dict, pr_files: List[Dict]) -> List[ReviewComment]:
        """
        Create inline comments from AI review results
        Maps AI suggestions to specific file lines for GitHub PR review
        """
        comments = []
        line_comments = ai_review_result.get("line_comments", [])
        
        # Create a mapping of filenames for quick lookup
        file_map = {f["filename"]: f for f in pr_files}
        
        for comment_data in line_comments:
            file_path = comment_data.get("file")
            line_number = comment_data.get("line")
            
            if file_path in file_map and line_number:
                # Calculate GitHub diff position
                position = self._calculate_position(file_map[file_path], line_number)
                
                if position > 0:  # Only add comment if we found a valid position
                    # Include code snippet if available
                    code_snippet = comment_data.get("code_snippet", "")
                    message = comment_data.get("message", "")
                    
                    if code_snippet:
                        body = f"**{comment_data.get('severity', 'SUGGESTION')}**: {message}\n\n```python\n{code_snippet}\n```"
                    else:
                        body = f"**{comment_data.get('severity', 'SUGGESTION')}**: {message}"
                    
                    comment = ReviewComment(
                        body=body,
                        path=file_path,
                        position=position
                    )
                    comments.append(comment)
        
        return comments
    
    def _calculate_position(self, file_data: Dict, target_line: int) -> int:
        """
        Calculate GitHub diff position for a given NEW file line number
        Maps NEW file line numbers to GitHub diff positions
        """
        if "patch" not in file_data:
            return 0  # Return 0 for invalid position
            
        patch_lines = file_data["patch"].split('\n')
        position = 0
        current_new_line = 0
        
        for line in patch_lines:
            position += 1
            
            if line.startswith('@@'):
                # Parse hunk header: @@ -old_start,old_count +new_start,new_count @@
                import re
                match = re.search(r'@@\s*-\d+(?:,\d+)?\s*\+(\d+)(?:,\d+)?\s*@@', line)
                if match:
                    current_new_line = int(match.group(1)) - 1  # Start before the first line
                else:
                    continue
                    
            elif line.startswith('+'):
                # This is an added line - increment new line counter first
                current_new_line += 1
                if current_new_line == target_line:
                    return position
                    
            elif line.startswith('-'):
                # This is a deleted line, don't increment new line counter
                pass
                
            elif line.startswith(' '):
                # This is a context line (unchanged) - increment new line counter
                current_new_line += 1
        
        return 0  # Return 0 if line not found

# Global service instance  
github_service = GitHubService() 