#!/usr/bin/env python3
"""
AI Talent Sourcing Agent

An agentic tool for automated candidate sourcing.
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
    else:
        print("Sourcing agent initialized. Ready for operation.")
        print("Usage: sourcing-agent --query '<search query>' [--platforms github,arxiv] [--output results.json]")

if __name__ == "__main__":
    main()
