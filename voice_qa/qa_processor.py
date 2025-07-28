from openai import OpenAI
import os
import json
from typing import Optional, Dict, Any
from leetcode_api_client import LeetCodeAPIClient
from dotenv import load_dotenv

class QAProcessor:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Q&A processor with OpenAI integration
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Set up OpenAI API key
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.use_openai = True
            print("✅ OpenAI API configured successfully!")
        else:
            self.client = None
            self.use_openai = False
            print("⚠️ No OpenAI API key found. Using fallback responses.")
        
        # Initialize LeetCode MCP client
        try:
            # Get credentials from .env file
            session = os.getenv('LEETCODE_SESSION')
            username = os.getenv('LEETCODE_USERNAME', 'dviresh1993')  # Default username
            site = os.getenv('LEETCODE_SITE', 'global')
            
            self.leetcode_client = LeetCodeAPIClient(session=session)
            self.default_username = username
            self.mcp_available = True
        except Exception as e:
            print(f"⚠️ LeetCode MCP client failed to initialize: {e}")
            self.leetcode_client = None
            self.mcp_available = False
        
        # Fallback responses for when OpenAI is not available
        self.fallback_responses = {
            "hello": "Hello! I'm your voice assistant. I can help with LeetCode problems and general questions!",
            "hi": "Hi there! Ask me about LeetCode problems or any other questions!",
            "how are you": "I'm doing great! Ready to help with LeetCode or other questions. How can I assist you?",
            "what is your name": "I'm your voice assistant powered by AI with LeetCode integration.",
            "goodbye": "Goodbye! It was nice talking with you.",
            "bye": "Bye! Have a great day!",
            "thank you": "You're welcome! Is there anything else I can help you with?",
            "thanks": "You're welcome!",
        }
    
    def process_question(self, question: str) -> str:
        """
        Process a question using OpenAI API with MCP functions or fallback responses
        
        Args:
            question: User's question as text
            
        Returns:
            Response text
        """
        if not question.strip():
            return "I didn't hear anything. Could you please repeat your question?"
        
        # Try OpenAI with function calling (LLM decides when to use MCP)
        if self.use_openai:
            try:
                return self._get_openai_response_with_mcp(question)
            except Exception as e:
                print(f"⚠️ OpenAI API error: {e}")
                print("Falling back to local responses...")
        
        # Fallback to local responses
        return self._get_fallback_response(question)
    
    def _get_openai_response_with_mcp(self, question: str) -> str:
        """Get OpenAI response with function calling for MCP functions"""
        try:
            # Define available MCP functions for OpenAI
            functions = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_daily_challenge",
                        "description": "Get today's LeetCode daily challenge problem",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                },
                {
                    "type": "function", 
                    "function": {
                        "name": "get_problem",
                        "description": "Get details about a specific LeetCode problem",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title_slug": {
                                    "type": "string",
                                    "description": "The problem slug (e.g., 'two-sum', 'add-two-numbers')"
                                }
                            },
                            "required": ["title_slug"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "search_problems", 
                        "description": "Search for LeetCode problems by keywords, tags, or difficulty",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "keywords": {
                                    "type": "string",
                                    "description": "Search keywords"
                                },
                                "difficulty": {
                                    "type": "string", 
                                    "enum": ["EASY", "MEDIUM", "HARD"],
                                    "description": "Problem difficulty level"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of results to return",
                                    "default": 5
                                }
                            },
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_user_profile",
                        "description": "Get LeetCode user profile information", 
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "LeetCode username (optional if default user is set)"
                                }
                            },
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_recent_submissions",
                        "description": "Get user's recent LeetCode submissions",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "username": {
                                    "type": "string",
                                    "description": "LeetCode username (optional if default user is set)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of submissions to return",
                                    "default": 10
                                }
                            },
                            "required": []
                        }
                    }
                }
            ]
            
            # Make initial request with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful voice assistant with access to LeetCode data. Use the available functions when users ask about LeetCode problems, daily challenges, or coding questions. Give concise, conversational responses (1-3 sentences)."
                    },
                    {
                        "role": "user", 
                        "content": question
                    }
                ],
                tools=functions,
                tool_choice="auto",
                max_tokens=150,
                temperature=0.7
            )
            
            # Check if the model wants to call a function
            if response.choices[0].message.tool_calls:
                # Handle function calls
                return self._handle_function_calls(response, question)
            else:
                # Regular response
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            raise e
    
    def _handle_function_calls(self, response, original_question: str) -> str:
        """Handle OpenAI function calls by executing MCP functions"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful voice assistant. Give concise, conversational responses (1-3 sentences)."
            },
            {
                "role": "user",
                "content": original_question
            },
            response.choices[0].message
        ]
        
        # Execute each function call
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            try:
                # Call the appropriate MCP function
                if function_name == "get_daily_challenge":
                    result = self.leetcode_client.get_daily_challenge()
                elif function_name == "get_problem":
                    result = self.leetcode_client.get_problem(function_args["title_slug"])
                elif function_name == "search_problems":
                    result = self.leetcode_client.search_problems(
                        keywords=function_args.get("keywords", ""),
                        difficulty=function_args.get("difficulty", ""),
                        limit=function_args.get("limit", 5)
                    )
                elif function_name == "get_user_profile":
                    username = function_args.get("username", self.default_username)
                    if not username:
                        result = {"error": "No username provided and no default username set"}
                    else:
                        result = self.leetcode_client.get_user_profile(username)
                elif function_name == "get_recent_submissions":
                    username = function_args.get("username", self.default_username)
                    if not username:
                        result = {"error": "No username provided and no default username set"}
                    else:
                        result = self.leetcode_client.get_recent_submissions(
                            username,
                            limit=function_args.get("limit", 10)
                        )
                else:
                    result = {"error": f"Unknown function: {function_name}"}
                
                # Add function result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                
            except Exception as e:
                # Add error result
                messages.append({
                    "role": "tool", 
                    "tool_call_id": tool_call.id,
                    "content": json.dumps({"error": str(e)})
                })
        
        # Get final response from OpenAI
        final_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return final_response.choices[0].message.content.strip()
    
    def _get_fallback_response(self, question: str) -> str:
        """Get fallback response when OpenAI is not available"""
        question_lower = question.lower().strip()
        
        # Check for direct matches in fallback responses
        for key, response in self.fallback_responses.items():
            if key in question_lower:
                return response
        
        # Handle specific question types
        if any(word in question_lower for word in ["what", "how", "why", "when", "where", "who"]):
            return "That's an interesting question! I'd recommend checking reliable sources for detailed information on this topic."
        elif any(word in question_lower for word in ["calculate", "math", "plus", "minus"]):
            return "I can help with basic math, but I'd need my full capabilities for complex calculations."
        else:
            return "I'm sorry, I need my AI capabilities to answer that properly. Please check your OpenAI API configuration."
    
    def _get_leetcode_session(self) -> Optional[str]:
        """Extract LeetCode session from .mcp.json or environment"""
        try:
            # First try environment variable
            session = os.getenv('LEETCODE_SESSION')
            if session:
                return session
            
            # Try to read from .mcp.json
            mcp_config_path = '/home/virus/Documents/repo/lc_problems/.mcp.json'
            if os.path.exists(mcp_config_path):
                with open(mcp_config_path, 'r') as f:
                    config = json.load(f)
                    
                # Extract session from args
                leetcode_config = config.get('mcpServers', {}).get('leetcode', {})
                args = leetcode_config.get('args', [])
                
                # Find --session argument
                for i, arg in enumerate(args):
                    if arg == '--session' and i + 1 < len(args):
                        return args[i + 1]
            
            return None
        except Exception as e:
            print(f"⚠️ Failed to get LeetCode session: {e}")
            return None

# Test function
if __name__ == "__main__":
    # Test with and without API key
    qa = QAProcessor()
    
    test_questions = [
        "Hello, how are you?",
        "What is Python programming?",
        "Explain machine learning briefly",
        "What's the capital of France?",
    ]
    
    print("Testing Q&A Processor...")
    for question in test_questions:
        response = qa.process_question(question)
        print(f"Q: {question}")
        print(f"A: {response}")
        print("-" * 50)