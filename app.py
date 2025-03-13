from flask import Flask, render_template, request, jsonify
import os
from news_service import NewsService
app = Flask(__name__)
news_service = NewsService()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        results = news_service.get_relevant_links(query)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})
if __name__ == '__main__':
    app.run(debug=True)