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

    def find_icra_authors(self, research_area: str = "", year: int = None, max_results: int = 20) -> list:
        """
        Find authors who have published at ICRA (International Conference on Robotics and Automation).

        This is particularly useful for finding robotics talent with proven track records at
        top-tier conferences like ICRA.

        Args:
            research_area: Specific research area to filter (e.g., "foundation models",
                          "end-to-end learning", "manipulation")
            year: Specific ICRA year to search (e.g., 2025, 2024). If None, searches all years.
            max_results: Maximum number of authors to return

        Returns:
            List of ICRA author profiles with their publications

        Examples:
            # Find all ICRA 2025 authors working on foundation models
            authors = agent.find_icra_authors("foundation models", year=2025)

            # Find ICRA authors working on end-to-end learning (any year)
            authors = agent.find_icra_authors("end-to-end learning")

            # Find all recent ICRA authors
            authors = agent.find_icra_authors(year=2024)
        """
        logger.info(f"Searching for ICRA authors" +
                   (f" in '{research_area}'" if research_area else "") +
                   (f" from ICRA {year}" if year else ""))

        try:
            # Use the ArXiv client's ICRA search method
            authors = self.arxiv_client.search_icra_authors(
                query=research_area,
                year=year,
                filters={'max_results': max_results}
            )

            # Store in candidates dict
            for author in authors:
                candidate_id = f"arxiv_icra_{author.get('id', 'unknown')}"
                self.candidates[candidate_id] = author

            logger.info(f"Found {len(authors)} ICRA authors")

            # Add summary stats
            if authors:
                total_papers = sum(a.get('icra_paper_count', 0) for a in authors)
                years_represented = set()
                for a in authors:
                    years_represented.update(a.get('icra_years', []))

                logger.info(f"  Total ICRA papers: {total_papers}")
                logger.info(f"  Years represented: {sorted(years_represented, reverse=True)}")

            return authors

        except Exception as e:
            logger.error(f"Failed to search ICRA authors: {e}")
            return []
    
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

    def generate_hm_summary(
        self,
        candidates: list,
        job_title: str = "Robotics ML Engineer - Core Autonomy",
        team_name: str = "Core Autonomy / Tesla Optimus",
        output_file: str = "HM_Summary.md",
        top_n: int = 3
    ):
        """
        Generate a hiring manager summary report with top candidates.

        Creates a professional markdown report with:
        - Top N candidates
        - ICRA paper titles
        - Fit summaries for the team
        - Drafted email for the hiring manager

        Args:
            candidates: List of candidate profiles (typically ICRA authors)
            job_title: Position title
            team_name: Team/division name
            output_file: Output markdown file path
            top_n: Number of top candidates to include (default: 3)

        Returns:
            Path to generated summary file
        """
        from datetime import datetime

        if not candidates:
            logger.warning("No candidates provided for HM summary")
            return None

        # Take top N candidates
        top_candidates = candidates[:top_n]

        # Generate summary content
        summary = f"""# Hiring Manager Summary
## {job_title} - {team_name}

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
**Total Candidates Reviewed:** {len(candidates)}
**Top Candidates Presented:** {len(top_candidates)}

---

## 🎯 Top {len(top_candidates)} Candidates

"""

        # Add each candidate
        for i, candidate in enumerate(top_candidates, 1):
            name = candidate.get('name', 'Unknown')
            icra_papers = candidate.get('icra_papers', [])
            icra_paper_count = candidate.get('icra_paper_count', 0)
            icra_years = candidate.get('icra_years', [])
            research_interests = candidate.get('research_interests', [])
            platform_url = candidate.get('platform_url', '')

            # Get most recent ICRA paper
            recent_paper = candidate.get('recent_icra_paper') or (icra_papers[0] if icra_papers else None)
            paper_title = recent_paper.get('title', 'N/A') if recent_paper else 'N/A'
            paper_year = recent_paper.get('conference_year', 'N/A') if recent_paper else 'N/A'

            # Generate fit summary (2 sentences)
            fit_summary = self._generate_fit_summary(candidate, team_name)

            summary += f"""### {i}. {name}

**ICRA Publications:** {icra_paper_count} paper{'s' if icra_paper_count != 1 else ''} ({', '.join(map(str, icra_years)) if icra_years else 'N/A'})

**Most Recent ICRA Paper:**
*"{paper_title}"* (ICRA {paper_year})

**Why This Candidate Fits {team_name}:**
{fit_summary}

**Research Interests:** {', '.join(research_interests[:5]) if research_interests else 'N/A'}

**Profile:** {platform_url}

---

"""

        # Add drafted email section
        summary += self._generate_hm_email(top_candidates, job_title, team_name)

        # Write to file
        with open(output_file, 'w') as f:
            f.write(summary)

        logger.info(f"Generated HM summary with {len(top_candidates)} candidates: {output_file}")
        print(f"\n✅ HM Summary generated: {output_file}")

        return output_file

    def _generate_fit_summary(self, candidate: dict, team_name: str) -> str:
        """
        Generate a 2-sentence summary of why candidate fits the team.

        Args:
            candidate: Candidate profile
            team_name: Team name

        Returns:
            2-sentence fit summary
        """
        name = candidate.get('name', 'This candidate')
        icra_paper_count = candidate.get('icra_paper_count', 0)
        icra_years = candidate.get('icra_years', [])
        recent_paper = candidate.get('recent_icra_paper')
        research_interests = candidate.get('research_interests', [])

        # Extract key terms from research interests
        has_robotics = any('robot' in str(r).lower() for r in research_interests)
        has_ai_ml = any(term in str(research_interests).lower() for term in ['cs.ai', 'cs.lg', 'cs.cv', 'machine learning', 'deep learning'])

        # Build first sentence based on ICRA track record
        most_recent_year = icra_years[0] if icra_years else 'recent'

        if icra_paper_count > 1:
            sentence1 = f"{name} has a strong track record in robotics research with {icra_paper_count} publications at ICRA (most recently {most_recent_year}), demonstrating proven expertise in cutting-edge robotic systems relevant to {team_name}."
        else:
            sentence1 = f"{name} brings robotics expertise demonstrated through recent ICRA {most_recent_year} publication, showing active engagement with state-of-the-art research directly applicable to {team_name}."

        # Build second sentence based on paper content or research interests
        paper_title = recent_paper.get('title', '').lower() if recent_paper else ''

        # Check for relevant keywords in paper title
        if any(term in paper_title for term in ['foundation', 'end-to-end', 'learning', 'manipulation', 'imitation', 'policy']):
            if 'foundation' in paper_title or 'end-to-end' in paper_title:
                sentence2 = "Their work on foundation models and end-to-end learning aligns perfectly with our goals of building scalable, generalizable robotic systems for humanoid manipulation tasks."
            elif 'manipulation' in paper_title or 'grasp' in paper_title:
                sentence2 = "Their focus on robotic manipulation and dexterous control directly addresses the core challenges we face in developing capable humanoid robot behaviors."
            elif 'imitation' in paper_title or 'learning' in paper_title:
                sentence2 = "Their expertise in learning-based approaches and imitation learning is critical for our work in developing data-efficient training methods for robotic behaviors."
            else:
                sentence2 = "Their research background in robot learning and control systems provides the technical foundation needed to advance our humanoid robotics capabilities."
        elif has_robotics and has_ai_ml:
            sentence2 = "The combination of robotics domain knowledge and modern ML techniques makes them well-suited to tackle the challenging problems in embodied AI and real-world robot deployment."
        else:
            sentence2 = "Their research in robotics and automation positions them to contribute meaningfully to our mission of building intelligent, capable humanoid robots."

        return f"{sentence1} {sentence2}"

    def _generate_hm_email(self, candidates: list, job_title: str, team_name: str) -> str:
        """
        Generate a drafted email to send to the hiring manager.

        Args:
            candidates: List of top candidates
            job_title: Position title
            team_name: Team name

        Returns:
            Formatted email draft as markdown
        """
        from datetime import datetime

        candidate_names = [c.get('name', 'Unknown') for c in candidates]
        total_icra_papers = sum(c.get('icra_paper_count', 0) for c in candidates)

        # Get year range
        all_years = []
        for c in candidates:
            all_years.extend(c.get('icra_years', []))
        year_range = f"{min(all_years)}-{max(all_years)}" if all_years else "recent years"

        email = f"""## 📧 Drafted Email to Hiring Manager

---

**Subject:** Top ICRA Authors for {job_title} - {len(candidates)} Strong Candidates Identified

**To:** [Hiring Manager Name]
**From:** [Your Name]
**Date:** {datetime.now().strftime('%B %d, %Y')}

---

Hi [HM Name],

I wanted to share some exciting findings from our latest sourcing effort for the **{job_title}** position on the **{team_name}** team.

I've identified **{len(candidates)} exceptional candidates** who have published at **ICRA (International Conference on Robotics and Automation)**, one of the premier robotics conferences. These researchers have a combined **{total_icra_papers} publications** at ICRA spanning **{year_range}**, demonstrating both depth and currency in cutting-edge robotics research.

### Top Candidates:

"""

        for i, candidate in enumerate(candidates, 1):
            name = candidate.get('name', 'Unknown')
            recent_paper = candidate.get('recent_icra_paper', {})
            paper_title = recent_paper.get('title', 'N/A') if recent_paper else 'N/A'
            icra_count = candidate.get('icra_paper_count', 0)

            email += f"""{i}. **{name}**
   - {icra_count} ICRA publication{'s' if icra_count != 1 else ''}
   - Recent work: *"{paper_title}"*
   - Strong fit for our foundation models and end-to-end learning initiatives

"""

        email += f"""
### Why These Candidates Stand Out:

- ✅ **Proven Research Track Record:** All have published at ICRA, validating their expertise through peer review at a top-tier conference
- ✅ **Relevant Expertise:** Their work spans foundation models, end-to-end learning, and robotic manipulation—directly aligned with our {team_name} roadmap
- ✅ **Active in Field:** Recent publications ({year_range}) show they're working on current problems, not legacy approaches
- ✅ **Publication + Implementation:** ICRA researchers typically have both theoretical knowledge and hands-on robotics experience

### Recommended Next Steps:

1. **Review profiles** (links in detailed summary above)
2. **Prioritize outreach** to these 3 candidates given their strong alignment
3. **Schedule initial screenings** to assess interest and availability
4. **Technical deep-dive** on their ICRA papers to identify conversation starters

I believe any of these candidates would be strong additions to the team. Their combination of robotics domain expertise and modern ML techniques is exactly what we need to accelerate our humanoid robotics capabilities.

**Would you like me to:**
- Draft personalized outreach emails?
- Set up preliminary screens?
- Source additional candidates in related areas?

Let me know your thoughts and preferred next steps.

Best regards,
[Your Name]
[Your Title]

---

**Attachments:**
- Full candidate profiles (JSON)
- ICRA paper summaries
- ArXiv links to recent publications

---
"""

        return email

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
