# ICRA Conference Integration

Find and evaluate robotics researchers who have published at **ICRA (International Conference on Robotics and Automation)**, one of the premier robotics conferences.

## 🎯 Overview

This feature helps you identify top robotics talent by:
- Searching ArXiv for papers published at ICRA
- Filtering by research areas (Foundation Models, End-to-End Learning, etc.)
- Filtering by specific ICRA years (e.g., ICRA 2025, ICRA 2024)
- Prioritizing ICRA authors in AI evaluation for Tesla Optimus roles

## 🚀 Quick Start

### Option 1: Simple Scan (No AI Evaluation)

```bash
python quick_icra_scan.py
```

This will:
- Search ICRA 2025 for "foundation models" authors
- Search ICRA 2025 for "end-to-end learning" authors
- Export results to JSON

### Option 2: Full Pipeline with AI Evaluation

```bash
python example_icra_search.py
```

This runs 5 comprehensive examples including AI-powered evaluation.

## 📚 How to Use

### 1. Basic ICRA Search

```python
from src.sourcing_agent import SourcingAgent

agent = SourcingAgent()

# Find ICRA 2025 authors working on Foundation Models
authors = agent.find_icra_authors(
    research_area="foundation models",
    year=2025,
    max_results=10
)

print(f"Found {len(authors)} ICRA authors")
for author in authors:
    print(f"{author['name']}: {author['icra_paper_count']} ICRA papers")
```

### 2. Search All ICRA Years

```python
# Search all ICRA years (not just 2025)
authors = agent.find_icra_authors(
    research_area="end-to-end learning manipulation",
    year=None,  # Search all years
    max_results=20
)
```

### 3. Multiple Research Areas

```python
topics = ["foundation models", "end-to-end learning", "imitation learning"]

all_authors = []
for topic in topics:
    authors = agent.find_icra_authors(topic, year=2025)
    all_authors.extend(authors)

print(f"Total authors: {len(all_authors)}")
```

### 4. AI Evaluation with ICRA Prioritization

```python
from src.orchestrator import SourcingOrchestrator

orchestrator = SourcingOrchestrator()

# Define job for Tesla Optimus
job_requirements = {
    "title": "Robotics ML Engineer - Tesla Optimus",
    "required_skills": [
        "Foundation Models",
        "End-to-End Learning",
        "Robot Manipulation"
    ],
    "domain": "Embodied AI / Robotics"
}

# Get ICRA authors
agent = SourcingAgent()
icra_authors = agent.find_icra_authors("foundation models", year=2025)

# Evaluate with AI (automatically prioritizes ICRA authors)
for candidate in icra_authors:
    evaluation = orchestrator.ai_evaluator.evaluate_candidate(
        candidate_profile=candidate,
        job_requirements=job_requirements
    )
    print(f"{candidate['name']}: {evaluation['match_score']}/100")
```

## 🔍 How It Works

### ArXiv ICRA Detection

The system searches ArXiv papers and filters for ICRA by checking:
1. **Comment field**: Papers often include "ICRA 2025" or "Accepted to ICRA"
2. **Journal reference**: May contain "International Conference on Robotics and Automation"

Example ICRA detection:
```python
# ArXiv paper metadata
arxiv_comment: "Accepted to ICRA 2025"
journal_ref: "IEEE International Conference on Robotics and Automation (ICRA), 2025"
```

### AI Evaluation Prioritization

The AI evaluator (`src/ai_evaluator.py`) gives bonus scores to:

| Factor | Bonus Points |
|--------|--------------|
| ICRA + Foundation Models/End-to-End Learning | +20-30 |
| Recent ICRA (last 2 years) | +15-20 |
| Multiple ICRA publications | +10-15 |
| Robotics + ML expertise | +10-15 |

This ensures ICRA authors are ranked higher for robotics roles.

## 📊 Output Format

### Author Profile

```json
{
  "id": "John Smith",
  "name": "John Smith",
  "platform": "ArXiv",
  "is_icra_author": true,
  "icra_paper_count": 3,
  "icra_years": [2025, 2024, 2023],
  "most_recent_icra_year": 2025,
  "icra_papers": [
    {
      "title": "Foundation Models for Robot Manipulation",
      "arxiv_id": "2501.12345",
      "published": "2025-01-15",
      "conference_year": 2025,
      "summary": "We present..."
    }
  ],
  "research_interests": ["cs.RO", "cs.AI", "cs.LG"],
  "platform_url": "https://arxiv.org/search/?query=John+Smith&searchtype=author"
}
```

## 🎯 Use Cases for Tesla Optimus

### 1. Find Foundation Model Experts

```python
authors = agent.find_icra_authors("foundation models vision language action", year=2025)
```

Perfect for finding researchers working on:
- RT-1, RT-2 style models
- Vision-Language-Action (VLA) models
- Large-scale robot learning

### 2. Find End-to-End Learning Experts

```python
authors = agent.find_icra_authors("end-to-end learning manipulation", year=2025)
```

Perfect for finding researchers working on:
- Imitation learning
- Behavior cloning
- Policy learning

### 3. Find Humanoid Robot Experts

```python
authors = agent.find_icra_authors("humanoid robot bipedal locomotion", year=2024)
```

Perfect for finding researchers working on:
- Humanoid robotics
- Bipedal locomotion
- Whole-body control

## 🔧 API Reference

### `find_icra_authors(research_area, year, max_results)`

Find authors who have published at ICRA.

**Parameters:**
- `research_area` (str): Research topic to filter (e.g., "foundation models")
- `year` (int, optional): Specific ICRA year (e.g., 2025). None = all years
- `max_results` (int): Maximum number of authors to return (default: 20)

**Returns:**
List of author profiles with ICRA publication data

**Example:**
```python
authors = agent.find_icra_authors(
    research_area="imitation learning",
    year=2025,
    max_results=15
)
```

### ArXiv Client Methods

**`search_icra_papers(query, year, filters)`** - Get ICRA papers
**`search_icra_authors(query, year, filters)`** - Get ICRA authors

### 5. Generate HM Summary Report

```python
# After finding candidates
authors = agent.find_icra_authors("foundation models", year=2025)

# Generate hiring manager summary
agent.generate_hm_summary(
    candidates=authors,
    job_title="Robotics ML Engineer - Core Autonomy",
    team_name="Core Autonomy / Tesla Optimus",
    output_file="HM_Summary.md",
    top_n=3
)
```

This creates a professional markdown report with:
- Top 3 candidates ranked by ICRA publications
- ICRA paper titles and years
- 2-sentence fit summaries for your team
- Drafted email ready to send to hiring manager
- Recommended next steps

**Output: HM_Summary.md**

## 📁 Example Scripts

| Script | Description |
|--------|-------------|
| `quick_icra_scan.py` | Fast scan for ICRA 2025 authors + auto-generates HM_Summary.md |
| `demo_hm_summary.py` | Demo of HM summary generation feature |
| `example_icra_search.py` | Comprehensive examples with AI evaluation |
| `examples.py` | General sourcing examples |

## 🐛 Troubleshooting

### No ICRA papers found?

1. **Try without year filter**: ICRA papers may not have year in metadata
   ```python
   authors = agent.find_icra_authors("foundation models", year=None)
   ```

2. **Try broader search terms**:
   ```python
   authors = agent.find_icra_authors("robot learning", year=2025)
   ```

3. **Check ArXiv directly**: Some ICRA papers may not be on ArXiv yet

### AI evaluation not working?

1. Check `.env` file has valid Claude credentials:
   ```
   ANTHROPIC_VERTEX_BASE_URL=https://...
   ANTHROPIC_AUTH_TOKEN=your_token
   ```

2. Verify `config.yaml` has AI evaluation enabled:
   ```yaml
   ai_evaluation:
     enabled: true
     model: claude-sonnet-4-5
   ```

## 🎓 ICRA Background

**ICRA** (International Conference on Robotics and Automation) is the flagship conference of the IEEE Robotics and Automation Society.

- **Acceptance Rate**: ~40-45% (highly selective)
- **Focus**: Robotics, automation, AI for robotics
- **Frequency**: Annual
- **Prestige**: Top-tier (along with RSS, CoRL)

Authors with ICRA publications have:
✅ Peer-reviewed robotics research
✅ Proven track record in the robotics community
✅ Cutting-edge expertise in robot learning and control

## 💡 Best Practices

1. **Combine with other sources**: Use ICRA as one signal, not the only signal
2. **Look for recent publications**: `year=2025` or `year=2024` for latest work
3. **Use specific keywords**: "foundation models" better than just "robotics"
4. **Evaluate with AI**: Let Claude assess fit beyond just ICRA status
5. **Cross-reference**: Check GitHub profiles for code implementation

## 🚀 Next Steps

After finding ICRA authors:

1. ✅ **Export results**: `agent.export_candidates("icra_authors.json")`
2. ✅ **Evaluate with AI**: Use `SourcingOrchestrator` for scoring
3. ✅ **Generate outreach**: Use `generate_outreach_context()` for personalization
4. ✅ **Track in ATS**: Import to your recruitment system

---

**Questions?** See `USAGE.md` for general usage or `README.md` for project overview.
