import os
from typing import Optional

class Settings:
    """Application configuration settings"""
    
    # OpenAI Configuration (Regular OpenAI)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    OPENAI_API_TYPE: str = os.getenv("OPENAI_API_TYPE", "openai")  # "openai" or "azure"
    OPENAI_API_VERSION: str = os.getenv("OPENAI_API_VERSION", "2024-02-01")
    
    # GitHub Configuration  
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_WEBHOOK_SECRET: Optional[str] = os.getenv("GITHUB_WEBHOOK_SECRET")
    
    # Server Configuration
    HOST: str = "localhost"
    PORT: int = 8000
    
    @property
    def openai_enabled(self) -> bool:
        """Check if OpenAI (regular or Azure) is available and configured"""
        if self.OPENAI_API_TYPE == "azure":
            return bool(self.AZURE_OPENAI_API_KEY and self.AZURE_OPENAI_ENDPOINT)
        else:
            return bool(self.OPENAI_API_KEY)
    
    @property
    def is_azure_openai(self) -> bool:
        """Check if using Azure OpenAI"""
        return self.OPENAI_API_TYPE == "azure"
    
    @property  
    def github_enabled(self) -> bool:
        """Check if GitHub integration is configured"""
        return bool(self.GITHUB_TOKEN)

# Global settings instance
settings = Settings() 