#!/usr/bin/env python3
"""
Command Line Interface for AI Code Review System
Uses the Python API client to provide CLI access to code reviews
"""

import argparse
import sys
from pathlib import Path
from services.api_client import CodeReviewAPIClient

def review_code_from_stdin(client: CodeReviewAPIClient):
    """Review code from standard input"""
    print("📝 Enter your code (Ctrl+D or Ctrl+Z when finished):")
    try:
        code = sys.stdin.read()
        if not code.strip():
            print("❌ No code provided")
            return
        
        print("\n🤖 Reviewing code...")
        result = client.review_code(code)
        print("\n" + "="*50)
        print("REVIEW RESULTS")
        print("="*50)
        print(result['review'])
        
    except KeyboardInterrupt:
        print("\n❌ Review cancelled")
    except Exception as e:
        print(f"❌ Error: {e}")

def review_file(client: CodeReviewAPIClient, file_path: str):
    """Review code from a file"""
    try:
        print(f"📁 Reviewing file: {file_path}")
        result = client.review_file(file_path)
        print("\n" + "="*50)
        print("REVIEW RESULTS")
        print("="*50)
        print(result['review'])
        
    except Exception as e:
        print(f"❌ Error: {e}")

def review_pr(client: CodeReviewAPIClient, pr_url: str):
    """Review a GitHub PR"""
    try:
        print(f"🔗 Reviewing PR: {pr_url}")
        result = client.review_pr(pr_url)
        print("\n" + "="*50)
        print("REVIEW RESULTS")
        print("="*50)
        print(result['review'])
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_status(client: CodeReviewAPIClient):
    """Show system status"""
    try:
        print("📊 System Status")
        print("-" * 20)
        
        status = client.get_status()
        health = client.health_check()
        
        print(f"🏥 Service: {health.get('message', 'Unknown')}")
        print(f"🤖 OpenAI: {'✅ Ready' if status.get('openai_configured') else '🟡 Mock Mode'}")
        print(f"🔗 GitHub: {'✅ Connected' if status.get('github_configured') else '⚫ Not Configured'}")
        print(f"🔧 Model: {status.get('openai_model', 'N/A')}")
        print(f"🖥️  Server: {status.get('server', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="AI Code Review System - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --status                           # Show system status
  %(prog)s --stdin                            # Review code from stdin
  %(prog)s --file app.py                      # Review a specific file
  %(prog)s --pr https://github.com/user/repo/pull/123  # Review a PR
  
  echo "print('hello')" | %(prog)s --stdin    # Pipe code for review
        """
    )
    
    parser.add_argument(
        "--server", 
        default="http://localhost:8001",
        help="API server URL (default: http://localhost:8001)"
    )
    
    # Action group - only one action allowed
    action_group = parser.add_mutually_exclusive_group(required=True)
    
    action_group.add_argument(
        "--status", 
        action="store_true",
        help="Show system status"
    )
    
    action_group.add_argument(
        "--stdin", 
        action="store_true",
        help="Review code from standard input"
    )
    
    action_group.add_argument(
        "--file", 
        metavar="PATH",
        help="Review code from file"
    )
    
    action_group.add_argument(
        "--pr", 
        metavar="URL",
        help="Review GitHub pull request by URL"
    )
    
    args = parser.parse_args()
    
    # Create API client
    client = CodeReviewAPIClient(args.server)
    
    # Execute the requested action
    try:
        if args.status:
            show_status(client)
        elif args.stdin:
            review_code_from_stdin(client)
        elif args.file:
            review_file(client, args.file)
        elif args.pr:
            review_pr(client, args.pr)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 