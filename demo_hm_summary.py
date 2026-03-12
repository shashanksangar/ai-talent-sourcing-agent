#!/usr/bin/env python3
"""
Demo: Generate HM Summary for ICRA 2025 Authors

This script demonstrates the new HM summary generation feature.
It searches for ICRA authors and creates a professional markdown report
with the top 3 candidates and a drafted email for the hiring manager.
"""

from src.sourcing_agent import SourcingAgent


def main():
    print("=" * 70)
    print("🎯 ICRA Author Search + HM Summary Generation Demo")
    print("=" * 70)

    # Initialize agent
    agent = SourcingAgent(config_file="config.yaml")

    # Step 1: Search for ICRA authors
    print("\n📚 Step 1: Searching for ICRA 2025 Authors")
    print("-" * 70)

    print("\n🔍 Searching: Foundation Models...")
    fm_authors = agent.find_icra_authors(
        research_area="foundation models",
        year=2025,
        max_results=10
    )

    print(f"\n🔍 Searching: End-to-End Learning...")
    e2e_authors = agent.find_icra_authors(
        research_area="end-to-end learning manipulation",
        year=2025,
        max_results=10
    )

    # Combine and deduplicate
    all_authors = fm_authors + e2e_authors
    unique_authors = {}

    for candidate in all_authors:
        name = candidate.get('name')
        if name not in unique_authors:
            unique_authors[name] = candidate
        else:
            # Merge ICRA papers if candidate appears in both searches
            existing = unique_authors[name]
            existing_papers = set(p.get('arxiv_id') for p in existing.get('icra_papers', []))
            for paper in candidate.get('icra_papers', []):
                if paper.get('arxiv_id') not in existing_papers:
                    existing['icra_papers'].append(paper)
            existing['icra_paper_count'] = len(existing['icra_papers'])

    unique_list = list(unique_authors.values())
    # Sort by ICRA paper count (most prolific first)
    unique_list.sort(key=lambda x: x.get('icra_paper_count', 0), reverse=True)

    print(f"\n✅ Found {len(unique_list)} unique ICRA authors")

    if not unique_list:
        print("\n⚠️  No ICRA 2025 authors found.")
        print("\n💡 Try:")
        print("   1. Remove year filter (set year=None)")
        print("   2. Use broader search terms")
        print("   3. Search ICRA 2024 or 2023")
        return

    # Show preview of top candidates
    print("\n📊 Top 5 Candidates by ICRA Publication Count:")
    print("-" * 70)
    for i, author in enumerate(unique_list[:5], 1):
        name = author.get('name')
        count = author.get('icra_paper_count', 0)
        recent = author.get('recent_icra_paper', {}).get('title', 'N/A')
        print(f"{i}. {name}")
        print(f"   ICRA Papers: {count} | Recent: {recent[:60]}...")

    # Step 2: Generate HM Summary
    print("\n" + "=" * 70)
    print("📝 Step 2: Generating Hiring Manager Summary")
    print("-" * 70)

    output_file = agent.generate_hm_summary(
        candidates=unique_list,
        job_title="Robotics ML Engineer - Core Autonomy",
        team_name="Core Autonomy / Tesla Optimus",
        output_file="HM_Summary.md",
        top_n=3
    )

    # Show what was generated
    print("\n" + "=" * 70)
    print("✅ SUCCESS!")
    print("=" * 70)
    print(f"\n📄 Generated File: {output_file}")
    print("\n📋 The HM Summary includes:")
    print("   ✓ Top 3 candidates with ICRA credentials")
    print("   ✓ ICRA paper titles and years")
    print("   ✓ 2-sentence fit summaries for Core Autonomy team")
    print("   ✓ Research interests and profile links")
    print("   ✓ Drafted email ready to send to hiring manager")
    print("   ✓ Recommended next steps")

    print("\n" + "=" * 70)
    print("🚀 Next Steps:")
    print("=" * 70)
    print("1. Open and review: HM_Summary.md")
    print("2. Customize the drafted email with HM name")
    print("3. Send to hiring manager")
    print("4. Schedule candidate screens")
    print("\n💡 Tip: You can also export full data with:")
    print("   agent.export_candidates('candidates.json')")

    # Show preview of generated file
    print("\n" + "=" * 70)
    print("📖 Preview of HM_Summary.md:")
    print("=" * 70)

    with open(output_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        preview_lines = lines[:30]  # Show first 30 lines
        print('\n'.join(preview_lines))
        if len(lines) > 30:
            print(f"\n... ({len(lines) - 30} more lines)")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check config.yaml exists")
        print("   2. Verify internet connection (ArXiv API)")
        print("   3. Try broader search terms or remove year filter")
