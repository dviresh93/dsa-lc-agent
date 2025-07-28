import subprocess
import json
import os
import tempfile
from typing import Dict, Any, Optional

class LeetCodeMCPClient:
    def __init__(self, site: str = "global", session: Optional[str] = None):
        """
        Initialize LeetCode MCP client
        
        Args:
            site: "global" or "cn" for LeetCode site
            session: Optional LeetCode session cookie for authenticated access
        """
        self.site = site
        self.session = session
        self.base_cmd = ["npx", "-y", "@jinzcdev/leetcode-mcp-server"]
        
        # Set environment variables
        self.env = os.environ.copy()
        self.env["LEETCODE_SITE"] = site
        if session:
            self.env["LEETCODE_SESSION"] = session
        
        print(f"✅ LeetCode MCP client initialized for {site} site")
    
    def _run_mcp_command(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run MCP command and return result
        
        Args:
            method: MCP method name
            params: Method parameters
            
        Returns:
            MCP response data
        """
        if params is None:
            params = {}
        
        # Create MCP request
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        try:
            # Write request to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(mcp_request, f)
                request_file = f.name
            
            # Run MCP server command
            cmd = self.base_cmd + ["--request", request_file]
            result = subprocess.run(
                cmd,
                env=self.env,
                capture_output=True,
                text=True,
                timeout=60  # Increased timeout to 60 seconds
            )
            
            # Clean up temp file
            os.unlink(request_file)
            
            if result.returncode != 0:
                print(f"❌ MCP command failed: {result.stderr}")
                return {}
            
            # Parse response
            response = json.loads(result.stdout)
            return response.get("result", {})
            
        except subprocess.TimeoutExpired:
            print("❌ MCP command timed out")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse MCP response: {e}")
            return {}
        except Exception as e:
            print(f"❌ MCP command error: {e}")
            return {}
    
    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get today's daily challenge"""
        print("🔄 Fetching daily challenge...")
        return self._run_mcp_command("leetcode/daily-challenge")
    
    def get_problem(self, title_slug: str) -> Dict[str, Any]:
        """
        Get problem details by slug
        
        Args:
            title_slug: Problem slug (e.g., "two-sum")
        """
        print(f"🔄 Fetching problem: {title_slug}")
        return self._run_mcp_command("leetcode/problem", {"titleSlug": title_slug})
    
    def search_problems(self, keywords: str = "", tags: list = None, difficulty: str = "", limit: int = 10) -> Dict[str, Any]:
        """
        Search problems
        
        Args:
            keywords: Search keywords
            tags: List of tags to filter by
            difficulty: Difficulty level (EASY, MEDIUM, HARD)
            limit: Number of results
        """
        params = {"limit": limit}
        if keywords:
            params["searchKeywords"] = keywords
        if tags:
            params["tags"] = tags
        if difficulty:
            params["difficulty"] = difficulty
        
        print(f"🔄 Searching problems with: {params}")
        return self._run_mcp_command("leetcode/search-problems", params)
    
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Get user profile
        
        Args:
            username: LeetCode username
        """
        print(f"🔄 Fetching user profile: {username}")
        return self._run_mcp_command("leetcode/user-profile", {"username": username})
    
    def get_recent_submissions(self, username: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get user's recent submissions
        
        Args:
            username: LeetCode username
            limit: Number of submissions
        """
        print(f"🔄 Fetching recent submissions for: {username}")
        return self._run_mcp_command("leetcode/recent-submissions", {
            "username": username,
            "limit": limit
        })

# Test function
if __name__ == "__main__":
    # Test the MCP client
    client = LeetCodeMCPClient()
    
    print("Testing LeetCode MCP Client...")
    
    # Test daily challenge
    daily = client.get_daily_challenge()
    print(f"Daily Challenge: {daily}")
    
    # Test problem lookup
    problem = client.get_problem("two-sum")
    print(f"Two Sum Problem: {problem}")
    
    # Test search
    search_results = client.search_problems("array", limit=3)
    print(f"Array Problems: {search_results}")