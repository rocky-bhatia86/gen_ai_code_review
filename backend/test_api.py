#!/usr/bin/env python3
"""
API Testing Suite for AI Code Review System
Uses the Python API client to test all endpoints
"""

import time
import tempfile
from pathlib import Path
from services.api_client import CodeReviewAPIClient

# Test data
SAMPLE_CODES = {
    "python": '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
''',
    
    "javascript": '''
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5));
''',
    
    "problematic": '''
def bad_function(x):
    password = "hardcoded123"
    if x == password:
        return True
    return False
'''
}

def test_health_check(client: CodeReviewAPIClient) -> bool:
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    try:
        result = client.health_check()
        print(f"   ✅ Health check passed: {result.get('message', 'OK')}")
        return True
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False

def test_status(client: CodeReviewAPIClient) -> bool:
    """Test the status endpoint"""
    print("📊 Testing status endpoint...")
    try:
        status = client.get_status()
        print(f"   ✅ Status retrieved")
        print(f"      OpenAI: {'Ready' if status.get('openai_configured') else 'Mock Mode'}")
        print(f"      GitHub: {'Connected' if status.get('github_configured') else 'Not Configured'}")
        return True
    except Exception as e:
        print(f"   ❌ Status check failed: {e}")
        return False

def test_code_review(client: CodeReviewAPIClient) -> bool:
    """Test code review endpoint"""
    print("📝 Testing code review...")
    success_count = 0
    
    for lang, code in SAMPLE_CODES.items():
        try:
            print(f"   Testing {lang} code...")
            result = client.review_code(code)
            
            if 'review' in result and result['review']:
                print(f"   ✅ {lang.capitalize()} review successful")
                success_count += 1
            else:
                print(f"   ⚠️  {lang.capitalize()} review returned empty")
                
        except Exception as e:
            print(f"   ❌ {lang.capitalize()} review failed: {e}")
    
    return success_count > 0

def test_file_review(client: CodeReviewAPIClient) -> bool:
    """Test file upload review endpoint"""
    print("📁 Testing file review...")
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(SAMPLE_CODES['python'])
            temp_file = f.name
        
        try:
            result = client.review_file(temp_file)
            
            if 'review' in result and result['review']:
                print("   ✅ File review successful")
                return True
            else:
                print("   ⚠️  File review returned empty")
                return False
                
        finally:
            # Clean up temp file
            Path(temp_file).unlink(missing_ok=True)
            
    except Exception as e:
        print(f"   ❌ File review failed: {e}")
        return False

def test_pr_review(client: CodeReviewAPIClient) -> bool:
    """Test PR review endpoint (with mock data)"""
    print("🔗 Testing PR review...")
    
    # Use a public GitHub PR URL for testing
    test_pr_url = "https://github.com/octocat/Hello-World/pull/1"
    
    try:
        # Test with diff content provided (so it doesn't need GitHub token)
        sample_diff = '''
diff --git a/README.md b/README.md
index 1234567..abcdefg 100644
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
 # Hello World
 
 This is a test repository.
+Added a new line for testing.
'''
        
        result = client.review_pr(test_pr_url, sample_diff)
        
        if 'review' in result and result['review']:
            print("   ✅ PR review successful")
            return True
        else:
            print("   ⚠️  PR review returned empty")
            return False
            
    except Exception as e:
        print(f"   ❌ PR review failed: {e}")
        return False

def run_performance_test(client: CodeReviewAPIClient):
    """Run simple performance test"""
    print("⚡ Running performance test...")
    
    try:
        start_time = time.time()
        result = client.review_code("print('Hello, World!')")
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"   ⏱️  Review completed in {duration:.2f} seconds")
        
        if duration < 10:  # Reasonable threshold
            print("   ✅ Performance acceptable")
        else:
            print("   ⚠️  Review took longer than expected")
            
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")

def main():
    """Run all API tests"""
    print("🧪 AI Code Review System - API Test Suite")
    print("=" * 50)
    
    client = CodeReviewAPIClient()
    
    # Track test results
    test_results = []
    
    # Run tests
    test_results.append(("Health Check", test_health_check(client)))
    test_results.append(("Status", test_status(client)))
    test_results.append(("Code Review", test_code_review(client)))
    test_results.append(("File Review", test_file_review(client)))
    test_results.append(("PR Review", test_pr_review(client)))
    
    # Performance test (non-critical)
    run_performance_test(client)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    exit(main()) 