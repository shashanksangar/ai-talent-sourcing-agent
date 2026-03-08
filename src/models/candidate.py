"""
Candidate Data Models

Data classes and schemas for candidate profiles.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class CandidateProfile:
    """Standard candidate profile schema."""
    
    id: str
    name: str
    platform: str
    platform_url: str
    
    # Basic info
    email: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    
    # Professional info
    skills: List[str] = field(default_factory=list)
    experience_level: Optional[str] = None
    experience_years: Optional[int] = None
    current_role: Optional[str] = None
    company: Optional[str] = None
    
    # Research/interests
    research_interests: List[str] = field(default_factory=list)
    publications: List[Dict[str, Any]] = field(default_factory=list)
    
    # Social metrics
    followers: Optional[int] = None
    connections: Optional[int] = None
    contributions: Optional[int] = None
    
    # Metadata
    discovered_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "platform": self.platform,
            "platform_url": self.platform_url,
            "email": self.email,
            "location": self.location,
            "bio": self.bio,
            "skills": self.skills,
            "experience_level": self.experience_level,
            "experience_years": self.experience_years,
            "current_role": self.current_role,
            "company": self.company,
            "research_interests": self.research_interests,
            "publications": self.publications,
            "followers": self.followers,
            "connections": self.connections,
            "contributions": self.contributions,
            "discovered_at": self.discovered_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CandidateProfile':
        """Create from dictionary representation."""
        return cls(**data)


@dataclass
class SearchFilter:
    """Search filter parameters."""
    
    platforms: List[str] = field(default_factory=lambda: ["github", "arxiv"])
    keywords: List[str] = field(default_factory=list)
    location: Optional[str] = None
    min_experience_years: int = 0
    min_followers: int = 0
    max_results: int = 50
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "platforms": self.platforms,
            "keywords": self.keywords,
            "location": self.location,
            "min_experience_years": self.min_experience_years,
            "min_followers": self.min_followers,
            "max_results": self.max_results,
        }
