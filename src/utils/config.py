"""
API Configuration Manager

Loads and manages API credentials and settings.
"""

import os
import logging
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class APIConfig:
    """Manages API configuration from environment and config files."""
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to YAML config file
        """
        load_dotenv()
        
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file and environment."""
        # Load YAML config
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Loaded config from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
        
        # Override with environment variables
        self._load_env_overrides()
    
    def _load_env_overrides(self):
        """Load environment variable overrides."""
        env_mapping = {
            'GITHUB_TOKEN': 'github_token',
            'LINKEDIN_TOKEN': 'linkedin_token',
            'ARXIV_EMAIL': 'arxiv_email',
            'RATE_LIMIT_DELAY': 'rate_limit_delay',
            'MAX_RETRIES': 'max_retries',
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                if config_key == 'rate_limit_delay' or config_key == 'max_retries':
                    try:
                        self.config[config_key] = float(value) if '.' in value else int(value)
                    except ValueError:
                        pass
                else:
                    self.config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def get_github_config(self) -> Dict[str, Any]:
        """Get GitHub API configuration."""
        return {
            'github_token': self.get('github_token'),
            'rate_limit_delay': self.get('rate_limit_delay', 1.0),
            'max_retries': self.get('max_retries', 3),
            'timeout': self.get('timeout', 30),
        }
    
    def get_arxiv_config(self) -> Dict[str, Any]:
        """Get ArXiv API configuration."""
        return {
            'arxiv_email': self.get('arxiv_email'),
            'rate_limit_delay': self.get('rate_limit_delay', 3.0),  # ArXiv has stricter limits
            'max_retries': self.get('max_retries', 3),
            'timeout': self.get('timeout', 30),
        }
    
    def get_linkedin_config(self) -> Dict[str, Any]:
        """Get LinkedIn API configuration."""
        return {
            'linkedin_token': self.get('linkedin_token'),
            'rate_limit_delay': self.get('rate_limit_delay', 1.0),
            'max_retries': self.get('max_retries', 3),
            'timeout': self.get('timeout', 30),
        }
    
    def validate(self) -> bool:
        """
        Validate that at least one API is configured.
        
        Returns:
            True if at least one API is properly configured
        """
        has_github = self.get('github_token') is not None
        has_arxiv = True  # ArXiv is public, no token needed
        has_linkedin = self.get('linkedin_token') is not None
        
        if not (has_github or has_arxiv):
            logger.error("No API credentials configured. Please set API tokens in .env")
            return False
        
        if not has_github:
            logger.warning("GitHub API not configured. Some features will be limited.")
        
        if not has_linkedin:
            logger.info("LinkedIn API not configured. Set LINKEDIN_TOKEN to enable LinkedIn search.")
        
        return True
