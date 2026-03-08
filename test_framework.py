#!/usr/bin/env python3
"""Quick test of the API Framework"""

from src.sourcing_agent import SourcingAgent

print("Testing AI Talent Sourcing Agent - API Framework")
print("=" * 60)

agent = SourcingAgent('config.yaml')

# Test ArXiv search (no auth required)
print("\nSearching ArXiv for 'transformer attention mechanism' researchers...")
print("-" * 60)

results = agent.search_candidates(
    query="transformer attention mechanism",
    platforms=['arxiv']
)

if results.get('arxiv'):
    arxiv_candidates = results['arxiv']
    print(f"\n✓ Found {len(arxiv_candidates)} researchers on ArXiv")
    print("\nTop 5 researchers:")
    for i, candidate in enumerate(arxiv_candidates[:5], 1):
        name = candidate.get('name', 'Unknown')
        paper = candidate.get('recent_paper', {})
        paper_title = paper.get('title', 'N/A')
        print(f"\n{i}. {name}")
        print(f"   Recent paper: {paper_title[:70]}...")
        if candidate.get('co_authors'):
            collab = ', '.join(candidate['co_authors'][:2])
            print(f"   Collaborators: {collab}")

print("\n" + "=" * 60)
print("✓ API Framework Test Complete!")
