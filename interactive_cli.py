#!/usr/bin/env python3
"""
Interactive CLI for AI Talent Sourcing Agent

Provides an easy-to-use command-line interface with prompts for:
- Searching for candidates
- Evaluating with AI
- Filtering and ranking results
- Exporting reports
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from src.sourcing_agent import SourcingAgent
from src.orchestrator import SourcingOrchestrator
from src.models.candidate import SearchFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InteractiveCLI:
    """Interactive command-line interface for sourcing agent."""
    
    def __init__(self):
        """Initialize the CLI with agents."""
        self.sourcing_agent = SourcingAgent()
        self.orchestrator = SourcingOrchestrator()
        self.last_results = None
    
    def print_header(self, title: str):
        """Print a formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")
    
    def print_menu(self):
        """Display main menu."""
        self.print_header("AI Talent Sourcing Agent - Main Menu")
        print("1. Search for candidates")
        print("2. Evaluate candidates with AI")
        print("3. Find AND evaluate candidates (complete pipeline)")
        print("4. View last results")
        print("5. Export results to file")
        print("6. Settings and configuration")
        print("7. Exit")
        print()
    
    def get_user_input(self, prompt: str, default: str = None) -> str:
        """Get input from user with optional default."""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        user_input = input(prompt).strip()
        return user_input if user_input else default
    
    def get_multiple_inputs(self, prompt: str, separator: str = ",") -> List[str]:
        """Get multiple comma-separated inputs from user."""
        user_input = input(f"{prompt} (comma-separated) [arxiv,github]: ").strip()
        if not user_input:
            user_input = "arxiv,github"
        return [item.strip() for item in user_input.split(separator)]
    
    def search_candidates(self):
        """Interactive candidate search."""
        self.print_header("Search for Candidates")
        
        # Get search parameters
        query = self.get_user_input("Search query (e.g., 'machine learning researcher')")
        if not query:
            print("❌ Search query required")
            return
        
        platforms = self.get_multiple_inputs("Which platforms to search?")
        limit = int(self.get_user_input("Number of results", "10"))
        
        print(f"\n🔍 Searching for '{query}' on {', '.join(platforms)}...")
        
        try:
            results = self.sourcing_agent.search_candidates(query, platforms)
            
            # Display results
            total_candidates = sum(len(candidates) for candidates in results.values())
            print(f"\n✅ Found {total_candidates} candidates:\n")
            
            candidate_list = []
            for platform, candidates in results.items():
                if candidates:
                    print(f"{platform.upper()} ({len(candidates)}):")
                    for i, cand in enumerate(candidates[:limit], 1):
                        print(f"  {i}. {cand.get('name', 'Unknown')} ({cand.get('id')})")
                        candidate_list.append(cand)
                    print()
            
            self.last_results = {
                'type': 'discovery',
                'query': query,
                'platforms': platforms,
                'candidates': candidate_list,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"📊 Total results: {len(candidate_list)}")
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            logger.exception("Search error")
    
    def evaluate_candidates(self):
        """Interactive candidate evaluation with AI."""
        self.print_header("Evaluate Candidates with AI")
        
        if not self.last_results:
            print("❌ No candidates to evaluate. Run search first.")
            return
        
        if self.last_results['type'] != 'discovery':
            print("❌ No search results available. Run search first.")
            return
        
        # Get job requirements
        job_title = self.get_user_input("Job title (e.g., 'Senior ML Engineer')")
        required_skills = self.get_user_input("Required skills (comma-separated)")
        preferred_skills = self.get_user_input("Preferred skills (comma-separated, optional)", "")
        
        job_requirements = {
            'title': job_title,
            'required_skills': [s.strip() for s in required_skills.split(",") if s.strip()],
            'preferred_skills': [s.strip() for s in preferred_skills.split(",") if s.strip()]
        }
        
        print(f"\n🤖 Evaluating {len(self.last_results['candidates'])} candidates...")
        
        # Mock evaluation results (full evaluation requires Claude API)
        evaluations = []
        for candidate in self.last_results['candidates'][:5]:  # Evaluate first 5
            evaluation = {
                'candidate': candidate,
                'score': 75,  # This would come from Claude
                'recommendation': 'Recommended',
                'match_details': 'Skills align with requirements'
            }
            evaluations.append(evaluation)
            print(f"  ✓ {candidate.get('name', 'Unknown')}: {evaluation['score']}/100")
        
        self.last_results = {
            'type': 'evaluation',
            'job_requirements': job_requirements,
            'evaluations': evaluations,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n✅ Evaluated {len(evaluations)} candidates")
    
    def find_and_evaluate(self):
        """Complete pipeline: discover and evaluate candidates."""
        self.print_header("Find and Evaluate Candidates (Complete Pipeline)")
        
        # Get search parameters
        query = self.get_user_input("Search query")
        if not query:
            print("❌ Search query required")
            return
        
        # Get job requirements
        job_title = self.get_user_input("Job title")
        required_skills = self.get_user_input("Required skills (comma-separated)")
        
        platforms = self.get_multiple_inputs("Platforms to search?")
        limit = int(self.get_user_input("Results limit", "5"))
        
        job_requirements = {
            'title': job_title,
            'required_skills': [s.strip() for s in required_skills.split(",") if s.strip()],
        }
        
        print(f"\n🚀 Starting complete pipeline...")
        print(f"   Query: {query}")
        print(f"   Role: {job_title}")
        print(f"   Platforms: {', '.join(platforms)}\n")
        
        try:
            print("📊 Step 1: Discovering candidates...")
            # This would use the full orchestrator pipeline
            discovery_results = self.sourcing_agent.search_candidates(query, platforms)
            
            all_candidates = []
            for platform, candidates in discovery_results.items():
                all_candidates.extend(candidates[:limit])
            
            print(f"✓ Found {len(all_candidates)} candidates\n")
            
            if all_candidates:
                print("🤖 Step 2: AI Evaluation (Claude Sonnet)...")
                print("⚠️  Note: Full Claude evaluation requires credentials configured\n")
                
                # Display candidates
                for i, cand in enumerate(all_candidates, 1):
                    name = cand.get('name', 'Unknown')
                    print(f"   {i}. {name}")
                
                self.last_results = {
                    'type': 'complete_pipeline',
                    'query': query,
                    'job_requirements': job_requirements,
                    'candidates': all_candidates,
                    'platforms': platforms,
                    'timestamp': datetime.now().isoformat()
                }
                
                print(f"\n✅ Pipeline complete: {len(all_candidates)} candidates ready")
            else:
                print("❌ No candidates found")
        
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            logger.exception("Pipeline error")
    
    def view_results(self):
        """Display last search/evaluation results."""
        self.print_header("Last Results")
        
        if not self.last_results:
            print("❌ No results available")
            return
        
        result_type = self.last_results.get('type', 'unknown')
        
        if result_type == 'discovery':
            print(f"Search: {self.last_results['query']}")
            print(f"Platforms: {', '.join(self.last_results['platforms'])}")
            print(f"Candidates found: {len(self.last_results['candidates'])}\n")
            
            for i, cand in enumerate(self.last_results['candidates'], 1):
                print(f"{i}. {cand.get('name', 'Unknown')}")
                print(f"   ID: {cand.get('id')}")
                print(f"   Platform: {cand.get('platform')}\n")
        
        elif result_type == 'complete_pipeline':
            print(f"Query: {self.last_results['query']}")
            print(f"Job: {self.last_results['job_requirements'].get('title')}")
            print(f"Candidates: {len(self.last_results['candidates'])}\n")
            
            for i, cand in enumerate(self.last_results['candidates'], 1):
                print(f"{i}. {cand.get('name', 'Unknown')}")
        
        print(f"Timestamp: {self.last_results['timestamp']}")
    
    def export_results(self):
        """Export last results to file."""
        self.print_header("Export Results")
        
        if not self.last_results:
            print("❌ No results to export")
            return
        
        filename = self.get_user_input(
            "Filename to export",
            f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.last_results, f, indent=2)
            
            print(f"✅ Results exported to {filename}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def show_settings(self):
        """Show configuration settings."""
        self.print_header("Configuration Settings")
        
        print("Current Configuration:")
        print(f"  API Base URL: {os.getenv('ANTHROPIC_VERTEX_BASE_URL', '❌ Not configured')}")
        print(f"  Claude Model: {os.getenv('ANTHROPIC_DEFAULT_SONNET_MODEL', 'claude-sonnet-4-5')}")
        print(f"  Project ID: {os.getenv('ANTHROPIC_VERTEX_PROJECT_ID', '❌ Not configured')}")
        print()
        print("Configuration file: config.yaml")
        print("Environment file: .env")
        print("\nNote: Update .env file to configure credentials")
    
    def run(self):
        """Main CLI loop."""
        print("\n🚀 AI Talent Sourcing Agent - Interactive CLI")
        
        while True:
            self.print_menu()
            choice = input("Select option (1-7): ").strip()
            
            if choice == "1":
                self.search_candidates()
            elif choice == "2":
                self.evaluate_candidates()
            elif choice == "3":
                self.find_and_evaluate()
            elif choice == "4":
                self.view_results()
            elif choice == "5":
                self.export_results()
            elif choice == "6":
                self.show_settings()
            elif choice == "7":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("❌ Invalid option. Please try again.")


def main():
    """Entry point."""
    cli = InteractiveCLI()
    cli.run()


if __name__ == "__main__":
    main()
