"""
AI Code Review Service
Handles OpenAI integration and review logic
"""
from typing import Optional
from config import settings

# Optional OpenAI import
try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
except ImportError:
    client = None

class ReviewService:
    """Service for handling code reviews using AI"""
    
    def __init__(self):
        self.client = client
        self.model = settings.OPENAI_MODEL
    
    def review_code(self, code: str, context: str = "general code") -> str:
        """
        Review code using OpenAI or return mock review
        
        Args:
            code: The code to review
            context: Context about the code (e.g., "Python function", "Git diff")
            
        Returns:
            Review feedback as string
        """
        if not code.strip():
            return "No code provided for review."
        
        if self.client and settings.openai_enabled:
            return self._ai_review(code, context)
        else:
            return self._mock_review(code, context)
    
    def _ai_review(self, code: str, context: str) -> str:
        """Get AI review from OpenAI"""
        try:
            system_prompt = """You are a senior software engineer reviewing code. 
            Provide constructive feedback focusing on:
            - Code quality and best practices
            - Potential bugs or security issues  
            - Performance improvements
            - Readability and maintainability
            Keep feedback clear and actionable."""
            
            user_prompt = f"Review this {context}:\n\n{code}"
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3  # Lower temperature for more consistent reviews
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error getting AI review: {str(e)}\n\nFalling back to mock review:\n{self._mock_review(code, context)}"
    
    def _mock_review(self, code: str, context: str) -> str:
        """Generate mock review for testing/offline mode"""
        mock_reviews = {
            "general code": "✅ Mock Review: Code structure looks good. Consider adding error handling and improving variable names.",
            "Git diff": "🔍 Mock PR Review: Changes detected. Ensure they follow project standards and include proper tests.",
            "file upload": "📁 Mock File Review: File processed successfully. Check for proper imports and documentation."
        }
        
        base_review = mock_reviews.get(context, mock_reviews["general code"])
        
        # Add some basic analysis
        lines = code.count('\n') + 1
        has_functions = 'def ' in code or 'function ' in code
        has_classes = 'class ' in code
        
        analysis = f"\n\n📊 Basic Analysis:\n- Lines of code: {lines}\n- Contains functions: {has_functions}\n- Contains classes: {has_classes}"
        
        return base_review + analysis

# Global service instance
review_service = ReviewService() 