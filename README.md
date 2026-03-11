# AI Talent Sourcing Agent

An agentic AI-powered tool for finding and evaluating candidates. Combines multiple data sources (GitHub, ArXiv, LinkedIn) with Claude AI for intelligent candidate assessment.

**🌟 Perfect for:** Quick candidate discovery, AI-powered evaluation, team dashboards

## ⚡ Quick Start (Choose Your Interface)

### 1️⃣ Interactive CLI (Fastest for Terminal Users)
```bash
python interactive_cli.py
# Menu-driven interface with prompts
# Search → Evaluate → Export
```

### 2️⃣ Web Dashboard (Best for Teams)
```bash
python app.py
# Open: http://localhost:5000
# Search, evaluate, and export in your browser
```

### 3️⃣ Python API (For Developers)
```python
from src.orchestrator import SourcingOrchestrator

orchestrator = SourcingOrchestrator()
results = orchestrator.find_and_evaluate_candidates(
    search_query="machine learning researcher",
    job_requirements={"title": "ML Engineer", "required_skills": ["PyTorch"]},
    platforms=['arxiv', 'github'],
    limit=5
)
```

## Features

- ✅ **Interactive CLI Interface** - Menu-driven terminal UI with rich prompts
- ✅ **Web Dashboard** - Beautiful HTML/CSS interface with real-time results
- ✅ **Intelligent Discovery** - Search across GitHub, ArXiv, LinkedIn
- ✅ **AI Evaluation** - Claude Sonnet scores and ranks candidates
- ✅ **Tesla Bottlerocket Integration** - Powered by GCP Vertex AI
- ✅ **One-Click Export** - JSON results for reporting
- ✅ **Result Caching** - View and manage past searches
- ✅ **Track Latest Papers** - Monitor cutting-edge research relevant to your team
- ✅ **Find Emerging Talent** - Discover rising stars in specific AI research areas

## Installation

1. Clone and setup:
```bash
git clone https://github.com/shashanksangar/ai-talent-sourcing-agent.git
cd ai-talent-sourcing-agent
```

2. Install dependencies:
```bash
pip install flask anthropic requests python-dotenv feedparser pyyaml
```

3. Configure credentials:
```bash
# Copy example and add your Tesla Bottlerocket credentials
cp .env.example .env
nano .env  # Add your API tokens
```

## Usage Guide

### 📖 Complete Documentation
See [`USAGE.md`](USAGE.md) for detailed guides:
- CLI interface tutorial
- Web dashboard walkthrough
- API examples
- Configuration options
- Troubleshooting

### CLI Examples

**Search for candidates:**
```bash
python interactive_cli.py
# Select: 1 (Search)
# Query: "deep learning researcher"
# Platforms: arxiv,github
# Limit: 10
```

**Find and evaluate (complete pipeline):**
```bash
python interactive_cli.py
# Select: 3 (Find & Evaluate)
# Query: "ML engineer"
# Job: "Senior ML Engineer"
# Required Skills: "Python, PyTorch, Research"
```

**Export results:**
```bash
python interactive_cli.py
# Select: 5 (Export)
# Filename: candidates_march.json
```

**Track latest papers for your team:**
```bash
python examples.py  # Run example_track_papers()
# Or programmatically:
from src.sourcing_agent import SourcingAgent
agent = SourcingAgent()
papers = agent.track_latest_papers(team_keywords=["computer vision", "transformers"])
```

**Find emerging talent in research areas:**
```bash
python examples.py  # Run example_emerging_talent()
# Or programmatically:
from src.sourcing_agent import SourcingAgent
agent = SourcingAgent()
talent = agent.find_emerging_talent(["natural language processing", "reinforcement learning"])
```

### Web Dashboard Examples

**Start server:**
```bash
python app.py
# Open: http://localhost:5000
```

**Complete Pipeline workflow:**
1. Go to "⚡ Complete Pipeline" tab
2. Enter search query: "computer vision engineer"
3. Enter job title: "CV Lead"
4. Add required skills: "CNN, Object Detection"
5. Click "Run Complete Pipeline"
6. Export JSON with "📥 Export" button

## Configuration

### Environment Variables (.env)
```
ANTHROPIC_VERTEX_BASE_URL=https://inference.bottlerocket.tesla.com/...
ANTHROPIC_AUTH_TOKEN=your_token_here
ANTHROPIC_VERTEX_PROJECT_ID=bottle-rocket-recruiting
```

### Config File (config.yaml)
```yaml
ai_evaluation:
  enabled: true
  model: claude-sonnet-4-5
  temperature: 0.5

platforms:
  - arxiv
  - github
```

## Project Structure

```
ai-talent-sourcing-agent/
├── interactive_cli.py          # CLI interface
├── app.py                      # Web server
├── templates/
│   └── index.html              # Web UI
├── src/
│   ├── sourcing_agent.py       # Main agent
│   ├── orchestrator.py         # Discovery + evaluation
│   ├── ai_evaluator.py         # Claude integration
│   ├── api/
│   │   ├── base_client.py
│   │   ├── github_client.py
│   │   ├── arxiv_client.py
│   │   └── linkedin_client.py
│   └── models/
├── config.yaml                 # Configuration
├── .env                        # Credentials
└── USAGE.md                    # Complete guide
```

## Development

### Run Tests
```bash
python -m pytest tests/
```

### Extend with New Platforms
See `src/api/base_client.py` for the client interface.

## Contributing

Part of the **AI Talent Copilot** ecosystem. See the main project for contribution guidelines.

## License

See main project repository.