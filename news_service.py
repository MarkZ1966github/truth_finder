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
            truth_score = self._calculate_truth_score(result.get('title', ''), 
                                                    result.get('desc', ''),
                                                    result.get('link', ''))
            processed_results.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'description': result.get('desc', ''),
                'relevance_score': min(round(relevance_score * 10), 10),
                'truth_score': truth_score,
                'ratings': {
                    'relevance': min(round(relevance_score * 10), 10),
                    'truth': truth_score
                }
            })
        return processed_results
def _calculate_relevance(self, query: str, content: str) -> float:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([query, content])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        """Calculate a truth score from 1-10 based on various factors.
        
        1-3: Likely disinformation
        4-6: Requires fact checking
        7-10: Likely truthful
        """
        score = 5.0  # Start with neutral score
        
        # Domain credibility check
        domain = self._extract_domain(url)
        credible_domains = {'reuters.com', 'apnews.com', 'bloomberg.com', 'bbc.com', 
                          'nytimes.com', 'wsj.com', 'washingtonpost.com'}
        suspicious_domains = {'wordpress.com', 'blogspot.com', 'medium.com'}
        
        if domain in credible_domains:
            score += 2.5
        elif domain in suspicious_domains:
            score -= 1.5
            
        # Content analysis
        text = f"{title} {description}".lower()
        
        # Check for clickbait patterns
        clickbait_patterns = ['you won\'t believe', 'shocking', 'mind blowing', 
                            'this will blow your mind', '!!!', '???']
        if any(pattern in text for pattern in clickbait_patterns):
            score -= 1.0
            
        # Check for balanced reporting indicators
        balanced_indicators = ['according to', 'research shows', 'studies indicate', 
                            'experts say', 'evidence suggests']
        if any(indicator in text for indicator in balanced_indicators):
            score += 1.0
            
        # Normalize score to 1-10 range
        score = max(1, min(10, score))
        return round(score)
        
def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed_uri = urlparse(url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            return domain
        except:
            return url
        """Extract the main domain from a URL."""
        from urllib.parse import urlparse
        try:
            return urlparse(url).netloc.lower()
        except:
            return ""