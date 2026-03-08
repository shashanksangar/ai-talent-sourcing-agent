"""
Sourcing Orchestrator

Combines API integrations with AI evaluation for end-to-end recruiting.
"""

import json
import logging
from typing import Dict, Any, List
from src.sourcing_agent import SourcingAgent
from src.ai_evaluator import AIEvaluator
from src.utils.config import APIConfig

logger = logging.getLogger(__name__)

class SourcingOrchestrator:
    """
    End-to-end orchestrator that:
    1. Discovers candidates via APIs
    2. Evaluates them with Claude
    3. Ranks and ranks them by fit
    4. Generates personalized outreach context
    """
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize the orchestrator.
        
        Args:
            config_file: Configuration file path
        """
        self.config = APIConfig(config_file)
        self.sourcing_agent = SourcingAgent(config_file)
        self.ai_evaluator = AIEvaluator(self.config.config)
    
    def find_and_evaluate_candidates(
        self,
        search_query: str,
        job_requirements: Dict[str, Any],
        platforms: List[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Complete pipeline: search, evaluate, and rank candidates.
        
        Args:
            search_query: Query for candidate discovery
            job_requirements: Job posting details
            platforms: Platforms to search
            limit: Max candidates to evaluate
        
        Returns:
            Ranked list of evaluated candidates
        """
        platforms = platforms or ['github', 'arxiv']
        
        logger.info(f"Starting candidate discovery and evaluation for: {job_requirements.get('title')}")
        
        # Phase 1: Discover candidates
        logger.info(f"Phase 1: Discovering candidates...")
        search_results = self.sourcing_agent.search_candidates(search_query, platforms)
        
        # Collect all candidates
        all_candidates = []
        for platform, candidates in search_results.items():
            all_candidates.extend(candidates)
        
        logger.info(f"Discovered {len(all_candidates)} candidates total")
        
        # Phase 2: Evaluate candidates with Claude
        logger.info(f"Phase 2: Evaluating top {min(limit, len(all_candidates))} candidates...")
        
        evaluations = []
        for i, candidate in enumerate(all_candidates[:limit], 1):
            logger.info(f"  Evaluating {i}/{min(limit, len(all_candidates))}: {candidate.get('name')}")
            
            evaluation = self.ai_evaluator.evaluate_candidate(
                candidate,
                job_requirements
            )
            evaluations.append(evaluation)
        
        # Phase 3: Generate outreach context for top candidates
        logger.info(f"Phase 3: Generating personalized outreach...")
        
        # Sort by match score
        evaluations.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        # Generate outreach for top 5
        for evaluation in evaluations[:5]:
            candidate_id = evaluation.get('candidate_id')
            candidate = next(
                (c for c in all_candidates if c.get('id') == candidate_id),
                {}
            )
            
            if candidate:
                outreach_context = self.ai_evaluator.generate_outreach_context(
                    candidate,
                    evaluation
                )
                evaluation['outreach_context'] = outreach_context
        
        logger.info("Candidate evaluation complete!")
        return evaluations
    
    def export_findings(
        self,
        evaluations: List[Dict[str, Any]],
        output_file: str = "evaluated_candidates.json"
    ):
        """
        Export evaluation results to file.
        
        Args:
            evaluations: List of evaluated candidates
            output_file: Output file path
        """
        export_data = {
            "total_evaluated": len(evaluations),
            "candidates": evaluations,
            "summary": {
                "highly_recommended": len([e for e in evaluations if e.get('recommendation') == 'Highly Recommended']),
                "recommended": len([e for e in evaluations if e.get('recommendation') == 'Recommended']),
                "maybe": len([e for e in evaluations if e.get('recommendation') == 'Maybe']),
                "pass": len([e for e in evaluations if e.get('recommendation') == 'Pass'])
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Results exported to {output_file}")
        return export_data
    
    def print_summary(self, evaluations: List[Dict[str, Any]]):
        """Print a summary of evaluation results."""
        print("\n" + "=" * 70)
        print("CANDIDATE EVALUATION SUMMARY")
        print("=" * 70)
        
        for i, eval_result in enumerate(evaluations[:10], 1):
            print(f"\n{i}. {eval_result.get('candidate_name')} - Score: {eval_result.get('match_score')}/100")
            print(f"   Recommendation: {eval_result.get('recommendation')}")
            print(f"   For: {eval_result.get('job_title')}")
            
            if eval_result.get('outreach_context'):
                print(f"   Outreach context available")
        
        print("\n" + "=" * 70)
        print(f"Total Evaluated: {len(evaluations)}")
        print("=" * 70)
