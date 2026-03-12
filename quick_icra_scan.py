#!/usr/bin/env python3
"""
Quick ICRA 2025 Scan - Minimal Example

Simple script to find ICRA 2025 authors working on Foundation Models or End-to-End Learning.
Perfect for a quick scan without evaluation.
"""

from src.sourcing_agent import SourcingAgent
import json


def main():
    print("🔍 ICRA 2025 Author Scan for Tesla Optimus")
    print("=" * 60)

    # Initialize agent
    agent = SourcingAgent(config_file="config.yaml")

    # Search ICRA 2025 for Foundation Models
    print("\n1️⃣  Searching ICRA 2025: Foundation Models...")
    fm_authors = agent.find_icra_authors(
        research_area="foundation models",
        year=2025,
        max_results=10
    )

    print(f"   ✅ Found {len(fm_authors)} authors\n")
    for i, author in enumerate(fm_authors[:5], 1):
        print(f"   {i}. {author.get('name')}")
        print(f"      Papers: {author.get('icra_paper_count')} | "
              f"Recent: {author.get('recent_icra_paper', {}).get('title', 'N/A')[:60]}...")

    # Search ICRA 2025 for End-to-End Learning
    print("\n2️⃣  Searching ICRA 2025: End-to-End Learning...")
    e2e_authors = agent.find_icra_authors(
        research_area="end-to-end learning manipulation",
        year=2025,
        max_results=10
    )

    print(f"   ✅ Found {len(e2e_authors)} authors\n")
    for i, author in enumerate(e2e_authors[:5], 1):
        print(f"   {i}. {author.get('name')}")
        print(f"      Papers: {author.get('icra_paper_count')} | "
              f"Recent: {author.get('recent_icra_paper', {}).get('title', 'N/A')[:60]}...")

    # Combine and deduplicate all candidates
    all_candidates = fm_authors + e2e_authors
    unique_candidates = {}
    for candidate in all_candidates:
        name = candidate.get('name')
        if name not in unique_candidates:
            unique_candidates[name] = candidate
        else:
            # Merge ICRA papers if candidate appears in both searches
            existing = unique_candidates[name]
            existing_papers = set(p.get('arxiv_id') for p in existing.get('icra_papers', []))
            for paper in candidate.get('icra_papers', []):
                if paper.get('arxiv_id') not in existing_papers:
                    existing['icra_papers'].append(paper)
            existing['icra_paper_count'] = len(existing['icra_papers'])

    unique_list = list(unique_candidates.values())
    # Sort by ICRA paper count
    unique_list.sort(key=lambda x: x.get('icra_paper_count', 0), reverse=True)

    # Export all results
    print("\n💾 Exporting results...")
    agent.export_candidates("icra_2025_quick_scan.json")

    # Generate HM Summary
    print("\n📝 Generating Hiring Manager Summary...")
    agent.generate_hm_summary(
        candidates=unique_list,
        job_title="Robotics ML Engineer - Core Autonomy",
        team_name="Core Autonomy / Tesla Optimus",
        output_file="HM_Summary.md",
        top_n=3
    )

    print("\n" + "=" * 60)
    print(f"✅ Scan complete! Found {len(unique_list)} unique candidates")
    print("\n📁 Generated Files:")
    print("  • icra_2025_quick_scan.json - Full candidate data")
    print("  • HM_Summary.md - Top 3 candidates + drafted email")
    print("\n💡 Next: Review HM_Summary.md and send to hiring manager!")


if __name__ == "__main__":
    main()
