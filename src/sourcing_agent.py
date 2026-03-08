#!/usr/bin/env python3
"""
AI Talent Sourcing Agent

An agentic tool for automated candidate sourcing.
"""

import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="AI Talent Sourcing Agent")
    parser.add_argument("--config", type=str, default="config.yaml", help="Configuration file")
    args = parser.parse_args()

    print("AI Talent Sourcing Agent starting...")
    print(f"Using config: {args.config}")

    # TODO: Implement sourcing logic
    # - API integrations (LinkedIn, GitHub, etc.)
    # - AI-powered filtering
    # - Outreach automation

    print("Sourcing agent initialized. Ready for operation.")

if __name__ == "__main__":
    main()
