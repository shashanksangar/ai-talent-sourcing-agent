#!/usr/bin/env python3
"""
Web Interface for AI Talent Sourcing Agent

Flask-based web application for:
- Interactive candidate search
- AI-powered evaluation
- Results dashboard
- Export functionality
"""

from flask import Flask, render_template, request, jsonify, send_file
from src.sourcing_agent import SourcingAgent
from src.orchestrator import SourcingOrchestrator
import json
import logging
from datetime import datetime
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize agents
sourcing_agent = SourcingAgent()
orchestrator = SourcingOrchestrator()

# Store results in session
results_cache = {}


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for candidate search."""
    try:
        data = request.json
        query = data.get('query', '').strip()
        platforms = data.get('platforms', ['arxiv', 'github'])
        limit = int(data.get('limit', 10))
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        logger.info(f"Searching for: {query} on {platforms}")
        
        results = sourcing_agent.search_candidates(query, platforms)
        
        # Flatten and limit results
        candidates = []
        for platform, cands in results.items():
            for cand in cands[:limit]:
                cand['platform'] = platform
                candidates.append(cand)
        
        # Cache results
        session_id = f"search_{datetime.now().timestamp()}"
        results_cache[session_id] = {
            'type': 'search',
            'query': query,
            'platforms': platforms,
            'candidates': candidates,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total': len(candidates),
            'candidates': candidates[:limit]
        })
    
    except Exception as e:
        logger.exception("Search error")
        return jsonify({'error': str(e)}), 500


@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    """API endpoint for candidate evaluation."""
    try:
        data = request.json
        session_id = data.get('session_id')
        job_title = data.get('job_title', '').strip()
        required_skills = data.get('required_skills', [])
        
        if not session_id or session_id not in results_cache:
            return jsonify({'error': 'Invalid session'}), 400
        
        if not job_title:
            return jsonify({'error': 'Job title required'}), 400
        
        cached_data = results_cache[session_id]
        candidates = cached_data.get('candidates', [])
        
        job_requirements = {
            'title': job_title,
            'required_skills': required_skills
        }
        
        logger.info(f"Evaluating {len(candidates)} candidates for: {job_title}")
        
        # Prepare evaluations (mock - full evaluation uses Claude)
        evaluations = []
        for cand in candidates[:10]:  # Evaluate first 10
            evaluation = {
                'candidate_id': cand.get('id'),
                'candidate_name': cand.get('name', 'Unknown'),
                'score': 75,  # This would come from Claude
                'recommendation': 'Recommended',
                'match_reason': 'Skills and experience align well'
            }
            evaluations.append(evaluation)
        
        # Sort by score descending
        evaluations = sorted(evaluations, key=lambda x: x['score'], reverse=True)
        
        # Update cache
        session_id = f"eval_{datetime.now().timestamp()}"
        results_cache[session_id] = {
            'type': 'evaluation',
            'job_requirements': job_requirements,
            'evaluations': evaluations,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total': len(evaluations),
            'evaluations': evaluations
        })
    
    except Exception as e:
        logger.exception("Evaluation error")
        return jsonify({'error': str(e)}), 500


@app.route('/api/pipeline', methods=['POST'])
def api_full_pipeline():
    """API endpoint for complete discover + evaluate pipeline."""
    try:
        data = request.json
        query = data.get('query', '').strip()
        job_title = data.get('job_title', '').strip()
        required_skills = data.get('required_skills', [])
        platforms = data.get('platforms', ['arxiv', 'github'])
        limit = int(data.get('limit', 5))
        
        if not query or not job_title:
            return jsonify({'error': 'Query and job title required'}), 400
        
        logger.info(f"Running full pipeline: {query} for {job_title}")
        
        # Step 1: Search
        search_results = sourcing_agent.search_candidates(query, platforms)
        candidates = []
        for platform, cands in search_results.items():
            for cand in cands[:limit]:
                cand['platform'] = platform
                candidates.append(cand)
        
        # Step 2: Prepare evaluations (mock)
        evaluations = []
        for cand in candidates[:10]:
            evaluation = {
                'candidate_id': cand.get('id'),
                'candidate_name': cand.get('name', 'Unknown'),
                'platform': cand.get('platform'),
                'score': 78,
                'recommendation': 'Recommended',
                'outreach_context': f"Interested in {job_title} role at Tesla"
            }
            evaluations.append(evaluation)
        
        evaluations = sorted(evaluations, key=lambda x: x['score'], reverse=True)
        
        # Cache results
        session_id = f"pipeline_{datetime.now().timestamp()}"
        results_cache[session_id] = {
            'type': 'full_pipeline',
            'query': query,
            'job_requirements': {
                'title': job_title,
                'required_skills': required_skills
            },
            'candidates_found': len(candidates),
            'evaluations': evaluations,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'candidates_found': len(candidates),
            'candidates_evaluated': len(evaluations),
            'evaluations': evaluations
        })
    
    except Exception as e:
        logger.exception("Pipeline error")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<session_id>', methods=['GET'])
def api_export(session_id):
    """API endpoint to export results."""
    try:
        if session_id not in results_cache:
            return jsonify({'error': 'Session not found'}), 404
        
        data = results_cache[session_id]
        
        # Generate JSON
        json_data = json.dumps(data, indent=2)
        
        # Return as file download
        return send_file(
            io.BytesIO(json_data.encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f"sourcing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    
    except Exception as e:
        logger.exception("Export error")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'AI Talent Sourcing Agent',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("\n🚀 Starting AI Talent Sourcing Agent Web Interface")
    print("📍 Access at: http://localhost:5000")
    print("   API Docs: http://localhost:5000/api/health\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
