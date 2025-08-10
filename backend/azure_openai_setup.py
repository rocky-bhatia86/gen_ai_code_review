"""
Azure OpenAI Setup and Testing Script
Run this to configure and test Azure OpenAI integration
"""

import os
import sys

def setup_azure_openai():
    """Set up Azure OpenAI environment variables"""
    
    # Set your Azure OpenAI credentials here or in environment variables
    os.environ["AZURE_OPENAI_API_KEY"] = "your_azure_openai_api_key_here"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource-name.openai.azure.com"
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "gpt-4o"
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2024-02-01"
    
    print("✅ Azure OpenAI environment variables configured")
    print("Configuration:")
    print(f"   - Endpoint: {os.environ['AZURE_OPENAI_ENDPOINT']}")
    print(f"   - Deployment: {os.environ['AZURE_OPENAI_DEPLOYMENT_NAME']}")
    print(f"   - API Version: {os.environ['OPENAI_API_VERSION']}")
    print(f"   - API Key: {'*' * 40}...{os.environ['AZURE_OPENAI_API_KEY'][-8:] if len(os.environ['AZURE_OPENAI_API_KEY']) > 8 else '*' * 8}")

def test_azure_openai_integration():
    """Test Azure OpenAI integration with the review service"""
    try:
        # Import the review service
        from services.review_service import review_service
        
        # Test code for review
        test_code = """
def test_function():
    password = "hardcoded_password"  # This should be flagged
    result = eval("2 + 2")  # This should be flagged as security issue
    return result
"""
        
        print("\n🧪 Testing Azure OpenAI integration...")
        print("Code to review:")
        print(test_code)
        
        # Test the review
        review = review_service.review_code(test_code, "test code")
        
        print("\n📝 AI Review Result:")
        print(review)
        
        # Check if the review contains expected security warnings
        if "password" in review.lower() or "security" in review.lower() or "eval" in review.lower():
            print("\n✅ Azure OpenAI integration is working correctly!")
            print("   The AI detected security issues as expected.")
            return True
        else:
            print("\n⚠️  Azure OpenAI responded but may not be detecting issues properly.")
            return False
            
    except Exception as e:
        print(f"\n❌ Azure OpenAI integration test failed: {e}")
        print("Please check your configuration and try again.")
        return False

def main():
    """Main setup and test function"""
    print("🚀 Azure OpenAI Setup and Test")
    print("=" * 50)
    
    # Setup environment
    setup_azure_openai()
    
    # Test integration
    success = test_azure_openai_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup complete! Azure OpenAI is ready to use.")
    else:
        print("❌ Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    main() 