from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from news_service import NewsService
import sys
app = Flask(__name__)
try:
    news_service = NewsService()
except ValueError as e:
    print(e)
    sys.exit(1)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    if not query:
        error = "Please enter a search term."
        return render_template("index.html", error=error)
    
    stories = news_service.search_news_stories(query)
    for story in stories:
        rating_data = news_service.get_url_rating(story["url"], story["title"])
        story["rating"] = rating_data["rating"]
        story["domain"] = rating_data["domain"]
        story["explanation"] = rating_data["explanation"]
    
    return render_template("results.html", query=query, results=stories)
if __name__ == "__main__":
    app.run(debug=True)