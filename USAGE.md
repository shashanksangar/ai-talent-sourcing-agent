# Running AI Talent Sourcing Agent: User Guides

This guide shows you how to run the Sourcing Agent with both interactive CLI and web interfaces.

## ⚡ Quick Start

### Prerequisites
```bash
pip install flask python-dotenv feedparser requests anthropic pyyaml
```

### Configuration
Make sure `.env` file is configured with Tesla Bottlerocket credentials:
```bash
cat .env  # Should show ANTHROPIC credentials configured
```

---

## 🎯 Option 1: Interactive CLI (Recommended for Quick Searches)

The fastest way to search and evaluate candidates from your terminal.

### Starting the CLI
```bash
python interactive_cli.py
```

### What You Can Do

**1. Search for Candidates**
```
Select option: 1

Search query: machine learning researcher
Which platforms to search?: arxiv,github
Number of results: 10
```

**2. Find & Evaluate in One Command**
```
Select option: 3

Search query: deep learning engineer
Job title: Senior ML Engineer
Required skills: PyTorch, Transformers, Python
Platforms: arxiv,github
Results limit: 5
```

**3. Export Results**
```
Select option: 5

Filename: my_candidates.json
✅ Results exported to my_candidates.json
```

### CLI Menu Options
```
1. Search for candidates              - Discover candidates
2. Evaluate candidates with AI        - Score using Claude
3. Find AND evaluate                  - Complete pipeline
4. View last results                  - Show cached results
5. Export results to file             - Save as JSON
6. Settings and configuration         - Check setup
7. Exit                               - Quit
```

### Example: Sourcing ML Researchers

```bash
# Start CLI
python interactive_cli.py

# Menu: Choose "3" (Find & Evaluate)
# Query: "deep learning researcher"
# Job: "AI Research Scientist"
# Required skills: "Python, PyTorch, published papers"

# Results: Ranked candidates with scores and recommendations
```

---

## 🌐 Option 2: Web Interface (Recommended for Dashboards)

Browser-based interface for searching, evaluating, and exporting results.

### Starting the Web Server

```bash
pip install flask
python app.py
```

Output:
```
🚀 Starting AI Talent Sourcing Agent Web Interface
📍 Access at: http://localhost:5000
```

### Opening in Browser
```
http://localhost:5000
```

### Web Interface Features

**Search Tab**
- Enter search query
- Select platforms (ArXiv, GitHub)
- Set result limit
- View and export results

**Evaluate Tab**
- Specify job requirements
- Add required skills
- Score candidates with Claude
- See recommendations

**Complete Pipeline Tab**
- Single form for full workflow
- Search + evaluate simultaneously
- Ranked results by fit
- One-click export

**Help Tab**
- Usage documentation
- Search examples
- Integration info

### Example: Dashboard Workflow

1. **Open browser:** `http://localhost:5000`
2. **Go to Complete Pipeline tab**
3. **Enter:**
   - Query: "computer vision specialist"
   - Job: "Computer Vision Lead"
   - Skills: "CNN, Object Detection, PyTorch"
4. **Click:** "Run Complete Pipeline"
5. **See:** Results ranked by AI score
6. **Export:** Click "📥 Export" for JSON file

---

## 📊 Command-Line Sourcing Agent (Advanced)

For scripted/automated sourcing:

```bash
python src/sourcing_agent.py --query "machine learning" \
                              --platforms github,arxiv \
                              --output results.json
```

Options:
- `--query`: Search term
- `--platforms`: Comma-separated (github,arxiv,linkedin)
- `--output`: File to save results
- `--config`: Configuration file (default: config.yaml)

---

## 🤖 Python API (For Developers)

### Basic Search
```python
from src.sourcing_agent import SourcingAgent

agent = SourcingAgent()
results = agent.search_candidates(
    query="machine learning researcher",
    platforms=['arxiv', 'github']
)

for platform, candidates in results.items():
    print(f"{platform.upper()}: {len(candidates)} candidates")
```

### Complete Pipeline with Evaluation
```python
from src.orchestrator import SourcingOrchestrator

orchestrator = SourcingOrchestrator()
results = orchestrator.find_and_evaluate_candidates(
    search_query="deep learning engineer",
    job_requirements={
        "title": "ML Engineer",
        "required_skills": ["PyTorch", "Python"]
    },
    platforms=['arxiv'],
    limit=5
)

for result in results:
    print(f"{result['candidate']['name']}: {result['score']}/100")
```

---

## 📁 Project Structure

```
ai-talent-sourcing-agent/
├── interactive_cli.py          ← Start CLI
├── app.py                      ← Start web server
├── templates/
│   └── index.html              ← Web interface
├── src/
│   ├── sourcing_agent.py       ← Main agent
│   ├── orchestrator.py         ← Discovery + evaluation
│   ├── ai_evaluator.py         ← Claude integration
│   ├── api/
│   │   ├── github_client.py
│   │   ├── arxiv_client.py
│   │   └── linkedin_client.py
│   └── models/
│       ├── candidate.py
│       └── position.py
├── config.yaml                 ← Configuration
└── .env                        ← Credentials
```

---

## 🚀 Running Scenarios

### Scenario 1: Quick Terminal Search
```bash
python interactive_cli.py
# Menu: 3 (Find & Evaluate)
# Enter search query and job details
```

### Scenario 2: Browse Results in Web Dashboard
```bash
python app.py
# Open http://localhost:5000
# Use Complete Pipeline tab
# Export results with one click
```

### Scenario 3: Automated Daily Sourcing
```bash
# Create script: daily_sourcing.py
python daily_sourcing.py  # Runs search + eval automatically
```

### Scenario 4: Integration with Other Tools
```python
# Import and use in your code
from src.orchestrator import SourcingOrchestrator
orchestrator = SourcingOrchestrator()
results = orchestrator.find_and_evaluate_candidates(...)
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```
ANTHROPIC_VERTEX_BASE_URL=https://inference.bottlerocket.tesla.com/...
ANTHROPIC_AUTH_TOKEN=your_token
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

---

## 🔧 Troubleshooting

### Port 5000 already in use?
```bash
python app.py --port 5001
```

### Claude API not responding?
- Check `.env` for valid Bottlerocket credentials
- Verify network connectivity
- Check logs in web console

### No results from search?
- Try broader search terms
- Check platform availability
- Verify API credentials in settings

### Import errors?
```bash
pip install -r requirements.txt
```

---

## 📞 Support

For issues or questions:
1. Check the Help tab in web interface
2. Review CLI menu options
3. Check config.yaml settings
4. Verify .env credentials

---

## 🎓 Learning Path

1. **Start with CLI:** Quick, interactive, no setup
2. **Try Web Interface:** Visual, easy to share
3. **Use Python API:** For automation
4. **Create Scripts:** For scheduled runs

---

## 📊 Example Results Format

### JSON Export
```json
{
  "type": "complete_pipeline",
  "query": "machine learning researcher",
  "job_requirements": {
    "title": "ML Engineer",
    "required_skills": ["PyTorch", "Python"]
  },
  "evaluations": [
    {
      "candidate_name": "Dr. Jane Smith",
      "score": 92,
      "recommendation": "Highly Recommended",
      "match_reason": "Excellent alignment with requirements"
    }
  ],
  "timestamp": "2024-03-07T19:30:00"
}
```

---

## 🚀 Next Steps

- [ ] Run `python interactive_cli.py` for quick test
- [ ] Then try `python app.py` for web interface
- [ ] Configure `.env` with your credentials
- [ ] Try the complete pipeline option
- [ ] Export results and share with team

Happy sourcing! 🎯
