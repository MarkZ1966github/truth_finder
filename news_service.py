from GoogleNews import GoogleNews
from typing import List, Dict
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('stopwords')
class NewsService:
    def __init__(self):
        self.googlenews = GoogleNews(lang='en', period='7d')
    
    def get_relevant_links(self, query: str) -> List[Dict]:
        self.googlenews.clear()
        self.googlenews.search(query)
        results = self.googlenews.results()
        
        # Process and rate the results
        processed_results = []
        for result in results[:10]:
            relevance_score = self._calculate_relevance(query, result.get('desc', ''))
            processed_results.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'description': result.get('desc', ''),
                'rating': min(round(relevance_score * 10), 10)  # Scale to 1-10
            })
        
        return processed_results
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([query, content])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]