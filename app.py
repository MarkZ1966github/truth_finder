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
    print("=== Starting verify request processing ===")  # Enhanced debug log
    
    # Log request headers
    print(f"Request Headers: {dict(request.headers)}")
    
    # Validate request content type
    if not request.is_json:
        print(f"Invalid content type: {request.content_type}")  # Debug log
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        if data is None:
            print("Error: None data received")  # Debug log
            return jsonify({'error': 'Invalid JSON payload'}), 400
            
        query = data.get('query', '').strip()
        print(f"Processed query: '{query}'")  # Debug log
        
        if not query:
            print("Error: Empty query after processing")  # Debug log
            return jsonify({'error': 'No query provided'}), 400
        
        print(f"Processing query through news service...")  # Debug log
        results = news_service.get_relevant_links(query)
        
        if not results:
            print("No results found for query")  # Debug log
            return jsonify({'results': [], 'message': 'No results found'}), 200
            
        print(f"Results obtained: {results}")  # Debug log
        return jsonify({
            'results': results,
            'status': 'success',
            'count': len(results)
        })
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        print(f"Error type: {type(e)}")  # Additional error info
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)