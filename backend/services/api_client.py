"""
Python API Client for AI Code Review System
Equivalent to frontend/src/services/api.js but in Python

This can be used for:
- Backend testing
- Automation scripts  
- Integration with other Python applications
- CLI tools
"""

import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path

class CodeReviewAPIClient:
    """Python client for the AI Code Review System API"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except:
                error_detail = str(e)
            
            raise Exception(f"API request failed: {error_detail}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def review_code(self, code: str) -> Dict[str, str]:
        """
        Review code by sending it as text
        
        Args:
            code: The code string to review
            
        Returns:
            Dictionary with 'review' and 'status' keys
        """
        data = {"code": code}
        return self._make_request("POST", "/review", json=data)
    
    def review_file(self, file_path: str) -> Dict[str, str]:
        """
        Review code from a file
        
        Args:
            file_path: Path to the code file
            
        Returns:
            Dictionary with 'review' and 'status' keys
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            raise Exception("File must be a text file (UTF-8 encoded)")
        
        # Prepare multipart form data
        files = {
            'file': (file_path.name, content, 'text/plain')
        }
        
        # Remove Content-Type header for multipart upload
        headers = {k: v for k, v in self.session.headers.items() 
                  if k.lower() != 'content-type'}
        
        url = f"{self.base_url}/review/file"
        response = requests.post(url, files=files, headers=headers)
        
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except:
                error_detail = str(e)
            
            raise Exception(f"File review failed: {error_detail}")
    
    def review_pr(self, pr_url: str, diff_content: str = "") -> Dict[str, str]:
        """
        Review a GitHub PR by URL
        
        Args:
            pr_url: GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)
            diff_content: Optional diff content (if empty, will fetch from GitHub)
            
        Returns:
            Dictionary with 'review' and 'status' keys
        """
        data = {
            "pr_url": pr_url,
            "diff_content": diff_content
        }
        return self._make_request("POST", "/review/pr", json=data)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get system status
        
        Returns:
            Dictionary with system configuration status
        """
        return self._make_request("GET", "/status")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API is running
        
        Returns:
            Dictionary with health status
        """
        return self._make_request("GET", "/")

# Example usage and testing functions
def main():
    """Example usage of the API client"""
    client = CodeReviewAPIClient()
    
    print("🤖 AI Code Review System - Python API Client")
    print("=" * 50)
    
    try:
        # Health check
        print("📊 Checking system status...")
        status = client.get_status()
        print(f"   OpenAI: {'✅ Ready' if status.get('openai_configured') else '🟡 Mock Mode'}")
        print(f"   GitHub: {'✅ Connected' if status.get('github_configured') else '⚫ Not Configured'}")
        print()
        
        # Example code review
        sample_code = '''
def calculate_factorial(n):
    if n < 0:
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
'''
        
        print("📝 Reviewing sample code...")
        review_result = client.review_code(sample_code)
        print("Review Result:")
        print("-" * 30)
        print(review_result['review'])
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 