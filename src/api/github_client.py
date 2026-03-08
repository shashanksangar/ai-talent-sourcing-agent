"""
GitHub API Client

Integration with GitHub API to discover AI/ML engineers.
"""

import requests
import logging
from typing import List, Dict, Any
from .base_client import BaseAPIClient

logger = logging.getLogger(__name__)

class GitHubAPIClient(BaseAPIClient):
    """
    GitHub API client for discovering ML engineers and projects.
    Uses GitHub search API to find repositories and users matching criteria.
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize GitHub client.
        
        Args:
            config: Config dict with 'github_token' for authentication
        """
        super().__init__(config)
        self.api_key = self.config.get('github_token')
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AI-Talent-Sourcing-Agent'
        }
        if self.api_key:
            self.headers['Authorization'] = f'token {self.api_key}'
    
    def search_candidates(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for GitHub users matching ML/AI criteria.
        
        Args:
            query: Search query (e.g., "pytorch OR tensorflow language:python")
            filters: Optional filters
        
        Returns:
            List of candidate profiles from GitHub
        """
        self._apply_rate_limit()
        
        # Build GitHub search query
        search_query = self._build_search_query(query, filters)
        
        endpoint = f"{self.BASE_URL}/search/users"
        params = {
            'q': search_query,
            'sort': 'followers',
            'order': 'desc',
            'per_page': 30
        }
        
        self._log_request("GitHub", "/search/users", params)
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            users = response.json().get('items', [])
            candidates = [self._normalize_github_user(user) for user in users]
            
            self._log_response("GitHub", "Success", len(candidates))
            return candidates
        
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {e}")
            return []
    
    def get_candidate_details(self, candidate_id: str) -> Dict[str, Any]:
        """
        Fetch detailed GitHub profile and repository information.
        
        Args:
            candidate_id: GitHub username
        
        Returns:
            Detailed candidate profile
        """
        self._apply_rate_limit()
        
        endpoint = f"{self.BASE_URL}/users/{candidate_id}"
        self._log_request("GitHub", f"/users/{candidate_id}")
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            user_data = response.json()
            
            # Get top repositories
            repos_data = self._get_user_repositories(candidate_id)
            user_data['top_repositories'] = repos_data
            
            return self._normalize_candidate(user_data, "GitHub")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching GitHub user {candidate_id}: {e}")
            return {}
    
    def _get_user_repositories(self, username: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch user's top repositories.
        
        Args:
            username: GitHub username
            limit: Number of repos to fetch
        
        Returns:
            List of repository objects
        """
        self._apply_rate_limit()
        
        endpoint = f"{self.BASE_URL}/users/{username}/repos"
        params = {
            'sort': 'stars',
            'order': 'desc',
            'per_page': limit,
            'type': 'owner'
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()[:limit]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching repos for {username}: {e}")
            return []
    
    def _build_search_query(self, query: str, filters: Dict[str, Any] = None) -> str:
        """
        Build GitHub search query with ML/AI keywords.
        
        Args:
            query: Base query
            filters: Additional filters
        
        Returns:
            Formatted GitHub search query
        """
        filters = filters or {}
        
        # Default ML/AI keywords
        ml_keywords = [
            "machine learning",
            "deep learning",
            "pytorch",
            "tensorflow",
            "neural networks",
            "computer vision",
            "nlp",
            "ai research"
        ]
        
        keyword_query = " OR ".join(ml_keywords)
        search_query = f"{query} {keyword_query} followers:>100"
        
        if filters.get('location'):
            search_query += f" location:{filters['location']}"
        
        if filters.get('min_followers'):
            search_query += f" followers:>{filters['min_followers']}"
        
        return search_query
    
    def _normalize_github_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize GitHub user data to candidate format.
        
        Args:
            user: Raw GitHub user data
        
        Returns:
            Normalized candidate profile
        """
        return {
            "id": user.get('login'),
            "name": user.get('name', user.get('login')),
            "platform": "GitHub",
            "platform_url": user.get('html_url'),
            "bio": user.get('bio'),
            "location": user.get('location'),
            "followers": user.get('followers'),
            "public_repos": user.get('public_repos'),
            "company": user.get('company'),
            "email": user.get('email'),
            "raw_data": user
        }
