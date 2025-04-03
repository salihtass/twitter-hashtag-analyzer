from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer."""
        pass
    
    def analyze_text(self, text):
        """
        Analyze the sentiment of a text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Sentiment score between -1 (negative) and 1 (positive)
        """
        if not text or text.strip() == '':
            return 0
        
        try:
            # Use TextBlob for sentiment analysis
            analysis = TextBlob(text)
            
            # TextBlob returns polarity between -1 (negative) and 1 (positive)
            return analysis.sentiment.polarity
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return 0
    
    def analyze_tweets(self, tweets):
        """
        Analyze the sentiment of multiple tweets.
        
        Args:
            tweets (list): List of tweet dictionaries with 'content' field
            
        Returns:
            list: List of tweet dictionaries with added 'sentiment_score' field
        """
        for tweet in tweets:
            if 'content' in tweet:
                tweet['sentiment_score'] = self.analyze_text(tweet['content'])
        
        return tweets
    
    def get_sentiment_label(self, score):
        """
        Convert a sentiment score to a label.
        
        Args:
            score (float): Sentiment score between -1 and 1
            
        Returns:
            str: Sentiment label ('positive', 'negative', or 'neutral')
        """
        if score > 0.1:
            return 'positive'
        elif score < -0.1:
            return 'negative'
        else:
            return 'neutral'
