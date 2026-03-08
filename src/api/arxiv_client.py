"""
ArXiv API Client

Integration with ArXiv API to discover AI/ML researchers.
"""

import feedparser
import logging
from typing import List, Dict, Any
from .base_client import BaseAPIClient
from datetime import datetime

logger = logging.getLogger(__name__)

class ArXivAPIClient(BaseAPIClient):
    """
    ArXiv API client for discovering AI/ML researchers through papers.
    Uses ArXiv search API to find recent papers and extract author information.
    """
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize ArXiv client."""
        super().__init__(config)
    
    def search_candidates(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for researchers by papers on ArXiv.
        
        Args:
            query: Search query (e.g., "computer vision transformers")
            filters: Optional filters (max_results, category, etc.)
        
        Returns:
            List of candidate profiles extracted from papers
        """
        self._apply_rate_limit()
        
        filters = filters or {}
        max_results = filters.get('max_results', 50)
        category = filters.get('category', 'cs.AI')
        
        # Format ArXiv search query
        search_query = self._format_arxiv_query(query, category)
        
        params = f"?search_query={search_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        url = f"{self.BASE_URL}{params}"
        
        self._log_request("ArXiv", "/api/query", {"query": search_query})
        
        try:
            feed = feedparser.parse(url)
            
            candidates = {}  # Use dict to deduplicate by author
            
            for entry in feed.entries:
                authors = entry.get('authors', [])
                for author in authors:
                    author_name = author.get('name', 'Unknown')
                    
                    if author_name not in candidates:
                        candidates[author_name] = self._normalize_arxiv_author(
                            author_name,
                            entry,
                            authors
                        )
            
            candidate_list = list(candidates.values())
            self._log_response("ArXiv", "Success", len(candidate_list))
            return candidate_list
        
        except Exception as e:
            logger.error(f"ArXiv API error: {e}")
            return []
    
    def get_candidate_details(self, candidate_id: str) -> Dict[str, Any]:
        """
        Fetch detailed information about a researcher.
        
        Args:
            candidate_id: Researcher name
        
        Returns:
            Detailed candidate profile
        """
        self._apply_rate_limit()
        
        # Search for papers by this author
        search_query = self._format_arxiv_query(f'au:{candidate_id}', None)
        params = f"?search_query={search_query}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending"
        url = f"{self.BASE_URL}{params}"
        
        self._log_request("ArXiv", "/api/query", {"author": candidate_id})
        
        try:
            feed = feedparser.parse(url)
            
            papers = []
            research_interests = set()
            
            for entry in feed.entries:
                paper = {
                    "title": entry.get('title'),
                    "published": entry.get('published'),
                    "summary": entry.get('summary'),
                    "arxiv_id": entry.get('id').split('/abs/')[-1],
                    "categories": entry.get('arxiv_primary_category', {}).get('term', '')
                }
                papers.append(paper)
                
                # Extract research interests from categories
                if paper['categories']:
                    research_interests.add(paper['categories'])
            
            candidate_profile = {
                "id": candidate_id,
                "name": candidate_id,
                "platform": "ArXiv",
                "papers": papers,
                "research_interests": list(research_interests),
                "paper_count": len(papers),
                "last_publication": papers[0].get('published') if papers else None,
                "raw_data": {
                    "papers": papers
                }
            }
            
            return candidate_profile
        
        except Exception as e:
            logger.error(f"Error fetching ArXiv details for {candidate_id}: {e}")
            return {}
    
    def _format_arxiv_query(self, query: str, category: str = None) -> str:
        """
        Format search query for ArXiv API.
        
        Args:
            query: Search query
            category: ArXiv category (cs.AI, cs.CV, etc.)
        
        Returns:
            Formatted query string
        """
        # Replace spaces with %20 for URL encoding
        formatted = query.replace(" ", "%20")
        
        if category:
            formatted = f"cat:{category}%20AND%20({formatted})"
        
        return formatted
    
    def _normalize_arxiv_author(self, name: str, paper: Dict[str, Any], all_authors: List) -> Dict[str, Any]:
        """
        Normalize ArXiv author data to candidate format.
        
        Args:
            name: Author name
            paper: Paper data from ArXiv
            all_authors: List of paper authors
        
        Returns:
            Normalized candidate profile
        """
        return {
            "id": name,
            "name": name,
            "platform": "ArXiv",
            "platform_url": f"https://arxiv.org/search/?query={name}&searchtype=author",
            "research_interests": [
                paper.get('arxiv_primary_category', {}).get('term', 'cs.AI')
            ],
            "recent_paper": {
                "title": paper.get('title'),
                "arxiv_id": paper.get('id').split('/abs/')[-1],
                "published": paper.get('published')
            },
            "co_authors": [
                auth.get('name') for auth in all_authors 
                if auth.get('name') != name
            ][:5],  # Top 5 collaborators
            "raw_data": paper
        }
