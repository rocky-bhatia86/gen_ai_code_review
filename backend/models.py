from pydantic import BaseModel
from typing import Optional, List

class CodeRequest(BaseModel):
    """Request model for code review"""
    code: str

class ReviewResponse(BaseModel):
    """Response model for code review results"""
    review: str
    status: str = "success"

class FileUploadRequest(BaseModel):
    """Request model for file upload review"""
    filename: str
    content: str
    file_type: Optional[str] = None

class GitHubWebhookEvent(BaseModel):
    """GitHub webhook event model"""
    action: str
    pull_request: dict
    repository: dict

class PRReviewRequest(BaseModel):
    """Request model for PR review"""
    pr_url: str
    diff_content: Optional[str] = None

class ReviewComment(BaseModel):
    """Model for review comments to post back to GitHub"""
    body: str
    path: str
    position: int  # Position in the diff (required by GitHub API)
    
    def dict(self):
        """Convert to dict format expected by GitHub API"""
        return {
            "body": self.body,
            "path": self.path,
            "position": self.position
        } 