# HM Summary Feature

## 🎯 Overview

The **HM Summary** feature automatically generates a professional markdown report for hiring managers, making it easy to share top ICRA candidates with formatted summaries and a drafted email.

---

## ✨ What It Does

Takes your ICRA candidate search results and creates a polished report including:

1. **Top 3 Candidates** (configurable)
   - Ranked by ICRA publication count
   - ICRA paper titles and years
   - 2-sentence fit summaries tailored to your team

2. **Drafted Email to Hiring Manager**
   - Professional format ready to send
   - Highlights why candidates stand out
   - Recommended next steps
   - Customizable with HM name

3. **Professional Formatting**
   - Clean markdown layout
   - Easy to read and share
   - Includes profile links and metadata

---

## 🚀 Quick Start

### Option 1: Automatic (Recommended)

```bash
python3 quick_icra_scan.py
```

This will:
1. Search ICRA 2025 for Foundation Models + End-to-End Learning
2. **Automatically generate `HM_Summary.md`** ✨
3. Export full data to JSON

### Option 2: Demo

```bash
python3 demo_hm_summary.py
```

See a complete demonstration of the HM summary feature.

### Option 3: Manual in Python

```python
from src.sourcing_agent import SourcingAgent

agent = SourcingAgent()

# Find ICRA authors
authors = agent.find_icra_authors("foundation models", year=2025)

# Generate HM summary
agent.generate_hm_summary(
    candidates=authors,
    job_title="Robotics ML Engineer - Core Autonomy",
    team_name="Core Autonomy / Tesla Optimus",
    output_file="HM_Summary.md",
    top_n=3  # Top 3 candidates
)
```

---

## 📊 Example Output

**File: HM_Summary.md**

```markdown
# Hiring Manager Summary
## Robotics ML Engineer - Core Autonomy - Core Autonomy / Tesla Optimus

**Generated:** March 12, 2026 at 01:30 PM
**Total Candidates Reviewed:** 15
**Top Candidates Presented:** 3

---

## 🎯 Top 3 Candidates

### 1. Dr. Jane Smith

**ICRA Publications:** 5 papers (2025, 2024, 2023, 2022, 2021)

**Most Recent ICRA Paper:**
*"Foundation Models for Generalizable Robot Manipulation"* (ICRA 2025)

**Why This Candidate Fits Core Autonomy / Tesla Optimus:**
Dr. Jane Smith has a strong track record in robotics research with 5 publications
at ICRA (most recently 2025), demonstrating proven expertise in cutting-edge
robotic systems relevant to Core Autonomy / Tesla Optimus. Their work on
foundation models and end-to-end learning aligns perfectly with our goals of
building scalable, generalizable robotic systems for humanoid manipulation tasks.

**Research Interests:** cs.RO, cs.AI, cs.LG, cs.CV

**Profile:** https://arxiv.org/search/?query=Jane+Smith&searchtype=author

---

## 📧 Drafted Email to Hiring Manager

---

**Subject:** Top ICRA Authors for Robotics ML Engineer - Core Autonomy - 3 Strong Candidates Identified

**To:** [Hiring Manager Name]
**From:** [Your Name]
**Date:** March 12, 2026

---

Hi [HM Name],

I wanted to share some exciting findings from our latest sourcing effort for the
**Robotics ML Engineer - Core Autonomy** position on the **Core Autonomy / Tesla Optimus** team.

I've identified **3 exceptional candidates** who have published at **ICRA (International
Conference on Robotics and Automation)**, one of the premier robotics conferences.
These researchers have a combined **12 publications** at ICRA spanning **2021-2025**,
demonstrating both depth and currency in cutting-edge robotics research.

### Top Candidates:

1. **Dr. Jane Smith**
   - 5 ICRA publications
   - Recent work: *"Foundation Models for Generalizable Robot Manipulation"*
   - Strong fit for our foundation models and end-to-end learning initiatives

... [2 more candidates]

### Why These Candidates Stand Out:

- ✅ **Proven Research Track Record:** All have published at ICRA, validating their
     expertise through peer review at a top-tier conference
- ✅ **Relevant Expertise:** Their work spans foundation models, end-to-end learning,
     and robotic manipulation—directly aligned with our Core Autonomy / Tesla Optimus roadmap
- ✅ **Active in Field:** Recent publications (2021-2025) show they're working on
     current problems, not legacy approaches
- ✅ **Publication + Implementation:** ICRA researchers typically have both theoretical
     knowledge and hands-on robotics experience

### Recommended Next Steps:

1. **Review profiles** (links in detailed summary above)
2. **Prioritize outreach** to these 3 candidates given their strong alignment
3. **Schedule initial screenings** to assess interest and availability
4. **Technical deep-dive** on their ICRA papers to identify conversation starters

...

Best regards,
[Your Name]
```

---

## 🎨 Customization Options

### Customize Team and Job Title

```python
agent.generate_hm_summary(
    candidates=authors,
    job_title="Staff ML Engineer - Autopilot",
    team_name="Autopilot Vision",
    output_file="HM_Summary_Autopilot.md"
)
```

### Change Number of Candidates

```python
# Show top 5 instead of top 3
agent.generate_hm_summary(
    candidates=authors,
    top_n=5,
    output_file="HM_Summary_Top5.md"
)
```

### Multiple Reports for Different Roles

```python
# Generate separate reports for different teams
agent.generate_hm_summary(authors, job_title="Robotics Engineer",
                         team_name="Optimus", output_file="HM_Optimus.md")

agent.generate_hm_summary(authors, job_title="Perception Engineer",
                         team_name="Autopilot", output_file="HM_Autopilot.md")
```

---

## 📝 How It Works

### 1. Candidate Ranking

Candidates are ranked by **ICRA publication count** (most prolific first).

### 2. Fit Summary Generation

The system automatically generates 2-sentence summaries by analyzing:
- Number of ICRA publications
- Most recent ICRA year
- Paper titles (keywords like "foundation models", "end-to-end", "manipulation")
- Research interests

**Example Logic:**
- **3+ ICRA papers** → "strong track record"
- **Recent ICRA (2024-2025)** → "most recently 2025"
- **"foundation" in title** → "work on foundation models aligns perfectly..."
- **"manipulation" in title** → "focus on robotic manipulation directly addresses..."

### 3. Email Draft

The email includes:
- Professional subject line
- Executive summary of findings
- Candidate highlights
- Why they stand out section
- Recommended next steps

All ready to customize with HM name and send.

---

## 🎯 Use Cases

### 1. Weekly Talent Pipeline Update

```python
# Every Friday, generate summary of new ICRA talent
agent = SourcingAgent()
authors = agent.find_icra_authors("foundation models", year=2025)
agent.generate_hm_summary(authors, output_file=f"HM_Summary_{date}.md")
# Email to HM
```

### 2. Specialized Role Recruiting

```python
# Different summaries for different specializations
for topic in ["manipulation", "navigation", "perception"]:
    authors = agent.find_icra_authors(topic, year=2025)
    agent.generate_hm_summary(
        authors,
        job_title=f"Robotics Engineer - {topic.title()}",
        output_file=f"HM_Summary_{topic}.md"
    )
```

### 3. Conference-Specific Sourcing

```python
# After ICRA 2025 concludes
icra_2025_authors = agent.find_icra_authors(year=2025, max_results=50)
agent.generate_hm_summary(icra_2025_authors,
                         output_file="HM_Summary_ICRA2025_Highlights.md")
```

---

## ✅ What Gets Generated

### File Structure

```
HM_Summary.md
├── Header (metadata, counts)
├── Top N Candidates Section
│   ├── Candidate 1
│   │   ├── ICRA publications count
│   │   ├── Most recent paper
│   │   ├── Fit summary (2 sentences)
│   │   ├── Research interests
│   │   └── Profile link
│   ├── Candidate 2
│   └── Candidate 3
└── Drafted Email Section
    ├── Subject line
    ├── To/From/Date
    ├── Executive summary
    ├── Top candidates list
    ├── Why they stand out
    └── Recommended next steps
```

### Metadata Included

For each candidate:
- Name
- ICRA publication count
- ICRA years (e.g., 2025, 2024, 2023)
- Most recent ICRA paper title
- Conference year of recent paper
- Fit summary (2 sentences)
- Research interests (top 5)
- ArXiv profile URL

---

## 🔧 API Reference

### `generate_hm_summary()`

```python
def generate_hm_summary(
    candidates: list,
    job_title: str = "Robotics ML Engineer - Core Autonomy",
    team_name: str = "Core Autonomy / Tesla Optimus",
    output_file: str = "HM_Summary.md",
    top_n: int = 3
) -> str
```

**Parameters:**
- `candidates` (list): List of candidate profiles (from `find_icra_authors()`)
- `job_title` (str): Position title for the report
- `team_name` (str): Team or division name
- `output_file` (str): Path to output markdown file
- `top_n` (int): Number of top candidates to include (default: 3)

**Returns:**
- `str`: Path to generated summary file

**Example:**
```python
output_file = agent.generate_hm_summary(
    candidates=icra_authors,
    job_title="Senior Robotics Engineer",
    team_name="Optimus Manipulation",
    output_file="summary.md",
    top_n=5
)
```

---

## 💡 Best Practices

### 1. Search Before Generating

Always find candidates first:
```python
# ✅ Good
authors = agent.find_icra_authors("foundation models", year=2025)
agent.generate_hm_summary(authors)

# ❌ Don't pass empty list
agent.generate_hm_summary([])  # Warning logged
```

### 2. Use Descriptive Output Names

```python
# ✅ Good - descriptive names
agent.generate_hm_summary(authors, output_file="HM_Summary_ICRA2025_FoundationModels.md")

# ❌ Less helpful
agent.generate_hm_summary(authors, output_file="summary.md")
```

### 3. Customize for Your Team

```python
# ✅ Good - specific to your org
agent.generate_hm_summary(
    authors,
    job_title="ML Engineer II - Robotics",
    team_name="Tesla Bot - Core Autonomy"
)
```

### 4. Review and Customize Email

The drafted email is a starting point. Always:
- Add HM name
- Adjust tone if needed
- Add any team-specific context
- Update next steps based on your process

---

## 🐛 Troubleshooting

### No HM_Summary.md created?

**Check:**
1. Did you pass candidates? `if not candidates: # No summary generated`
2. Check logs for warnings
3. Verify write permissions in directory

### Summary looks empty?

**Likely causes:**
1. Empty candidate list passed
2. Candidates missing ICRA metadata
3. Use `find_icra_authors()` not regular `search_candidates()`

### Want more/fewer candidates?

```python
# Change top_n parameter
agent.generate_hm_summary(authors, top_n=5)  # Top 5 instead of 3
```

---

## 📚 Related Documentation

- **ICRA_README.md** - Full ICRA feature guide
- **USAGE.md** - General usage guide
- **README.md** - Project overview

---

## ✨ Summary

**What:** Automatically generates hiring manager summaries with top ICRA candidates

**Why:** Saves time formatting reports and drafting emails

**How:** One method call creates professional markdown with candidates + email

**Output:** `HM_Summary.md` ready to send to hiring manager

**Scripts:**
- `quick_icra_scan.py` - Auto-generates summary
- `demo_hm_summary.py` - Feature demonstration
- `example_icra_search.py` - Example 6 shows usage

**Quick Start:**
```bash
python3 quick_icra_scan.py
# Opens HM_Summary.md
```

---

**Ready to use!** 🎉
