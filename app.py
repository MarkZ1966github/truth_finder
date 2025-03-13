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
    print("Received verify request")  # Debug log
    data = request.get_json()
    query = data.get('query', '')
    
    print(f"Query received: {query}")  # Debug log
    
    if not query:
        print("Error: Empty query")  # Debug log
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        print(f"Processing query through news service...")  # Debug log
        results = news_service.get_relevant_links(query)
        print(f"Results obtained: {results}")  # Debug log
        return jsonify({'results': results})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)