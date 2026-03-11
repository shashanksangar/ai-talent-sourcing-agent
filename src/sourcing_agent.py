#!/usr/bin/env python3
"""
AI Talent Sourcing Agent

An agentic tool for automated candidate sourcing with AI evaluation.
"""

import argparse
import os
import json
import logging
from dotenv import load_dotenv

# Import API clients
from src.api.github_client import GitHubAPIClient
from src.api.arxiv_client import ArXivAPIClient
from src.api.linkedin_client import LinkedInAPIClient
from src.utils.config import APIConfig
from src.models.candidate import SearchFilter

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SourcingAgent:
    """Main sourcing agent for discovering candidates."""
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize the sourcing agent.
        
        Args:
            config_file: Path to configuration file
        """
        self.api_config = APIConfig(config_file)
        
        if not self.api_config.validate():
            logger.warning("Configuration validation failed. Some features may be limited.")
        
        # Initialize API clients
        self.github_client = GitHubAPIClient(self.api_config.get_github_config())
        self.arxiv_client = ArXivAPIClient(self.api_config.get_arxiv_config())
        self.linkedin_client = LinkedInAPIClient(self.api_config.get_linkedin_config())
        
        self.candidates = {}
    
    def search_candidates(self, query: str, platforms: list = None) -> dict:
        """
        Search for candidates across configured platforms.
        
        Args:
            query: Search query
            platforms: List of platforms to search (default: all)
        
        Returns:
            Dict of candidates found on each platform
        """
        platforms = platforms or ['github', 'arxiv']
        results = {}
        
        logger.info(f"Starting candidate search for: '{query}' on platforms: {platforms}")
        
        if 'github' in platforms:
            logger.info("Searching GitHub...")
            try:
                github_candidates = self.github_client.search_candidates(query)
                results['github'] = github_candidates
                logger.info(f"  Found {len(github_candidates)} candidates on GitHub")
            except Exception as e:
                logger.error(f"GitHub search failed: {e}")
                results['github'] = []
        
        if 'arxiv' in platforms:
            logger.info("Searching ArXiv...")
            try:
                arxiv_candidates = self.arxiv_client.search_candidates(query)
                results['arxiv'] = arxiv_candidates
                logger.info(f"  Found {len(arxiv_candidates)} candidates on ArXiv")
            except Exception as e:
                logger.error(f"ArXiv search failed: {e}")
                results['arxiv'] = []
        
        if 'linkedin' in platforms:
            logger.info("LinkedIn search not yet available")
            results['linkedin'] = []
        
        # Merge results
        for platform, candidates in results.items():
            for candidate in candidates:
                candidate_id = f"{platform}_{candidate.get('id', 'unknown')}"
                self.candidates[candidate_id] = candidate
        
        return results
    
    def track_latest_papers(self, team_keywords: list = None, max_results: int = 20) -> list:
        """
        Track the latest papers relevant to the team.
        
        Args:
            team_keywords: List of keywords relevant to the team (default: from config)
            max_results: Maximum number of papers to return
        
        Returns:
            List of latest relevant papers
        """
        team_keywords = team_keywords or self.api_config.get('keywords', ['machine learning', 'deep learning'])
        
        # Use the first keyword as primary search, others as additional terms
        primary_keyword = team_keywords[0]
        additional_terms = ' '.join(team_keywords[1:])
        query = f"{primary_keyword} {additional_terms}".strip()
        
        logger.info(f"Tracking latest papers for team keywords: {team_keywords}")
        
        try:
            papers = self.arxiv_client.search_papers(query, {'max_results': max_results})
            logger.info(f"Found {len(papers)} recent papers")
            return papers
        except Exception as e:
            logger.error(f"Failed to track papers: {e}")
            return []
    
    def find_emerging_talent(self, research_areas: list, max_results: int = 20) -> list:
        """
        Find emerging AI talent in specific research areas.
        
        Emerging talent criteria:
        - Recent publications (last 2 years)
        - Limited publication history (fewer than 10 papers)
        - Active in specified research areas
        
        Args:
            research_areas: List of research areas to focus on
            max_results: Maximum number of candidates to return
        
        Returns:
            List of emerging talent profiles
        """
        query = ' '.join(research_areas)  # Combine research areas into search query
        
        logger.info(f"Finding emerging talent in: {research_areas}")
        
        # Search for recent papers in these areas
        papers = self.arxiv_client.search_papers(query, {'max_results': max_results * 3})  # Get more papers to find authors
        
        # Extract unique authors from recent papers
        author_papers = {}  # author -> list of their papers
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=730)  # 2 years ago
        
        for paper in papers:
            pub_date_str = paper.get('published')
            if pub_date_str:
                try:
                    pub_date = datetime.strptime(pub_date_str[:10], '%Y-%m-%d')
                    if pub_date > cutoff_date:  # Only recent papers
                        for author in paper.get('authors', []):
                            if author not in author_papers:
                                author_papers[author] = []
                            author_papers[author].append(paper)
                except ValueError:
                    pass  # Skip if date parsing fails
        
        # Filter for emerging talent (fewer than 10 papers)
        emerging_talent = []
        for author, papers_list in author_papers.items():
            if len(papers_list) < 10:  # Emerging talent threshold
                # Create candidate profile
                recent_paper = max(papers_list, key=lambda p: p.get('published', ''))
                candidate = {
                    "id": author,
                    "name": author,
                    "platform": "ArXiv",
                    "platform_url": f"https://arxiv.org/search/?query={author}&searchtype=author",
                    "research_interests": research_areas,
                    "recent_paper": {
                        "title": recent_paper.get('title'),
                        "arxiv_id": recent_paper.get('arxiv_id'),
                        "published": recent_paper.get('published')
                    },
                    "paper_count": len(papers_list),
                    "raw_data": {
                        "papers": papers_list
                    }
                }
                emerging_talent.append(candidate)
        
        # Sort by recency and paper count (prefer more recent with fewer papers)
        emerging_talent.sort(key=lambda x: (x.get('recent_paper', {}).get('published', ''), -x.get('paper_count', 0)), reverse=True)
        emerging_talent = emerging_talent[:max_results]
        
        logger.info(f"Found {len(emerging_talent)} emerging talent candidates")
        return emerging_talent
    
    def get_candidate_details(self, platform: str, candidate_id: str) -> dict:
        """
        Fetch detailed information about a candidate.
        
        Args:
            platform: Source platform
            candidate_id: Candidate identifier
        
        Returns:
            Detailed candidate profile
        """
        if platform == 'github':
            details = self.github_client.get_candidate_details(candidate_id)
        elif platform == 'arxiv':
            details = self.arxiv_client.get_candidate_details(candidate_id)
        elif platform == 'linkedin':
            details = self.linkedin_client.get_candidate_details(candidate_id)
        else:
            logger.error(f"Unknown platform: {platform}")
            return {}
        
        return details
    
    def evaluate_with_ai(self, candidate: dict, job_requirements: dict):
        """
        Evaluate a candidate using Claude AI.
        
        Args:
            candidate: Candidate profile
            job_requirements: Job details
        
        Returns:
            Evaluation results
            
        Note: Requires importing and using the AIEvaluator separately
        See example_with_evaluation.py for usage
        """
        logger.info(f"To evaluate with Claude, use SourcingOrchestrator from src.orchestrator")
        return None
    
    def export_candidates(self, output_file: str = "candidates.json"):
        """
        Export discovered candidates to file.
        
        Args:
            output_file: Output file path
        """
        with open(output_file, 'w') as f:
            json.dump(self.candidates, f, indent=2)
        
        logger.info(f"Exported {len(self.candidates)} candidates to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="AI Talent Sourcing Agent")
    parser.add_argument("--query", type=str, help="Search query for candidates")
    parser.add_argument("--platforms", type=str, default="github,arxiv", 
                       help="Comma-separated list of platforms to search")
    parser.add_argument("--output", type=str, help="Output file for results")
    parser.add_argument("--config", type=str, default="config.yaml", help="Configuration file")
    args = parser.parse_args()

    logger.info("AI Talent Sourcing Agent starting...")
    
    agent = SourcingAgent(args.config)
    
    if args.query:
        platforms = [p.strip() for p in args.platforms.split(",")]
        results = agent.search_candidates(args.query, platforms)
        
        # Display results
        for platform, candidates in results.items():
            if candidates:
                print(f"\n{platform.upper()} Results ({len(candidates)} candidates):")
                for candidate in candidates[:5]:  # Show first 5
                    print(f"  - {candidate.get('name', 'Unknown')} ({candidate.get('id')})")
                if len(candidates) > 5:
                    print(f"  ... and {len(candidates) - 5} more")
        
        if args.output:
            agent.export_candidates(args.output)
            print(f"\nFull results exported to {args.output}")
        
        print("\n" + "=" * 60)
        print("To evaluate candidates with AI, use:")
        print("  from src.orchestrator import SourcingOrchestrator")
        print("  See example_with_evaluation.py for complete pipeline")
    else:
        print("Sourcing agent initialized. Ready for operation.")
        print("Usage: sourcing-agent --query '<search query>' [--platforms github,arxiv] [--output results.json]")
        print("\nFor AI evaluation pipeline, use: python example_with_evaluation.py")

if __name__ == "__main__":
    main()
