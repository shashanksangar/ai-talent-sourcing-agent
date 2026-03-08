"""
Base API Client

Abstract base class for all platform API clients.
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAPIClient(ABC):
    """
    Abstract base class for all candidate discovery API clients.
    Provides rate limiting, error handling, and logging.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the API client.
        
        Args:
            config: Configuration dict with API settings
        """
        self.config = config or {}
        self.rate_limit_delay = self.config.get('rate_limit_delay', 1.0)
        self.max_retries = self.config.get('max_retries', 3)
        self.timeout = self.config.get('timeout', 30)
        self.last_request_time = None
    
    @abstractmethod
    def search_candidates(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for candidates matching query criteria.
        
        Args:
            query: Search query string
            filters: Optional filter criteria
        
        Returns:
            List of candidate profiles
        """
        pass
    
    @abstractmethod
    def get_candidate_details(self, candidate_id: str) -> Dict[str, Any]:
        """
        Fetch detailed profile information for a candidate.
        
        Args:
            candidate_id: Unique identifier for the candidate
        
        Returns:
            Detailed candidate profile
        """
        pass
    
    def _apply_rate_limit(self):
        """Apply rate limiting between API requests."""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _log_request(self, platform: str, endpoint: str, params: Dict = None):
        """Log API request details."""
        logger.info(f"[{platform}] GET {endpoint} at {datetime.now().isoformat()}")
        if params:
            logger.debug(f"  Params: {params}")
    
    def _log_response(self, platform: str, status: str, count: int):
        """Log API response summary."""
        logger.info(f"[{platform}] Response: {status}, Found {count} candidates")
    
    def _normalize_candidate(self, raw_data: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """
        Normalize candidate data to standard format.
        
        Args:
            raw_data: Raw candidate data from API
            platform: Source platform name
        
        Returns:
            Normalized candidate profile
        """
        return {
            "id": raw_data.get("id"),
            "name": raw_data.get("name"),
            "platform": platform,
            "platform_url": raw_data.get("url"),
            "skills": raw_data.get("skills", []),
            "experience_level": raw_data.get("experience_level"),
            "research_interests": raw_data.get("research_interests", []),
            "location": raw_data.get("location"),
            "profile_summary": raw_data.get("bio", raw_data.get("summary")),
            "contact_email": raw_data.get("email"),
            "last_updated": datetime.now().isoformat(),
            "raw_data": raw_data
        }
