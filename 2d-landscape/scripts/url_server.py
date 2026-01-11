"""
Simple Flask server to receive URLs from Chrome extension and save to all_urls.json
Run with: python url_server.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from Chrome extension

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'all_urls.json')

@app.route('/add-url', methods=['POST'])
def add_url():
    try:
        data = request.json
        url = data.get('url')
        design_keywords = data.get('designKeywords', [])
        critical_keywords = data.get('criticalKeywords', [])
        
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'}), 400
        
        # Load current data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        else:
            all_data = {'urls': []}
        
        # Check if URL already exists
        if url in all_data['urls']:
            return jsonify({
                'success': False, 
                'error': 'URL already exists',
                'totalUrls': len(all_data['urls'])
            }), 409
        
        # Add new URL
        all_data['urls'].append(url)
        
        # Save back to file
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Added URL: {url}")
        print(f"  Design keywords: {', '.join(design_keywords)}")
        print(f"  Critical keywords: {', '.join(critical_keywords)}")
        print(f"  Total URLs: {len(all_data['urls'])}")
        
        return jsonify({
            'success': True,
            'totalUrls': len(all_data['urls']),
            'message': 'URL added successfully'
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'running', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    print("=" * 60)
    print("URL Collection Server")
    print("=" * 60)
    print(f"Server running on http://localhost:5000")
    print(f"Saving to: {DATA_FILE}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='localhost', port=5000, debug=False)
