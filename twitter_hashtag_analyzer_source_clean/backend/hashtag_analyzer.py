import os
import sys
import json
from datetime import datetime

from models.database import Database
from services.twitter_service import TwitterService
from services.geocoding_service import GeocodingService
from services.sentiment_analyzer import SentimentAnalyzer

class HashtagAnalyzer:
    def __init__(self, db_path='twitter_hashtag_analyzer.db'):
        """
        Initialize the hashtag analyzer.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db = Database(db_path)
        self.twitter_service = TwitterService()
        self.geocoding_service = GeocodingService()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def analyze_hashtag(self, hashtag, count=100, search_type="Latest"):
        """
        Analyze a Twitter hashtag.
        
        Args:
            hashtag (str): Hashtag to analyze (with or without #)
            count (int): Number of tweets to retrieve
            search_type (str): Type of search (Top, Latest, Photos, Videos, People)
            
        Returns:
            dict: Analysis results
        """
        # Clean hashtag format
        clean_hashtag = hashtag.strip()
        if clean_hashtag.startswith('#'):
            clean_hashtag = clean_hashtag[1:]
        
        # Get or create hashtag record
        hashtag_record = self.db.get_or_create_hashtag(clean_hashtag)
        hashtag_id = hashtag_record['id']
        
        # Collect tweets
        collected_data = self._collect_tweets(clean_hashtag, hashtag_id, count, search_type)
        
        # Process locations
        self._process_locations(collected_data['users'])
        
        # Update statistics
        self.db.update_hashtag_stats(hashtag_id)
        self.db.update_top_contributors(hashtag_id)
        
        # Get analysis results
        return self._get_analysis_results(hashtag_id)
    
    def _collect_tweets(self, hashtag, hashtag_id, count, search_type):
        """
        Collect tweets for a hashtag.
        
        Args:
            hashtag (str): Hashtag to collect tweets for
            hashtag_id (int): Database ID of the hashtag
            count (int): Number of tweets to retrieve
            search_type (str): Type of search
            
        Returns:
            dict: Collected data including tweets and users
        """
        collected_data = {
            'tweets': [],
            'users': {}
        }
        
        # Format hashtag for search
        search_hashtag = f"#{hashtag}"
        
        # Search for tweets
        cursor = None
        remaining = count
        
        while remaining > 0:
            batch_count = min(remaining, 100)  # API limit per request
            
            # Search Twitter
            results = self.twitter_service.search_hashtag(
                search_hashtag, 
                count=batch_count,
                search_type=search_type,
                cursor=cursor
            )
            
            if not results or not results['tweets']:
                break
            
            # Process tweets
            tweets = results['tweets']
            users = results['users']
            
            # Analyze sentiment
            tweets = self.sentiment_analyzer.analyze_tweets(tweets)
            
            # Save tweets and users to database
            for tweet in tweets:
                # Skip if missing essential data
                if not tweet.get('id') or not tweet.get('user_id'):
                    continue
                
                # Save tweet
                self.db.save_tweet(tweet, hashtag_id)
                collected_data['tweets'].append(tweet)
            
            # Save users
            for user_id, user in users.items():
                self.db.save_user(user)
                collected_data['users'][user_id] = user
            
            # Update remaining count
            remaining -= len(tweets)
            
            # Update cursor for pagination
            if results.get('cursor') and results['cursor'].get('bottom'):
                cursor = results['cursor']['bottom']
            else:
                break
        
        return collected_data
    
    def _process_locations(self, users):
        """
        Process and geocode user locations.
        
        Args:
            users (dict): Dictionary of user data
        """
        # Collect unique locations
        locations = set()
        for user_id, user in users.items():
            if user.get('location') and user['location'].strip():
                locations.add(user['location'].strip())
        
        # Geocode locations
        geocoded = self.geocoding_service.batch_geocode(list(locations))
        
        # Save locations and link to users
        for user_id, user in users.items():
            if not user.get('location') or not user['location'].strip():
                continue
                
            location_text = user['location'].strip()
            geo_data = geocoded.get(location_text)
            
            if geo_data:
                # Save location
                location_id = self.db.save_location(
                    location_text,
                    geo_data.get('latitude'),
                    geo_data.get('longitude'),
                    geo_data.get('country'),
                    geo_data.get('city')
                )
                
                # Link user to location
                if location_id:
                    self.db.link_user_location(user_id, location_id)
    
    def _get_analysis_results(self, hashtag_id):
        """
        Get analysis results for a hashtag.
        
        Args:
            hashtag_id (int): Database ID of the hashtag
            
        Returns:
            dict: Analysis results
        """
        # Get summary data
        summary = self.db.get_hashtag_summary(hashtag_id)
        
        # Get top contributors
        top_contributors = self.db.get_top_contributors(hashtag_id)
        
        # Get sentiment analysis
        sentiment = self.db.get_sentiment_analysis(hashtag_id)
        
        # Get location stats
        locations = self.db.get_location_stats(hashtag_id)
        
        return {
            'summary': summary,
            'top_contributors': top_contributors,
            'sentiment': sentiment,
            'locations': locations
        }
    
    def close(self):
        """Close database connection."""
        self.db.close()


# Main application controller
class HashtagAnalyzerApp:
    def __init__(self, db_path='twitter_hashtag_analyzer.db'):
        """
        Initialize the hashtag analyzer application.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.analyzer = HashtagAnalyzer(db_path)
    
    def analyze_hashtag(self, hashtag, count=100, search_type="Latest"):
        """
        Analyze a Twitter hashtag.
        
        Args:
            hashtag (str): Hashtag to analyze (with or without #)
            count (int): Number of tweets to retrieve
            search_type (str): Type of search (Top, Latest, Photos, Videos, People)
            
        Returns:
            dict: Analysis results
        """
        try:
            return self.analyzer.analyze_hashtag(hashtag, count, search_type)
        except Exception as e:
            print(f"Error analyzing hashtag: {str(e)}")
            return {"error": str(e)}
    
    def close(self):
        """Close the application."""
        self.analyzer.close()


# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hashtag_analyzer.py <hashtag> [count] [search_type]")
        sys.exit(1)
    
    hashtag = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    search_type = sys.argv[3] if len(sys.argv) > 3 else "Latest"
    
    app = HashtagAnalyzerApp()
    results = app.analyze_hashtag(hashtag, count, search_type)
    
    # Print summary
    if 'summary' in results and 'hashtag' in results['summary']:
        hashtag_data = results['summary']['hashtag']
        print(f"Hashtag: #{hashtag_data['name']}")
        print(f"Total tweets: {hashtag_data['total_tweets']}")
        print(f"Total contributors: {hashtag_data['total_contributors']}")
        print(f"Sentiment score: {hashtag_data['sentiment_score']:.2f}")
    
    # Save results to file
    output_file = f"{hashtag}_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Full analysis saved to {output_file}")
    
    app.close()
