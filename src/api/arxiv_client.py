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
    
    def search_papers(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for papers on ArXiv.
        
        Args:
            query: Search query
            filters: Optional filters (max_results, category, etc.)
        
        Returns:
            List of paper details
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
            
            papers = []
            for entry in feed.entries:
                paper = {
                    "title": entry.get('title'),
                    "authors": [auth.get('name') for auth in entry.get('authors', [])],
                    "published": entry.get('published'),
                    "updated": entry.get('updated'),
                    "summary": entry.get('summary'),
                    "arxiv_id": entry.get('id').split('/abs/')[-1],
                    "categories": entry.get('tags', []),
                    "pdf_url": entry.get('id').replace('/abs/', '/pdf/'),
                    "abs_url": entry.get('id')
                }
                papers.append(paper)
            
            self._log_response("ArXiv", "Success", len(papers))
            return papers
        
        except Exception as e:
            logger.error(f"ArXiv API error: {e}")
            return []
    
    def search_icra_papers(self, query: str = "", year: int = None, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for papers published at ICRA (International Conference on Robotics and Automation).

        This method specifically filters for papers that mention 'ICRA' or
        'International Conference on Robotics and Automation' in their comment
        or journal-ref fields.

        Args:
            query: Additional search query terms (e.g., "foundation models", "end-to-end learning")
            year: Specific ICRA year (e.g., 2025, 2024)
            filters: Optional filters (max_results, etc.)

        Returns:
            List of ICRA papers with author information
        """
        self._apply_rate_limit()

        filters = filters or {}
        max_results = filters.get('max_results', 100)

        # Build search query for robotics with ICRA filter
        # ArXiv doesn't allow direct filtering on comment/journal-ref in search query,
        # so we search robotics papers and filter results
        base_query = "cat:cs.RO"  # Robotics category

        if query:
            search_query = f"{base_query}%20AND%20({self._format_arxiv_query(query, None)})"
        else:
            search_query = base_query

        params = f"?search_query={search_query}&start=0&max_results={max_results * 2}&sortBy=submittedDate&sortOrder=descending"
        url = f"{self.BASE_URL}{params}"

        self._log_request("ArXiv", "/api/query (ICRA filter)", {"query": search_query, "year": year})

        try:
            feed = feedparser.parse(url)

            icra_papers = []
            for entry in feed.entries:
                # Check if paper is ICRA publication
                comment = entry.get('arxiv_comment', '').lower()
                journal_ref = entry.get('arxiv_journal_ref', '').lower()

                is_icra = False
                icra_year = None

                # Check for ICRA mentions
                if 'icra' in comment or 'icra' in journal_ref:
                    is_icra = True
                    # Try to extract year from comment/journal_ref
                    for field in [comment, journal_ref]:
                        if 'icra' in field:
                            # Look for year pattern (e.g., "ICRA 2025", "ICRA-2024")
                            import re
                            year_match = re.search(r'icra[\s-]?(\d{4})', field)
                            if year_match:
                                icra_year = int(year_match.group(1))
                                break

                elif 'international conference on robotics and automation' in comment or \
                     'international conference on robotics and automation' in journal_ref:
                    is_icra = True

                # Apply year filter if specified
                if is_icra:
                    if year and icra_year and icra_year != year:
                        continue

                    paper = {
                        "title": entry.get('title'),
                        "authors": [auth.get('name') for auth in entry.get('authors', [])],
                        "published": entry.get('published'),
                        "updated": entry.get('updated'),
                        "summary": entry.get('summary'),
                        "arxiv_id": entry.get('id').split('/abs/')[-1],
                        "categories": entry.get('tags', []),
                        "pdf_url": entry.get('id').replace('/abs/', '/pdf/'),
                        "abs_url": entry.get('id'),
                        "conference": "ICRA",
                        "conference_year": icra_year,
                        "comment": entry.get('arxiv_comment', ''),
                        "journal_ref": entry.get('arxiv_journal_ref', '')
                    }
                    icra_papers.append(paper)

            self._log_response("ArXiv", "ICRA papers found", len(icra_papers))
            logger.info(f"Found {len(icra_papers)} ICRA papers" + (f" from {year}" if year else ""))

            return icra_papers[:max_results]  # Limit to requested max

        except Exception as e:
            logger.error(f"ArXiv ICRA search error: {e}")
            return []

    def search_icra_authors(self, query: str = "", year: int = None, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Search for authors who have published at ICRA.

        Args:
            query: Research area filter (e.g., "foundation models", "end-to-end learning")
            year: Specific ICRA year (e.g., 2025, 2024)
            filters: Optional filters (max_results, etc.)

        Returns:
            List of unique ICRA author profiles with their papers
        """
        # Get ICRA papers
        icra_papers = self.search_icra_papers(query, year, filters)

        # Extract unique authors
        author_profiles = {}

        for paper in icra_papers:
            for author_name in paper.get('authors', []):
                if author_name not in author_profiles:
                    author_profiles[author_name] = {
                        "id": author_name,
                        "name": author_name,
                        "platform": "ArXiv",
                        "platform_url": f"https://arxiv.org/search/?query={author_name}&searchtype=author",
                        "icra_papers": [],
                        "research_interests": set(),
                        "icra_years": set()
                    }

                # Add paper to author's profile
                author_profiles[author_name]["icra_papers"].append({
                    "title": paper.get('title'),
                    "arxiv_id": paper.get('arxiv_id'),
                    "published": paper.get('published'),
                    "conference_year": paper.get('conference_year'),
                    "summary": paper.get('summary', '')[:200] + "..."
                })

                # Track research interests and years
                if paper.get('conference_year'):
                    author_profiles[author_name]["icra_years"].add(paper.get('conference_year'))

                # Extract research interests from categories
                for tag in paper.get('categories', []):
                    if hasattr(tag, 'term'):
                        author_profiles[author_name]["research_interests"].add(tag.term)

        # Convert sets to lists and format profiles
        result = []
        for author_name, profile in author_profiles.items():
            profile["research_interests"] = list(profile["research_interests"])
            profile["icra_years"] = sorted(list(profile["icra_years"]), reverse=True)
            profile["icra_paper_count"] = len(profile["icra_papers"])
            profile["recent_icra_paper"] = profile["icra_papers"][0] if profile["icra_papers"] else None

            # Add ICRA-specific metadata
            profile["is_icra_author"] = True
            profile["most_recent_icra_year"] = profile["icra_years"][0] if profile["icra_years"] else None

            result.append(profile)

        # Sort by number of ICRA papers (most prolific first)
        result.sort(key=lambda x: x.get('icra_paper_count', 0), reverse=True)

        logger.info(f"Found {len(result)} unique ICRA authors")
        return result

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
