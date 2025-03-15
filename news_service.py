import os
import requests
import urllib.parse
import numpy as np
from sklearn.ensemble import RandomForestRegressor
class NewsService:
    def __init__(self):
        self.newsapi_key = os.environ.get("NEWSAPI_KEY")
        if not self.newsapi_key:
            raise ValueError("Please set the NEWSAPI_KEY environment variable with your NewsAPI key.")
        self.newsapi_endpoint = "https://newsapi.org/v2/everything"
        # Train a machine learning model on dummy data.
        self.model = self.train_model()
    def search_news_stories(self, query, max_results=10):
        """
        Searches for news stories via the NewsAPI's /everything endpoint.
        Returns a list of dictionaries, each containing 'title' and 'url'.
        """
        params = {
            "q": query,
            "pageSize": max_results,
            "apiKey": self.newsapi_key,
            "sortBy": "relevancy"
        }
        response = requests.get(self.newsapi_endpoint, params=params)
        if response.status_code != 200:
            print("Error fetching news:", response.text)
            return []
        data = response.json()
        articles = data.get("articles", [])
        stories = []
        for article in articles:
            stories.append({
                "title": article.get("title", "No Title"),
                "url": article.get("url", "#")
            })
        return stories
    def scan_for_clickbait(self, title):
        """
        A simple function to estimate the clickbait factor in a title.
        The function looks for exclamation marks, question marks, and select
        keywords that might indicate sensational language.
        Returns a normalized value between 0 and 1.
        """
        score = 0
        if title:
            score += title.count("!")
            score += title.count("?")
            lower_title = title.lower()
            keywords = ["shocking", "amazing", "unbelievable", "you won't believe", "surprising"]
            for word in keywords:
                if word in lower_title:
                    score += 1
        normalized = min(score / 5.0, 1.0)
        return normalized
    def extract_features(self, url, title):
        """
        Extracts features used for predicting the news source rating.
        Features include:
          - Base score from domain heuristics.
          - Clickbait factor from the title.
        Returns a NumPy 2D-array (1 x n_features).
        """
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()
        if "gov" in domain or "edu" in domain:
            base_score = 10
        elif any(x in domain for x in ["bbc", "cnn", "apnews", "reuters"]):
            base_score = 9
        elif "news" in domain:
            base_score = 7
        elif "blog" in domain:
            base_score = 4
        else:
            base_score = 5
        clickbait = self.scan_for_clickbait(title)
        return np.array([base_score, clickbait]).reshape(1, -1)
    def train_model(self):
        """
        Trains a simple machine learning model using a dummy dataset.
        In a production setting, replace this with labeled training data.
        The feature vector is [base_score, clickbait_factor] and the target is a rating.
        """
        X = np.array([
            [10, 0.0],
            [9,  0.1],
            [7,  0.5],
            [4,  0.8],
            [5,  0.5],
            [9,  0.0],
            [8,  0.2],
            [10, 0.0],
            [4,  1.0],
            [5,  0.3]
        ])
        y = np.array([10, 9, 7, 3, 5, 9, 8, 10, 2, 5])
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)
        return model
    def get_url_rating(self, url, title=""):
        """
        Calculates a "Site Reliability or Disinformation" rating for the given URL,
        using both domain heuristics and the clickbait factor extracted from the title.
        The model predicts a rating, which is then clamped between 1 and 10 without rounding.
        Returns a dictionary with keys: rating, domain, explanation.
        """
        features = self.extract_features(url, title)
        predicted = self.model.predict(features)
        rating = predicted[0]
        rating = max(1, min(10, rating))
        
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()
        explanation_lines = []
        if "gov" in domain or "edu" in domain:
            explanation_lines.append("This domain is governmental or educational, which is trusted.")
        elif any(x in domain for x in ["bbc", "cnn", "apnews", "reuters"]):
            explanation_lines.append("This is a well-known, reliable news source.")
        elif "news" in domain:
            explanation_lines.append("This domain appears to be a news site.")
        elif "blog" in domain:
            explanation_lines.append("This domain is a blog, which may be less reliable.")
        else:
            explanation_lines.append("Using a default rating based on heuristics.")
        
        clickbait = self.scan_for_clickbait(title)
        if clickbait > 0.5:
            explanation_lines.append("High clickbait indicators are present in the title.")
        else:
            explanation_lines.append("Low clickbait factor detected.")
        
        explanation = " ".join(explanation_lines)
        
        return {
            "rating": rating,
            "domain": domain,
            "explanation": explanation
        }