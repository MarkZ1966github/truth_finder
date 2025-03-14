from flask import Flask, render_template, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
from news_service import NewsService
app = Flask(__name__)
news_service = NewsService()
def fetch_google_news(query, max_results=5):
    """
    Scrape Google News for articles matching the query.
    Returns a list of dictionaries with keys: 'title', 'url', and 'description'
    """
    try:
        search_url = "https://news.google.com/search?q=" + requests.utils.quote(query)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/134.0.0.0 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Google News request failed with status:", response.status_code)
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        results = []
        for article in articles:
            # Extract headline text from the entire article
            headline = article.get_text(separator=" ").strip()
            
            # Find the first anchor tag to retrieve the link
            link_tag = article.find('a')
            link = ""
            if link_tag and link_tag.has_attr("href"):
                link = link_tag["href"]
                if link.startswith("."):
                    link = "https://news.google.com" + link[1:]
            
            # Only add if both headline and link are present;
            # map the keys to those expected by your frontend.
            if headline and link:
                results.append({
                    "title": headline,
                    "url": link,
                    "description": "No Description available"
                })
            if len(results) >= max_results:
                break
        return results
    except Exception as e:
        print("Error fetching Google News:", e)
        return []
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/verify', methods=['POST'])
def verify():
    print("=== Starting verify request processing ===")
    print(f"Request Headers: {dict(request.headers)}")
    
    if not request.is_json:
        print(f"Invalid content type: {request.content_type}")
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        if data is None:
            print("Error: None data received")
            return jsonify({'error': 'Invalid JSON payload'}), 400
        query = data.get('query', '').strip()
        print(f"Processed query: '{query}'")
        if not query:
            print("Error: Empty query after processing")
            return jsonify({'error': 'No query provided'}), 400
        print("Processing query through news service...")
        try:
            raw_results = news_service.get_relevant_links(query)
            results = list(raw_results) if raw_results is not None else []
        except Exception as e:
            print("Error from NewsService:", e)
            results = []
        # Fallback to Google News if primary service produced no results.
        if not results:
            print("No results from primary service. Trying Google News fallback...")
            results = fetch_google_news(query)
        if not results:
            print("No results found for query after fallback")
            return jsonify({'results': [], 'message': 'No results found'}), 200
        print(f"Results obtained: {results}")
        return jsonify({
            'results': results,
            'status': 'success',
            'count': len(results)
        })
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'details': str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)