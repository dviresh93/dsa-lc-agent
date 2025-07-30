import requests
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class LeetCodeAPIClient:
    def __init__(self, session: Optional[str] = None):
        """
        Initialize LeetCode API client with session cookie
        
        Args:
            session: LeetCode session cookie
        """
        load_dotenv()
        
        self.session = session or os.getenv('LEETCODE_SESSION')
        self.username = os.getenv('LEETCODE_USERNAME', 'dviresh1993')
        
        # Set up session with cookies
        self.requests_session = requests.Session()
        if self.session:
            self.requests_session.cookies.set('LEETCODE_SESSION', self.session, domain='.leetcode.com')
            self.requests_session.cookies.set('csrftoken', 'dummy', domain='.leetcode.com')
        
        # Headers
        self.requests_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Referer': 'https://leetcode.com/',
            'Content-Type': 'application/json',
        })
        
        print(f"✅ LeetCode API client initialized for user: {self.username}")
    
    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get today's daily challenge"""
        try:
            url = 'https://leetcode.com/graphql'
            query = {
                "query": """
                query questionOfToday {
                    activeDailyCodingChallengeQuestion {
                        date
                        userStatus
                        link
                        question {
                            acRate
                            difficulty
                            freqBar
                            frontendQuestionId: questionFrontendId
                            isFavor
                            paidOnly: isPaidOnly
                            status
                            title
                            titleSlug
                            hasVideoSolution
                            hasSolution
                            topicTags {
                                name
                                id
                                slug
                            }
                        }
                    }
                }
                """,
                "variables": {}
            }
            
            response = self.requests_session.post(url, json=query, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']['activeDailyCodingChallengeQuestion']:
                challenge = data['data']['activeDailyCodingChallengeQuestion']
                question = challenge['question']
                return {
                    'questionTitle': question['title'],
                    'difficulty': question['difficulty'],
                    'titleSlug': question['titleSlug'],
                    'date': challenge['date'],
                    'link': f"https://leetcode.com{challenge['link']}"
                }
            return {}
            
        except Exception as e:
            print(f"❌ Error fetching daily challenge: {e}")
            return {}
    
    def get_problem(self, title_slug: str) -> Dict[str, Any]:
        """Get problem details by slug"""
        try:
            url = 'https://leetcode.com/graphql'
            query = {
                "query": """
                query questionData($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                        questionId
                        questionFrontendId
                        title
                        titleSlug
                        content
                        difficulty
                        likes
                        dislikes
                        isLiked
                        similarQuestions
                        topicTags {
                            name
                            slug
                        }
                        stats
                    }
                }
                """,
                "variables": {"titleSlug": title_slug}
            }
            
            response = self.requests_session.post(url, json=query, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']['question']:
                return data['data']['question']
            return {}
            
        except Exception as e:
            print(f"❌ Error fetching problem: {e}")
            return {}
    
    def get_recent_submissions(self, username: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Get user's recent submissions"""
        try:
            username = username or self.username
            url = 'https://leetcode.com/graphql'
            query = {
                "query": """
                query recentSubmissions($username: String!, $limit: Int!) {
                    recentSubmissionList(username: $username, limit: $limit) {
                        title
                        titleSlug
                        timestamp
                        statusDisplay
                        lang
                        runtime
                        memory
                        url
                    }
                }
                """,
                "variables": {"username": username, "limit": limit}
            }
            
            response = self.requests_session.post(url, json=query, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']['recentSubmissionList']:
                return {
                    'submissions': data['data']['recentSubmissionList'],
                    'username': username
                }
            return {}
            
        except Exception as e:
            print(f"❌ Error fetching submissions: {e}")
            return {}
    
    def get_user_profile(self, username: Optional[str] = None) -> Dict[str, Any]:
        """Get user profile"""
        try:
            username = username or self.username
            url = 'https://leetcode.com/graphql'
            query = {
                "query": """
                query userPublicProfile($username: String!) {
                    matchedUser(username: $username) {
                        username
                        profile {
                            realName
                            ranking
                            userAvatar
                            reputation
                            websites
                            countryName
                            company
                            school
                            skillTags
                        }
                        submitStats {
                            acSubmissionNum {
                                difficulty
                                count
                                submissions
                            }
                            totalSubmissionNum {
                                difficulty
                                count
                                submissions
                            }
                        }
                    }
                }
                """,
                "variables": {"username": username}
            }
            
            response = self.requests_session.post(url, json=query, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']['matchedUser']:
                return data['data']['matchedUser']
            return {}
            
        except Exception as e:
            print(f"❌ Error fetching user profile: {e}")
            return {}
    
    def search_problems(self, keywords: str = "", difficulty: str = "", limit: int = 10) -> Dict[str, Any]:
        """Search problems"""
        try:
            url = 'https://leetcode.com/graphql'
            
            # Build filters
            filters = {}
            if difficulty:
                filters["difficulty"] = difficulty.upper()
            if keywords:
                filters["searchKeywords"] = keywords
            
            query = {
                "query": """
                query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                    problemsetQuestionList: questionList(
                        categorySlug: $categorySlug
                        limit: $limit
                        skip: $skip
                        filters: $filters
                    ) {
                        total: totalNum
                        questions: data {
                            acRate
                            difficulty
                            freqBar
                            frontendQuestionId: questionFrontendId
                            isFavor
                            paidOnly: isPaidOnly
                            status
                            title
                            titleSlug
                            topicTags {
                                name
                                id
                                slug
                            }
                            hasSolution
                            hasVideoSolution
                        }
                    }
                }
                """,
                "variables": {
                    "categorySlug": "",
                    "limit": limit,
                    "skip": 0,
                    "filters": filters
                }
            }
            
            response = self.requests_session.post(url, json=query, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']['problemsetQuestionList']:
                return data['data']['problemsetQuestionList']
            return {}
            
        except Exception as e:
            print(f"❌ Error searching problems: {e}")
            return {}

# Test function
if __name__ == "__main__":
    client = LeetCodeAPIClient()
    
    print("Testing LeetCode API Client...")
    
    # Test recent submissions
    submissions = client.get_recent_submissions(limit=3)
    print(f"Recent submissions: {submissions}")
    
    # Test daily challenge
    daily = client.get_daily_challenge()
    print(f"Daily challenge: {daily}")