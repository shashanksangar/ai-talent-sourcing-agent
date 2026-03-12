#!/usr/bin/env python3
"""
Example: Finding ICRA Authors for Tesla Optimus Team

This example demonstrates how to:
1. Search for ICRA 2025 authors working on Foundation Models
2. Search for ICRA authors working on End-to-End Learning
3. Evaluate ICRA authors with AI prioritization
4. Export results for recruitment

Perfect for finding robotics talent with proven track records at top-tier conferences.
"""

import json
from src.sourcing_agent import SourcingAgent
from src.orchestrator import SourcingOrchestrator


def example_icra_2025_foundation_models():
    """Example 1: Find ICRA 2025 authors working on Foundation Models."""
    print("=" * 80)
    print("Example 1: ICRA 2025 Authors - Foundation Models for Robotics")
    print("=" * 80)

    agent = SourcingAgent(config_file="config.yaml")

    # Search for ICRA 2025 authors working on foundation models
    authors = agent.find_icra_authors(
        research_area="foundation models",
        year=2025,
        max_results=10
    )

    print(f"\n✅ Found {len(authors)} ICRA 2025 authors working on Foundation Models\n")

    # Display results
    for i, author in enumerate(authors[:5], 1):
        print(f"{i}. {author.get('name')}")
        print(f"   📄 ICRA Papers: {author.get('icra_paper_count')}")
        print(f"   📅 ICRA Years: {', '.join(map(str, author.get('icra_years', [])))}")

        if author.get('recent_icra_paper'):
            paper = author['recent_icra_paper']
            print(f"   📝 Recent: \"{paper.get('title')}\" (ICRA {paper.get('conference_year')})")

        print(f"   🔗 ArXiv: {author.get('platform_url')}\n")

    return authors


def example_icra_end_to_end_learning():
    """Example 2: Find ICRA authors working on End-to-End Learning."""
    print("=" * 80)
    print("Example 2: ICRA Authors - End-to-End Learning for Robotics")
    print("=" * 80)

    agent = SourcingAgent(config_file="config.yaml")

    # Search for ICRA authors working on end-to-end learning (any recent year)
    authors = agent.find_icra_authors(
        research_area="end-to-end learning manipulation",
        year=None,  # Search all years
        max_results=15
    )

    print(f"\n✅ Found {len(authors)} ICRA authors working on End-to-End Learning\n")

    # Group by year
    by_year = {}
    for author in authors:
        for year in author.get('icra_years', []):
            if year not in by_year:
                by_year[year] = []
            by_year[year].append(author)

    print("Authors by ICRA Year:")
    for year in sorted(by_year.keys(), reverse=True):
        print(f"  ICRA {year}: {len(by_year[year])} authors")

    return authors


def example_icra_with_ai_evaluation():
    """Example 3: Find and evaluate ICRA authors with AI prioritization."""
    print("\n" + "=" * 80)
    print("Example 3: ICRA Authors + AI Evaluation (Tesla Optimus Prioritization)")
    print("=" * 80)

    orchestrator = SourcingOrchestrator(config_file="config.yaml")

    # Define Tesla Optimus job requirements
    job_requirements = {
        "title": "Robotics ML Engineer - Tesla Optimus",
        "team": "Tesla Optimus (Humanoid Robot)",
        "required_skills": [
            "Foundation Models",
            "End-to-End Learning",
            "Robot Manipulation",
            "Imitation Learning",
            "Vision-Language-Action Models",
            "PyTorch",
            "Sim-to-Real Transfer"
        ],
        "domain": "Embodied AI / Robotics",
        "seniority_level": "Senior / Staff",
        "min_experience_years": 3,
        "description": """
        We're looking for researchers and engineers to build foundation models for Tesla Optimus,
        our humanoid robot. You'll work on end-to-end learning systems that enable Optimus to
        perform complex manipulation tasks in real-world environments.

        Ideal candidates have published at top robotics conferences (ICRA, RSS, CoRL) and have
        experience with large-scale vision-language-action models for robotics.
        """
    }

    print("\n🔍 Searching for ICRA 2025 authors working on Foundation Models...")

    # Get ICRA authors
    agent = SourcingAgent(config_file="config.yaml")
    icra_authors = agent.find_icra_authors(
        research_area="foundation models imitation learning",
        year=2025,
        max_results=10
    )

    if not icra_authors:
        print("\n⚠️  No ICRA 2025 authors found. Trying without year filter...")
        icra_authors = agent.find_icra_authors(
            research_area="foundation models imitation learning",
            year=None,
            max_results=10
        )

    print(f"✅ Found {len(icra_authors)} ICRA authors\n")

    # Evaluate with AI (prioritizes ICRA authors)
    print("🤖 Evaluating candidates with Claude AI (ICRA prioritization enabled)...\n")

    evaluations = []
    for candidate in icra_authors[:5]:  # Evaluate top 5
        try:
            evaluation = orchestrator.ai_evaluator.evaluate_candidate(
                candidate_profile=candidate,
                job_requirements=job_requirements,
                context="ICRA author with robotics expertise - priority candidate for Tesla Optimus"
            )
            evaluations.append(evaluation)

            print(f"📊 {evaluation.get('candidate_name')}")
            print(f"   Score: {evaluation.get('match_score')}/100")
            print(f"   Recommendation: {evaluation.get('recommendation')}")
            print(f"   ICRA Papers: {candidate.get('icra_paper_count')}")
            print()

        except Exception as e:
            print(f"⚠️  Error evaluating {candidate.get('name')}: {e}\n")

    # Sort by score
    evaluations.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    print("\n" + "=" * 80)
    print("🏆 TOP CANDIDATES (Ranked by AI Score)")
    print("=" * 80)

    for i, eval_result in enumerate(evaluations[:3], 1):
        print(f"\n{i}. {eval_result.get('candidate_name')} - {eval_result.get('match_score')}/100")
        print(f"   {eval_result.get('recommendation')}")

    return evaluations


def example_export_icra_results():
    """Example 4: Search and export ICRA authors to JSON."""
    print("\n" + "=" * 80)
    print("Example 4: Export ICRA 2025 Authors to JSON")
    print("=" * 80)

    agent = SourcingAgent(config_file="config.yaml")

    # Search for multiple research areas
    research_areas = [
        "foundation models",
        "end-to-end learning",
        "imitation learning",
        "vision language action"
    ]

    all_authors = []
    for area in research_areas:
        print(f"\n🔍 Searching ICRA 2025 for: {area}")
        authors = agent.find_icra_authors(
            research_area=area,
            year=2025,
            max_results=5
        )
        all_authors.extend(authors)
        print(f"   Found: {len(authors)} authors")

    # Deduplicate by name
    unique_authors = {author['name']: author for author in all_authors}
    unique_authors_list = list(unique_authors.values())

    print(f"\n✅ Total unique ICRA 2025 authors: {len(unique_authors_list)}")

    # Export to JSON
    output_file = "icra_2025_authors.json"
    export_data = {
        "search_type": "icra_authors",
        "conference": "ICRA 2025",
        "research_areas": research_areas,
        "total_authors": len(unique_authors_list),
        "authors": unique_authors_list,
        "timestamp": str(__import__('datetime').datetime.now().isoformat())
    }

    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"💾 Exported to: {output_file}")

    return unique_authors_list


def example_quick_icra_scan():
    """Example 5: Quick ICRA scan for specific topics."""
    print("\n" + "=" * 80)
    print("Example 5: Quick ICRA Scan - Tesla Optimus Relevant Topics")
    print("=" * 80)

    agent = SourcingAgent(config_file="config.yaml")

    # Topics relevant to Tesla Optimus
    optimus_topics = [
        ("foundation models", 2025),
        ("end-to-end learning", 2025),
        ("humanoid robot", 2024),
        ("manipulation learning", 2024),
        ("vision language action", 2025)
    ]

    results_summary = []
    all_authors = []

    for topic, year in optimus_topics:
        authors = agent.find_icra_authors(
            research_area=topic,
            year=year,
            max_results=3
        )

        all_authors.extend(authors)

        results_summary.append({
            "topic": topic,
            "year": year,
            "author_count": len(authors),
            "top_authors": [a.get('name') for a in authors[:3]]
        })

        print(f"\n📌 {topic.upper()} (ICRA {year}): {len(authors)} authors")
        for author in authors[:3]:
            print(f"   • {author.get('name')} ({author.get('icra_paper_count')} ICRA papers)")

    # Deduplicate and sort
    unique_authors = {a['name']: a for a in all_authors}
    unique_list = list(unique_authors.values())
    unique_list.sort(key=lambda x: x.get('icra_paper_count', 0), reverse=True)

    print("\n" + "=" * 80)
    print("Summary:")
    print(f"Total unique candidates discovered: {len(unique_list)}")
    print("=" * 80)

    return unique_list


def example_generate_hm_summary():
    """Example 6: Generate HM Summary Report."""
    print("\n" + "=" * 80)
    print("Example 6: Generate Hiring Manager Summary Report")
    print("=" * 80)

    agent = SourcingAgent(config_file="config.yaml")

    # Search for candidates
    print("\n🔍 Searching ICRA 2025 for Foundation Models + End-to-End Learning...")

    fm_authors = agent.find_icra_authors("foundation models", year=2025, max_results=5)
    e2e_authors = agent.find_icra_authors("end-to-end learning", year=2025, max_results=5)

    # Combine and deduplicate
    all_authors = fm_authors + e2e_authors
    unique_authors = {a['name']: a for a in all_authors}
    unique_list = list(unique_authors.values())
    unique_list.sort(key=lambda x: x.get('icra_paper_count', 0), reverse=True)

    print(f"✅ Found {len(unique_list)} unique ICRA authors")

    if unique_list:
        # Generate HM Summary
        print("\n📝 Generating Hiring Manager Summary with top 3 candidates...")

        output_file = agent.generate_hm_summary(
            candidates=unique_list,
            job_title="Robotics ML Engineer - Core Autonomy",
            team_name="Core Autonomy / Tesla Optimus",
            output_file="HM_Summary_Example.md",
            top_n=3
        )

        print(f"\n✅ HM Summary generated: {output_file}")
        print("\n📋 Summary includes:")
        print("   • Top 3 candidates with ICRA papers")
        print("   • 2-sentence fit summaries")
        print("   • Drafted email to hiring manager")
        print("   • Next steps and recommendations")

        # Show preview
        with open(output_file, 'r') as f:
            preview = f.read()[:800]
            print("\n" + "=" * 80)
            print("Preview of HM_Summary_Example.md:")
            print("=" * 80)
            print(preview + "\n...")
            print("=" * 80)

    else:
        print("\n⚠️  No candidates found. Try broader search terms or remove year filter.")

    return unique_list


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🤖 ICRA Author Search for Tesla Optimus Recruitment")
    print("=" * 80)
    print("\nThis script demonstrates how to find ICRA authors working on:")
    print("  • Foundation Models for Robotics")
    print("  • End-to-End Learning")
    print("  • Embodied AI and Robot Manipulation")
    print("\nWith AI-powered evaluation that prioritizes ICRA publications.\n")

    try:
        # Run examples
        print("\n🚀 Running ICRA search examples...\n")

        # Example 1: ICRA 2025 Foundation Models
        authors_fm = example_icra_2025_foundation_models()

        # Example 2: End-to-End Learning
        authors_e2e = example_icra_end_to_end_learning()

        # Example 3: AI Evaluation (requires Claude API)
        try:
            evaluations = example_icra_with_ai_evaluation()
        except Exception as e:
            print(f"\n⚠️  Skipping AI evaluation (requires Claude API): {e}")

        # Example 4: Export results
        unique_authors = example_export_icra_results()

        # Example 5: Quick scan
        unique_authors = example_quick_icra_scan()

        # Example 6: Generate HM Summary
        example_generate_hm_summary()

        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        print("\n📁 Check the following files:")
        print("  • icra_2025_authors.json - Exported ICRA author profiles")
        print("  • discovered_candidates.json - All discovered candidates")
        print("  • HM_Summary_Example.md - Hiring manager summary report")
        print("\n💡 Next steps:")
        print("  1. Review the candidate profiles")
        print("  2. Review HM_Summary_Example.md")
        print("  3. Send drafted email to hiring manager")
        print("  4. Use the AI evaluator to rank candidates")
        print("  5. Export top candidates for outreach")
        print("  6. Integrate with your ATS/recruitment system")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Ensure .env file has ANTHROPIC credentials")
        print("  2. Check internet connectivity for ArXiv API")
        print("  3. Verify config.yaml exists")
        print(f"\n📚 Error details: {type(e).__name__}: {e}")
