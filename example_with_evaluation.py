#!/usr/bin/env python3
"""
Example: AI Talent Sourcing with Claude Evaluation

Demonstrates the complete pipeline:
1. Discover candidates via GitHub/ArXiv
2. Evaluate with Claude
3. Rank by fit
4. Generate personalized outreach context
"""

import json
import logging
from src.orchestrator import SourcingOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def example_sourcing_pipeline():
    """Run the complete sourcing and evaluation pipeline."""
    
    print("\n" + "=" * 70)
    print("AI TALENT SOURCING + CLAUDE EVALUATION PIPELINE")
    print("=" * 70)
    
    # Initialize orchestrator
    orchestrator = SourcingOrchestrator("config.yaml")
    
    # Define the job we're hiring for
    job_requirements = {
        "title": "AI Engineer, Computer Vision & Robotics",
        "team": "Tesla Autopilot Vision",
        "domain": "Computer Vision",
        "seniority_level": "Senior",
        "min_experience_years": 4,
        "required_skills": [
            "PyTorch",
            "Computer Vision",
            "Deep Learning",
            "Python",
            "Distributed Training"
        ],
        "description": """
Lead the development of cutting-edge computer vision systems for autonomous vehicles.
We're looking for AI engineers who:
- Have deep expertise in neural networks and deep learning
- Can work on large-scale distributed training
- Are passionate about autonomous systems
- Have published research or contributed to open-source projects
- Can innovate on hard problems
"""
    }
    
    # Search query for discovering candidates
    search_query = "computer vision deep learning autonomous driving transformers"
    
    print(f"\nJob: {job_requirements['title']}")
    print(f"Search Query: {search_query}")
    print("-" * 70)
    
    # Run the complete pipeline
    evaluations = orchestrator.find_and_evaluate_candidates(
        search_query=search_query,
        job_requirements=job_requirements,
        platforms=['arxiv'],  # Using ArXiv since GitHub requires auth
        limit=5  # Evaluate top 5 for demo
    )
    
    # Print summary
    orchestrator.print_summary(evaluations)
    
    # Show detailed results for top candidate
    if evaluations:
        top_candidate = evaluations[0]
        print("\n" + "=" * 70)
        print("TOP CANDIDATE - DETAILED EVALUATION")
        print("=" * 70)
        print(f"\nCandidate: {top_candidate.get('candidate_name')}")
        print(f"Match Score: {top_candidate.get('match_score')}/100")
        print(f"Recommendation: {top_candidate.get('recommendation')}")
        
        if top_candidate.get('evaluation_details'):
            print(f"\nEvaluation Details:")
            print(top_candidate['evaluation_details'][:500] + "...")
        
        if top_candidate.get('outreach_context'):
            print(f"\nPersonalized Outreach Context:")
            print(top_candidate['outreach_context'][:300] + "...")
    
    # Export results
    print("\n" + "-" * 70)
    export_file = "evaluated_candidates_example.json"
    results = orchestrator.export_findings(evaluations, export_file)
    print(f"\nResults Summary:")
    print(f"  Total Evaluated: {results['summary']}")
    print(f"  Export File: {export_file}")
    
    return evaluations

def example_direct_evaluation():
    """Example of directly evaluating a candidate without discovery."""
    
    print("\n" + "=" * 70)
    print("DIRECT CANDIDATE EVALUATION EXAMPLE")
    print("=" * 70)
    
    from src.ai_evaluator import AIEvaluator
    from src.utils.config import APIConfig
    
    config = APIConfig("config.yaml")
    evaluator = AIEvaluator(config.config)
    
    # Sample candidate profile
    candidate = {
        "id": "researcher_001",
        "name": "Dr. Jane Smith",
        "current_role": "ML Research Scientist",
        "experience_years": 6,
        "skills": ["PyTorch", "Computer Vision", "Deep Learning", "Python", "CUDA"],
        "research_interests": ["Vision Transformers", "Semantic Segmentation", "3D Vision"],
        "location": "San Francisco, CA",
        "company": "Tech Research Lab",
        "bio": "PhD in Computer Science with 6 years of research experience in computer vision and deep learning. Published 12 papers on vision transformers and object detection.",
        "publications": [
            {"title": "Efficient Vision Transformers for Real-Time Applications", "year": 2024},
            {"title": "3D Scene Understanding with GNNs", "year": 2023}
        ],
        "followers": 500
    }
    
    # Job requirement
    job = {
        "title": "Senior ML Engineer, Computer Vision",
        "team": "Vision Team",
        "domain": "Autonomous Driving",
        "seniority_level": "Senior",
        "min_experience_years": 4,
        "required_skills": ["PyTorch", "Computer Vision", "Deep Learning"],
        "description": "Lead computer vision systems for autonomous vehicles"
    }
    
    print(f"\nCandidate: {candidate['name']}")
    print(f"Job: {job['title']}")
    print("-" * 70)
    
    # Evaluate
    evaluation = evaluator.evaluate_candidate(candidate, job)
    
    print(f"\nMatch Score: {evaluation.get('match_score')}/100")
    print(f"Recommendation: {evaluation.get('recommendation')}")
    print(f"\nEvaluation:")
    print(evaluation.get('evaluation_details', 'No details available')[:400] + "...")
    
    # Generate outreach
    print(f"\nGenerating personalized outreach context...")
    outreach = evaluator.generate_outreach_context(candidate, evaluation)
    print(f"\nOutreach Context:")
    print(outreach[:300] + "...")
    
    return evaluation

if __name__ == "__main__":
    try:
        # Run example 1: Complete pipeline (requires Claude API configured)
        print("Running Example 1: AI Talent Sourcing Pipeline with Claude...")
        example_sourcing_pipeline()
        
        # Uncomment to run example 2: Direct evaluation
        # print("\n\nRunning Example 2: Direct Candidate Evaluation...")
        # example_direct_evaluation()
        
    except Exception as e:
        logger.error(f"Error running examples: {e}")
        print("\nNote: To use Claude evaluation features, ensure:")
        print("1. ANTHROPIC_VERTEX_BASE_URL is set in .env")
        print("2. ANTHROPIC_AUTH_TOKEN is set in .env")
        print("3. ANTHROPIC_VERTEX_PROJECT_ID is set in .env")
