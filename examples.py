"""
Example: Using the API Integration Framework

This example demonstrates how to use the AI Talent Sourcing Agent
to discover candidates across multiple platforms.
"""

import json
from src.sourcing_agent import SourcingAgent

def example_basic_search():
    """Example 1: Basic candidate search."""
    print("=" * 60)
    print("Example 1: Basic Candidate Search")
    print("=" * 60)
    
    agent = SourcingAgent(config_file="config.yaml")
    
    # Search for computer vision engineers
    results = agent.search_candidates(
        query="computer vision deep learning",
        platforms=['github', 'arxiv']
    )
    
    # Display results
    total_found = sum(len(candidates) for candidates in results.values())
    print(f"\nTotal candidates found: {total_found}")
    
    for platform, candidates in results.items():
        print(f"\n{platform.upper()} candidates:")
        for candidate in candidates[:3]:
            print(f"  - {candidate.get('name')} ({candidate.get('id')})")

def example_github_search():
    """Example 2: GitHub-specific search."""
    print("\n" + "=" * 60)
    print("Example 2: GitHub Search")
    print("=" * 60)
    
    agent = SourcingAgent()
    
    # Search GitHub for ML engineers
    github_results = agent.search_candidates(
        query="pytorch tensorflow machine learning",
        platforms=['github']
    )
    
    if github_results.get('github'):
        print(f"\nFound {len(github_results['github'])} GitHub users")
        
        # Get details for first candidate
        first_candidate = github_results['github'][0]
        candidate_id = first_candidate.get('id')
        
        print(f"\nFetching details for: {first_candidate.get('name')}...")
        details = agent.get_candidate_details('github', candidate_id)
        
        if details:
            print(json.dumps(details, indent=2)[:500] + "...")

def example_arxiv_search():
    """Example 3: ArXiv research paper search."""
    print("\n" + "=" * 60)
    print("Example 3: ArXiv Search")
    print("=" * 60)
    
    agent = SourcingAgent()
    
    # Search ArXiv for AI researchers
    arxiv_results = agent.search_candidates(
        query="transformer neural networks attention",
        platforms=['arxiv']
    )
    
    if arxiv_results.get('arxiv'):
        print(f"\nFound {len(arxiv_results['arxiv'])} researchers")
        
        # Get details for first researcher
        first_researcher = arxiv_results['arxiv'][0]
        researcher_name = first_researcher.get('name')
        
        print(f"\nFetching details for: {researcher_name}...")
        details = agent.get_candidate_details('arxiv', researcher_name)
        
        if details.get('papers'):
            print(f"Recent papers by {researcher_name}:")
            for paper in details.get('papers', [])[:2]:
                print(f"  - {paper.get('title')}")

def example_export_results():
    """Example 4: Export candidates to JSON."""
    print("\n" + "=" * 60)
    print("Example 4: Export Results")
    print("=" * 60)
    
    agent = SourcingAgent()
    
    # Search multiple platforms
    results = agent.search_candidates(
        query="ai machine learning",
        platforms=['github', 'arxiv']
    )
    
    # Export results
    output_file = "discovered_candidates.json"
    agent.export_candidates(output_file)
    
    print(f"\nExported {len(agent.candidates)} candidates to {output_file}")

def example_track_papers():
    """Example 5: Track latest papers relevant to the team."""
    print("\n" + "=" * 60)
    print("Example 5: Track Latest Papers")
    print("=" * 60)
    
    agent = SourcingAgent()
    
    # Track latest papers for team keywords
    papers = agent.track_latest_papers(max_results=5)
    
    print(f"\nFound {len(papers)} latest relevant papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.get('title')}")
        print(f"   Authors: {', '.join(paper.get('authors', []))}")
        print(f"   Published: {paper.get('published')}")
        print(f"   ArXiv ID: {paper.get('arxiv_id')}")
        print(f"   URL: {paper.get('abs_url')}")

def example_emerging_talent():
    """Example 6: Find emerging AI talent."""
    print("\n" + "=" * 60)
    print("Example 6: Find Emerging Talent")
    print("=" * 60)
    
    agent = SourcingAgent()
    
    # Find emerging talent in specific research areas
    research_areas = ["computer vision", "natural language processing", "reinforcement learning"]
    talent = agent.find_emerging_talent(research_areas, max_results=5)
    
    print(f"\nFound {len(talent)} emerging talent candidates:")
    for i, candidate in enumerate(talent, 1):
        print(f"\n{i}. {candidate.get('name')}")
        print(f"   Platform: {candidate.get('platform')}")
        if candidate.get('recent_paper'):
            print(f"   Recent Paper: {candidate['recent_paper'].get('title')}")
            print(f"   Published: {candidate['recent_paper'].get('published')}")
        print(f"   Research Interests: {', '.join(candidate.get('research_interests', []))}")

if __name__ == "__main__":
    # Run examples (uncomment as needed)
    
    try:
        example_basic_search()
        example_github_search()
        example_arxiv_search()
        example_export_results()
        example_track_papers()
        example_emerging_talent()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
    
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure to:")
        print("1. Set GITHUB_TOKEN in .env for GitHub searches")
        print("2. Run: pip install -r requirements.txt")
        print("3. Configure API credentials in .env")
