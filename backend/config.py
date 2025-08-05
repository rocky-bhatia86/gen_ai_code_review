import os
from typing import Optional

class Settings:
    """Application configuration settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # GitHub Configuration  
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_WEBHOOK_SECRET: Optional[str] = os.getenv("GITHUB_WEBHOOK_SECRET")
    
    # Server Configuration
    HOST: str = "localhost"
    PORT: int = 8000
    
    @property
    def openai_enabled(self) -> bool:
        """Check if OpenAI is available and configured"""
        return bool(self.OPENAI_API_KEY)
    
    @property  
    def github_enabled(self) -> bool:
        """Check if GitHub integration is configured"""
        return bool(self.GITHUB_TOKEN)

# Global settings instance
settings = Settings() 