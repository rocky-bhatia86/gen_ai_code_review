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
        Convert AI review results to GitHub inline comments
        
        Args:
            ai_review_result: Dict with 'line_comments' array
            pr_files: List of PR file data from GitHub API
            
        Returns:
            List of ReviewComment objects for GitHub API
        """
        comments = []
        line_comments = ai_review_result.get("line_comments", [])
        
        file_map = {f["filename"]: f for f in pr_files}
        
        for comment_data in line_comments:
            file_path = comment_data.get("file")
            line_number = comment_data.get("line")
            
            if not file_path or not line_number:
                continue
                
            if file_path not in file_map:
                continue

            # Calculate GitHub diff position
            position = self._calculate_position(file_map[file_path], line_number)
            
            if position <= 0:
                continue

            # Handle both old and new AI response formats
            message = self._format_comment_message(comment_data)
            
            if not message:
                continue
            
            comment = ReviewComment(
                body=message,
                path=file_path,
                position=position
            )
            comments.append(comment)
        return comments
    
    def _format_comment_message(self, comment_data: Dict) -> str:
        """
        Format comment message from AI response data.
        Handles both old format (single 'message' field) and new format (issue/impact/fix fields)
        """
        # New structured format with separate fields
        if "issue" in comment_data or "impact" in comment_data or "fix" in comment_data:
            severity = comment_data.get('severity', 'SUGGESTION')
            issue = comment_data.get('issue', '')
            impact = comment_data.get('impact', '')
            fix = comment_data.get('fix', '')
            code_snippet = comment_data.get('code_snippet', '')
            
            # Build structured message
            parts = []
            
            if issue:
                parts.append(f"**{severity}**: {issue}")
            
            if code_snippet:
                # Try to detect language from code snippet
                language = self._detect_language(code_snippet)
                parts.append(f"\n**Current code:**\n```{language}\n{code_snippet}\n```")
            
            if impact:
                parts.append(f"\n**Impact:** {impact}")
                
            if fix:
                parts.append(f"\n**Recommended fix:** {fix}")
            
            return "\n".join(parts) if parts else ""
        
        # Old format with single 'message' field
        elif "message" in comment_data:
            message = comment_data.get("message", "")
            severity = comment_data.get('severity', 'SUGGESTION')
            code_snippet = comment_data.get('code_snippet', '')
            
            if code_snippet and code_snippet not in message:
                language = self._detect_language(code_snippet)
                return f"**{severity}**: {message}\n\n```{language}\n{code_snippet}\n```"
            else:
                return f"**{severity}**: {message}"
        
        # Fallback: try to construct from any available fields
        else:
            severity = comment_data.get('severity', 'SUGGESTION')
            code_snippet = comment_data.get('code_snippet', '')
            
            if code_snippet:
                language = self._detect_language(code_snippet)
                return f"**{severity}**: Code review suggestion\n\n```{language}\n{code_snippet}\n```"
            
            return f"**{severity}**: Code review suggestion"
    
    def _detect_language(self, code_snippet: str) -> str:
        """Detect programming language from code snippet for syntax highlighting"""
        code_lower = code_snippet.lower()
        
        # Python indicators
        if any(keyword in code_lower for keyword in ['def ', 'import ', 'from ', 'print(', '__init__']):
            return 'python'
        
        # JavaScript/TypeScript indicators  
        elif any(keyword in code_lower for keyword in ['function ', 'const ', 'let ', 'var ', '=>', 'console.log']):
            return 'javascript'
            
        # Java indicators
        elif any(keyword in code_lower for keyword in ['public class', 'private ', 'public static', 'system.out']):
            return 'java'
            
        # C/C++ indicators
        elif any(keyword in code_lower for keyword in ['#include', 'int main', 'printf(', 'cout <<']):
            return 'cpp'
            
        # Go indicators
        elif any(keyword in code_lower for keyword in ['func ', 'package ', 'import (', 'fmt.print']):
            return 'go'
            
        # Default to generic code highlighting
        else:
            return 'text'

    def _calculate_position(self, file_data: Dict, target_line: int) -> int:
        """
        Calculate GitHub diff position for a given NEW file line number
        Maps NEW file line numbers to GitHub diff positions
        
        Args:
            file_data: GitHub file data with patch information
            target_line: NEW file line number to find
            
        Returns:
            GitHub diff position (1-based) or 0 if not found
        """
        if "patch" not in file_data:
            return 0
            
        patch_lines = file_data["patch"].split('\n')
        position = 0
        current_new_line = 0
        found_hunk = False
        
        for line in patch_lines:
            position += 1
            
            if line.startswith('@@'):
                # Parse hunk header: @@ -old_start,old_count +new_start,new_count @@
                import re
                match = re.search(r'@@\s*-\d+(?:,\d+)?\s*\+(\d+)(?:,\d+)?\s*@@', line)
                if match:
                    current_new_line = int(match.group(1)) - 1  # Start before the first line
                    found_hunk = True
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
