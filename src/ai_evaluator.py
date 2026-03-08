"""
AI Evaluation Module

Uses Claude to intelligently evaluate and analyze candidates.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class AIEvaluator:
    """
    Uses Claude to evaluate candidates based on job requirements
    and provide intelligent matching recommendations.
    """
    
    def __init__(self, api_config: Dict[str, Any] = None):
        """
        Initialize the AI evaluator.
        
        Args:
            api_config: Configuration with Anthropic API settings
        """
        self.config = api_config or {}
        
        # Initialize Anthropic client
        self.client = Anthropic(
            api_key=self.config.get('anthropic_auth_token'),
            base_url=self.config.get('anthropic_vertex_base_url')
        )
        
        self.model = self.config.get('model', 'claude-sonnet-4-5')
        self.temperature = self.config.get('temperature', 0.5)
        self.conversation_history = []
    
    def evaluate_candidate(
        self,
        candidate_profile: Dict[str, Any],
        job_requirements: Dict[str, Any],
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Evaluate a candidate's fit for a specific role.
        
        Args:
            candidate_profile: Candidate information
            job_requirements: Job posting details
            context: Additional context about the evaluation
        
        Returns:
            Evaluation results with score and reasoning
        """
        prompt = self._build_evaluation_prompt(candidate_profile, job_requirements, context)
        
        logger.info(f"Evaluating {candidate_profile.get('name')} for {job_requirements.get('title')}")
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                system=self._get_system_prompt(),
                messages=[{"role": "user", "content": prompt}]
            )
            
            evaluation_text = response.content[0].text
            evaluation = self._parse_evaluation(evaluation_text, candidate_profile, job_requirements)
            
            return evaluation
        
        except Exception as e:
            logger.error(f"Error evaluating candidate: {e}")
            return self._default_evaluation(candidate_profile, job_requirements)
    
    def compare_candidates(
        self,
        candidates: List[Dict[str, Any]],
        job_requirements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Compare multiple candidates and rank them by fit.
        
        Args:
            candidates: List of candidate profiles
            job_requirements: Job requirements
        
        Returns:
            Ranked list of candidates with scores
        """
        logger.info(f"Comparing {len(candidates)} candidates for {job_requirements.get('title')}")
        
        evaluations = []
        for candidate in candidates:
            evaluation = self.evaluate_candidate(candidate, job_requirements)
            evaluations.append(evaluation)
        
        # Sort by match score
        evaluations.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        return evaluations
    
    def generate_outreach_context(
        self,
        candidate_profile: Dict[str, Any],
        evaluation: Dict[str, Any]
    ) -> str:
        """
        Generate personalized outreach context based on evaluation.
        
        Args:
            candidate_profile: Candidate information
            evaluation: Evaluation results
        
        Returns:
            Outreach context and talking points
        """
        prompt = f"""
Based on this candidate evaluation, provide personalized outreach talking points:

Candidate: {candidate_profile.get('name')}
Research Interests: {', '.join(candidate_profile.get('research_interests', []))}

Evaluation Summary:
{json.dumps(evaluation, indent=2)}

Provide:
1. 3-5 specific talking points about why this candidate is a great fit
2. Research/work you should reference from their profile
3. Unique value proposition for this role
4. Suggested tone and approach for outreach

Format as actionable talking points for a recruiter.
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system="You are a technical recruiter helping to personalize outreach.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Error generating outreach context: {e}")
            return "Unable to generate personalized context"
    
    def _build_evaluation_prompt(
        self,
        candidate: Dict[str, Any],
        job: Dict[str, Any],
        context: str
    ) -> str:
        """Build the evaluation prompt for Claude."""
        
        candidate_summary = f"""
CANDIDATE PROFILE:
Name: {candidate.get('name')}
Current Role: {candidate.get('current_role', 'N/A')}
Experience Years: {candidate.get('experience_years', 'N/A')}
Skills: {', '.join(candidate.get('skills', []))}
Research Interests: {', '.join(candidate.get('research_interests', []))}
Location: {candidate.get('location', 'N/A')}
Current Company: {candidate.get('company', 'N/A')}

Publications: {len(candidate.get('publications', []))} papers
Followers/Connections: {candidate.get('followers', candidate.get('connections', 'N/A'))}

Profile Summary:
{candidate.get('bio', 'No summary available')[:500]}
"""
        
        job_summary = f"""
JOB REQUIREMENTS:
Title: {job.get('title')}
Team: {job.get('team', 'N/A')}
Required Skills: {', '.join(job.get('required_skills', []))}
Seniority Level: {job.get('seniority_level', 'N/A')}
Domain: {job.get('domain', 'N/A')}
Experience Required: {job.get('min_experience_years', 'N/A')} years

Job Description:
{job.get('description', 'No description available')[:500]}
"""
        
        prompt = f"""{candidate_summary}

{job_summary}

{f"Additional Context: {context}" if context else ""}

TASK: Evaluate this candidate for the role. Provide:
1. Match Score (0-100) with clear justification
2. Key Strengths (3-5 specific points aligned to the role)
3. Potential Gaps (areas for development)
4. Recommendation (Highly Recommended / Recommended / Maybe / Pass)
5. Specific Reasons why this candidate would excel (or struggle) in this role

Consider their research trajectory, technical skills, domain expertise, and growth potential.
Be specific and cite their actual background."""
        
        return prompt
    
    def _get_system_prompt(self) -> str:
        """System prompt for candidate evaluation."""
        return """You are an expert technical recruiter with deep knowledge of AI/ML hiring. 
Your role is to objectively evaluate candidates for technical roles, considering:
- Technical skill alignment
- Research/domain expertise fit
- Career trajectory and growth potential
- Ability to impact and innovate in the role
- Cultural and team fit indicators

Provide detailed, actionable evaluations that help with hiring decisions.
Be fair and objective, highlighting both strengths and growth areas."""
    
    def _parse_evaluation(
        self,
        response_text: str,
        candidate: Dict[str, Any],
        job: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Parse Claude's evaluation response."""
        
        try:
            # Try to extract score from the response
            match_score = 75  # Default
            if "Score:" in response_text or "score:" in response_text:
                # Simple extraction - could be more sophisticated
                for line in response_text.split('\n'):
                    if 'score' in line.lower() and any(char.isdigit() for char in line):
                        try:
                            # Extract first number found
                            score_str = ''.join(filter(lambda x: x.isdigit() or x == '.', 
                                                      line.split(':')[-1][:20]))
                            if score_str:
                                match_score = min(100, max(0, float(score_str)))
                        except:
                            pass
            
            # Extract recommendation
            recommendation = "Recommended"
            if "highly recommended" in response_text.lower():
                recommendation = "Highly Recommended"
            elif "pass" in response_text.lower() or "not recommended" in response_text.lower():
                recommendation = "Pass"
            elif "maybe" in response_text.lower():
                recommendation = "Maybe"
            
            return {
                "candidate_name": candidate.get('name'),
                "candidate_id": candidate.get('id'),
                "job_title": job.get('title'),
                "match_score": match_score,
                "recommendation": recommendation,
                "evaluation_details": response_text,
                "evaluated_at": str(__import__('datetime').datetime.now().isoformat())
            }
        
        except Exception as e:
            logger.error(f"Error parsing evaluation: {e}")
            return self._default_evaluation(candidate, job)
    
    def _default_evaluation(self, candidate: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Return a default evaluation if Claude fails."""
        return {
            "candidate_name": candidate.get('name'),
            "candidate_id": candidate.get('id'),
            "job_title": job.get('title'),
            "match_score": 50,
            "recommendation": "Manual Review Needed",
            "evaluation_details": "Unable to evaluate - please review manually",
            "error": True
        }
