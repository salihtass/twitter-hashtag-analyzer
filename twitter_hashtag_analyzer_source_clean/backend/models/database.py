import sqlite3
import os
import json
from datetime import datetime

class Database:
    def __init__(self, db_path='twitter_hashtag_analyzer.db'):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables based on the schema."""
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS hashtags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_tweets INTEGER DEFAULT 0,
            total_contributors INTEGER DEFAULT 0,
            sentiment_score REAL DEFAULT 0,
            UNIQUE(name)
        );

        CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            hashtag_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            retweet_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            is_retweet BOOLEAN DEFAULT FALSE,
            is_reply BOOLEAN DEFAULT FALSE,
            has_media BOOLEAN DEFAULT FALSE,
            sentiment_score REAL DEFAULT 0,
            FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            display_name TEXT,
            profile_image_url TEXT,
            followers_count INTEGER DEFAULT 0,
            following_count INTEGER DEFAULT 0,
            tweet_count INTEGER DEFAULT 0,
            location TEXT,
            account_created_at TIMESTAMP,
            is_verified BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_text TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            country TEXT,
            city TEXT,
            is_geocoded BOOLEAN DEFAULT FALSE,
            UNIQUE(location_text)
        );

        CREATE TABLE IF NOT EXISTS user_locations (
            user_id TEXT NOT NULL,
            location_id INTEGER NOT NULL,
            PRIMARY KEY (user_id, location_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (location_id) REFERENCES locations(id)
        );

        CREATE TABLE IF NOT EXISTS hashtag_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashtag_id INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            tweet_count INTEGER DEFAULT 0,
            contributor_count INTEGER DEFAULT 0,
            retweet_count INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            media_count INTEGER DEFAULT 0,
            sentiment_score REAL DEFAULT 0,
            FOREIGN KEY (hashtag_id) REFERENCES hashtags(id)
        );

        CREATE TABLE IF NOT EXISTS top_contributors (
            hashtag_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            tweet_count INTEGER DEFAULT 0,
            retweet_count INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            influence_score REAL DEFAULT 0,
            PRIMARY KEY (hashtag_id, user_id),
            FOREIGN KEY (hashtag_id) REFERENCES hashtags(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_tweets_hashtag_id ON tweets(hashtag_id);
        CREATE INDEX IF NOT EXISTS idx_tweets_user_id ON tweets(user_id);
        CREATE INDEX IF NOT EXISTS idx_tweets_created_at ON tweets(created_at);
        CREATE INDEX IF NOT EXISTS idx_users_location ON users(location);
        CREATE INDEX IF NOT EXISTS idx_hashtag_stats_hashtag_id ON hashtag_stats(hashtag_id);
        CREATE INDEX IF NOT EXISTS idx_hashtag_stats_timestamp ON hashtag_stats(timestamp);
        CREATE INDEX IF NOT EXISTS idx_locations_country_city ON locations(country, city);
        ''')
        self.conn.commit()
    
    def get_or_create_hashtag(self, hashtag_name):
        """Get a hashtag by name or create it if it doesn't exist."""
        self.cursor.execute(
            "SELECT * FROM hashtags WHERE name = ?", 
            (hashtag_name,)
        )
        hashtag = self.cursor.fetchone()
        
        if not hashtag:
            self.cursor.execute(
                "INSERT INTO hashtags (name) VALUES (?)",
                (hashtag_name,)
            )
            self.conn.commit()
            return self.get_or_create_hashtag(hashtag_name)
        
        return dict(hashtag)
    
    def save_tweet(self, tweet_data, hashtag_id):
        """Save a tweet to the database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO tweets 
                (id, hashtag_id, user_id, content, created_at, 
                retweet_count, like_count, reply_count, 
                is_retweet, is_reply, has_media, sentiment_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tweet_data['id'],
                    hashtag_id,
                    tweet_data['user_id'],
                    tweet_data['content'],
                    tweet_data['created_at'],
                    tweet_data.get('retweet_count', 0),
                    tweet_data.get('like_count', 0),
                    tweet_data.get('reply_count', 0),
                    tweet_data.get('is_retweet', False),
                    tweet_data.get('is_reply', False),
                    tweet_data.get('has_media', False),
                    tweet_data.get('sentiment_score', 0)
                )
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Tweet already exists
            return False
    
    def save_user(self, user_data):
        """Save a user to the database."""
        try:
            self.cursor.execute(
                """
                INSERT INTO users 
                (id, username, display_name, profile_image_url, 
                followers_count, following_count, tweet_count, 
                location, account_created_at, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_data['id'],
                    user_data['username'],
                    user_data.get('display_name', ''),
                    user_data.get('profile_image_url', ''),
                    user_data.get('followers_count', 0),
                    user_data.get('following_count', 0),
                    user_data.get('tweet_count', 0),
                    user_data.get('location', ''),
                    user_data.get('account_created_at', ''),
                    user_data.get('is_verified', False)
                )
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # User already exists, update instead
            self.cursor.execute(
                """
                UPDATE users SET
                username = ?,
                display_name = ?,
                profile_image_url = ?,
                followers_count = ?,
                following_count = ?,
                tweet_count = ?,
                location = ?,
                account_created_at = ?,
                is_verified = ?
                WHERE id = ?
                """,
                (
                    user_data['username'],
                    user_data.get('display_name', ''),
                    user_data.get('profile_image_url', ''),
                    user_data.get('followers_count', 0),
                    user_data.get('following_count', 0),
                    user_data.get('tweet_count', 0),
                    user_data.get('location', ''),
                    user_data.get('account_created_at', ''),
                    user_data.get('is_verified', False),
                    user_data['id']
                )
            )
            self.conn.commit()
            return True
    
    def save_location(self, location_text, latitude=None, longitude=None, country=None, city=None):
        """Save a location to the database."""
        if not location_text:
            return None
            
        try:
            self.cursor.execute(
                """
                INSERT INTO locations 
                (location_text, latitude, longitude, country, city, is_geocoded)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    location_text,
                    latitude,
                    longitude,
                    country,
                    city,
                    bool(latitude and longitude)
                )
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Location already exists, get its ID
            self.cursor.execute(
                "SELECT id FROM locations WHERE location_text = ?",
                (location_text,)
            )
            location = self.cursor.fetchone()
            
            # If coordinates are provided, update them
            if latitude and longitude and location:
                self.cursor.execute(
                    """
                    UPDATE locations SET
                    latitude = ?,
                    longitude = ?,
                    country = ?,
                    city = ?,
                    is_geocoded = TRUE
                    WHERE id = ?
                    """,
                    (latitude, longitude, country, city, location['id'])
                )
                self.conn.commit()
                
            return location['id'] if location else None
    
    def link_user_location(self, user_id, location_id):
        """Link a user to a location."""
        if not user_id or not location_id:
            return False
            
        try:
            self.cursor.execute(
                """
                INSERT INTO user_locations 
                (user_id, location_id)
                VALUES (?, ?)
                """,
                (user_id, location_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Relationship already exists
            return False
    
    def update_hashtag_stats(self, hashtag_id):
        """Update statistics for a hashtag."""
        # Get total tweets
        self.cursor.execute(
            "SELECT COUNT(*) as count FROM tweets WHERE hashtag_id = ?",
            (hashtag_id,)
        )
        total_tweets = self.cursor.fetchone()['count']
        
        # Get total contributors
        self.cursor.execute(
            "SELECT COUNT(DISTINCT user_id) as count FROM tweets WHERE hashtag_id = ?",
            (hashtag_id,)
        )
        total_contributors = self.cursor.fetchone()['count']
        
        # Get average sentiment score
        self.cursor.execute(
            "SELECT AVG(sentiment_score) as avg_score FROM tweets WHERE hashtag_id = ?",
            (hashtag_id,)
        )
        sentiment_score = self.cursor.fetchone()['avg_score'] or 0
        
        # Update hashtag record
        self.cursor.execute(
            """
            UPDATE hashtags SET
            total_tweets = ?,
            total_contributors = ?,
            sentiment_score = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (total_tweets, total_contributors, sentiment_score, hashtag_id)
        )
        self.conn.commit()
        
        # Create a new stats record
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get retweet count
        self.cursor.execute(
            "SELECT COUNT(*) as count FROM tweets WHERE hashtag_id = ? AND is_retweet = TRUE",
            (hashtag_id,)
        )
        retweet_count = self.cursor.fetchone()['count']
        
        # Get reply count
        self.cursor.execute(
            "SELECT COUNT(*) as count FROM tweets WHERE hashtag_id = ? AND is_reply = TRUE",
            (hashtag_id,)
        )
        reply_count = self.cursor.fetchone()['count']
        
        # Get media count
        self.cursor.execute(
            "SELECT COUNT(*) as count FROM tweets WHERE hashtag_id = ? AND has_media = TRUE",
            (hashtag_id,)
        )
        media_count = self.cursor.fetchone()['count']
        
        self.cursor.execute(
            """
            INSERT INTO hashtag_stats
            (hashtag_id, timestamp, tweet_count, contributor_count, 
            retweet_count, reply_count, media_count, sentiment_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hashtag_id,
                current_time,
                total_tweets,
                total_contributors,
                retweet_count,
                reply_count,
                media_count,
                sentiment_score
            )
        )
        self.conn.commit()
    
    def update_top_contributors(self, hashtag_id):
        """Update top contributors for a hashtag."""
        # Clear existing top contributors
        self.cursor.execute(
            "DELETE FROM top_contributors WHERE hashtag_id = ?",
            (hashtag_id,)
        )
        
        # Get top contributors by tweet count
        self.cursor.execute(
            """
            SELECT user_id, 
                COUNT(*) as tweet_count,
                SUM(CASE WHEN is_retweet = TRUE THEN 1 ELSE 0 END) as retweet_count,
                SUM(CASE WHEN is_reply = TRUE THEN 1 ELSE 0 END) as reply_count
            FROM tweets 
            WHERE hashtag_id = ?
            GROUP BY user_id
            ORDER BY tweet_count DESC
            LIMIT 50
            """,
            (hashtag_id,)
        )
        
        contributors = self.cursor.fetchall()
        
        for contributor in contributors:
            # Calculate influence score based on followers and engagement
            self.cursor.execute(
                "SELECT followers_count FROM users WHERE id = ?",
                (contributor['user_id'],)
            )
            user = self.cursor.fetchone()
            followers_count = user['followers_count'] if user else 0
            
            # Simple influence score formula
            influence_score = (
                contributor['tweet_count'] * 1 + 
                contributor['retweet_count'] * 0.5 + 
                contributor['reply_count'] * 0.7 + 
                (followers_count / 1000)
            )
            
            self.cursor.execute(
                """
                INSERT INTO top_contributors
                (hashtag_id, user_id, tweet_count, retweet_count, reply_count, influence_score)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    hashtag_id,
                    contributor['user_id'],
                    contributor['tweet_count'],
                    contributor['retweet_count'],
                    contributor['reply_count'],
                    influence_score
                )
            )
        
        self.conn.commit()
    
    def get_hashtag_summary(self, hashtag_id):
        """Get summary statistics for a hashtag."""
        self.cursor.execute(
            "SELECT * FROM hashtags WHERE id = ?",
            (hashtag_id,)
        )
        hashtag = self.cursor.fetchone()
        
        if not hashtag:
            return None
        
        # Get tweet type breakdown
        self.cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN is_retweet = FALSE AND is_reply = FALSE THEN 1 ELSE 0 END) as original_count,
                SUM(CASE WHEN is_retweet = TRUE THEN 1 ELSE 0 END) as retweet_count,
                SUM(CASE WHEN is_reply = TRUE THEN 1 ELSE 0 END) as reply_count,
                SUM(CASE WHEN has_media = TRUE THEN 1 ELSE 0 END) as media_count
            FROM tweets 
            WHERE hashtag_id = ?
            """,
            (hashtag_id,)
        )
        tweet_types = self.cursor.fetchone()
        
        # Get time-based activity
        self.cursor.execute(
            """
            SELECT 
                strftime('%Y-%m-%d %H:00:00', created_at) as hour,
                COUNT(*) as tweet_count,
                COUNT(DISTINCT user_id) as user_count
            FROM tweets 
            WHERE hashtag_id = ?
            GROUP BY hour
            ORDER BY hour
            """,
            (hashtag_id,)
        )
        activity = [dict(row) for row in self.cursor.fetchall()]
        
        # Get location data
        self.cursor.execute(
            """
            SELECT 
                l.location_text, l.latitude, l.longitude, l.country, l.city,
                COUNT(DISTINCT t.user_id) as user_count
            FROM tweets t
            JOIN users u ON t.user_id = u.id
            JOIN user_locations ul ON u.id = ul.user_id
            JOIN locations l ON ul.location_id = l.id
            WHERE t.hashtag_id = ? AND l.is_geocoded = TRUE
            GROUP BY l.id
            """,
            (hashtag_id,)
        )
        locations = [dict(row) for row in self.cursor.fetchall()]
        
        return {
            'hashtag': dict(hashtag),
            'tweet_types': dict(tweet_types) if tweet_types else {},
            'activity': activity,
            'locations': locations
        }
    
    def get_top_contributors(self, hashtag_id, limit=10):
        """Get top contributors for a hashtag."""
        self.cursor.execute(
            """
            SELECT tc.*, u.username, u.display_name, u.profile_image_url, u.followers_count
            FROM top_contributors tc
            JOIN users u ON tc.user_id = u.id
            WHERE tc.hashtag_id = ?
            ORDER BY tc.influence_score DESC
            LIMIT ?
            """,
            (hashtag_id, limit)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_sentiment_analysis(self, hashtag_id):
        """Get sentiment analysis for a hashtag."""
        # Get overall sentiment score
        self.cursor.execute(
            "SELECT sentiment_score FROM hashtags WHERE id = ?",
            (hashtag_id,)
        )
        overall_score = self.cursor.fetchone()['sentiment_score'] if self.cursor.fetchone() else 0
        
        # Get sentiment distribution
        self.cursor.execute(
            """
            SELECT 
                CASE 
                    WHEN sentiment_score > 0.5 THEN 'positive'
                    WHEN sentiment_score < -0.5 THEN 'negative'
                    ELSE 'neutral'
                END as sentiment,
                COUNT(*) as count
            FROM tweets 
            WHERE hashtag_id = ?
            GROUP BY sentiment
            """,
            (hashtag_id,)
        )
        distribution = {row['sentiment']: row['count'] for row in self.cursor.fetchall()}
        
        # Get sentiment over time
        self.cursor.execute(
            """
            SELECT 
                strftime('%Y-%m-%d %H:00:00', created_at) as hour,
                AVG(sentiment_score) as avg_score
            FROM tweets 
            WHERE hashtag_id = ?
            GROUP BY hour
            ORDER BY hour
            """,
            (hashtag_id,)
        )
        timeline = [dict(row) for row in self.cursor.fetchall()]
        
        return {
            'overall_score': overall_score,
            'distribution': distribution,
            'timeline': timeline
        }
    
    def get_location_stats(self, hashtag_id):
        """Get location statistics for a hashtag."""
        # Get country distribution
        self.cursor.execute(
            """
            SELECT 
                l.country,
                COUNT(DISTINCT t.user_id) as user_count
            FROM tweets t
            JOIN users u ON t.user_id = u.id
            JOIN user_locations ul ON u.id = ul.user_id
            JOIN locations l ON ul.location_id = l.id
            WHERE t.hashtag_id = ? AND l.country IS NOT NULL
            GROUP BY l.country
            ORDER BY user_count DESC
            """,
            (hashtag_id,)
        )
        countries = [dict(row) for row in self.cursor.fetchall()]
        
        # Get city distribution
        self.cursor.execute(
            """
            SELECT 
                l.city, l.country,
                COUNT(DISTINCT t.user_id) as user_count
            FROM tweets t
            JOIN users u ON t.user_id = u.id
            JOIN user_locations ul ON u.id = ul.user_id
            JOIN locations l ON ul.location_id = l.id
            WHERE t.hashtag_id = ? AND l.city IS NOT NULL
            GROUP BY l.city, l.country
            ORDER BY user_count DESC
            LIMIT 50
            """,
            (hashtag_id,)
        )
        cities = [dict(row) for row in self.cursor.fetchall()]
        
        # Get all geocoded locations
        self.cursor.execute(
            """
            SELECT 
                l.location_text, l.latitude, l.longitude, l.country, l.city,
                COUNT(DISTINCT t.user_id) as user_count
            FROM tweets t
            JOIN users u ON t.user_id = u.id
            JOIN user_locations ul ON u.id = ul.user_id
            JOIN locations l ON ul.location_id = l.id
            WHERE t.hashtag_id = ? AND l.is_geocoded = TRUE
            GROUP BY l.id
            """,
            (hashtag_id,)
        )
        locations = [dict(row) for row in self.cursor.fetchall()]
        
        return {
            'countries': countries,
            'cities': cities,
            'locations': locations
        }
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
