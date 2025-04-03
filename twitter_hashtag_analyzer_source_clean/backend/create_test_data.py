import sqlite3
import os
import json
from datetime import datetime

# Create test database file
DB_PATH = 'test_hashtag_analyzer.db'

# Initialize database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.executescript('''
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
''')

# Insert test hashtag
cursor.execute(
    "INSERT INTO hashtags (name, total_tweets, total_contributors, sentiment_score) VALUES (?, ?, ?, ?)",
    ("TürkiyedeKadınOlmak", 23230, 3715, 9.91)
)
hashtag_id = cursor.lastrowid

# Insert test users with locations
test_users = [
    {
        "id": "user1",
        "username": "user1",
        "display_name": "User One",
        "followers_count": 554265,
        "location": "İstanbul, Türkiye"
    },
    {
        "id": "user2",
        "username": "user2",
        "display_name": "User Two",
        "followers_count": 258110,
        "location": "Ankara, Türkiye"
    },
    {
        "id": "user3",
        "username": "user3",
        "display_name": "User Three",
        "followers_count": 228708,
        "location": "İzmir, Türkiye"
    },
    {
        "id": "user4",
        "username": "user4",
        "display_name": "User Four",
        "followers_count": 150000,
        "location": "Bursa, Türkiye"
    },
    {
        "id": "user5",
        "username": "user5",
        "display_name": "User Five",
        "followers_count": 120000,
        "location": "Antalya, Türkiye"
    }
]

for user in test_users:
    cursor.execute(
        """
        INSERT INTO users 
        (id, username, display_name, followers_count, location)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user["id"], user["username"], user["display_name"], user["followers_count"], user["location"])
    )

# Insert test locations
test_locations = [
    {
        "location_text": "İstanbul, Türkiye",
        "latitude": 41.0082,
        "longitude": 28.9784,
        "country": "Türkiye",
        "city": "İstanbul"
    },
    {
        "location_text": "Ankara, Türkiye",
        "latitude": 39.9334,
        "longitude": 32.8597,
        "country": "Türkiye",
        "city": "Ankara"
    },
    {
        "location_text": "İzmir, Türkiye",
        "latitude": 38.4237,
        "longitude": 27.1428,
        "country": "Türkiye",
        "city": "İzmir"
    },
    {
        "location_text": "Bursa, Türkiye",
        "latitude": 40.1885,
        "longitude": 29.0610,
        "country": "Türkiye",
        "city": "Bursa"
    },
    {
        "location_text": "Antalya, Türkiye",
        "latitude": 36.8969,
        "longitude": 30.7133,
        "country": "Türkiye",
        "city": "Antalya"
    }
]

for location in test_locations:
    cursor.execute(
        """
        INSERT INTO locations 
        (location_text, latitude, longitude, country, city, is_geocoded)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            location["location_text"],
            location["latitude"],
            location["longitude"],
            location["country"],
            location["city"],
            True
        )
    )
    location_id = cursor.lastrowid
    
    # Link user to location
    user_id = f"user{test_locations.index(location) + 1}"
    cursor.execute(
        "INSERT INTO user_locations (user_id, location_id) VALUES (?, ?)",
        (user_id, location_id)
    )

# Insert test tweets
test_tweets = [
    {
        "id": "tweet1",
        "user_id": "user1",
        "content": "Türkiye'de kadın olmak çok güzel ama aynı zamanda zorlukları da var. #TürkiyedeKadınOlmak",
        "created_at": "2025-04-01 12:00:00",
        "retweet_count": 100,
        "like_count": 200,
        "reply_count": 30,
        "is_retweet": False,
        "is_reply": False,
        "has_media": False,
        "sentiment_score": 9.5
    },
    {
        "id": "tweet2",
        "user_id": "user2",
        "content": "Kadınlarımız her alanda başarılı oluyorlar. Gurur duyuyoruz! #TürkiyedeKadınOlmak",
        "created_at": "2025-04-01 13:00:00",
        "retweet_count": 150,
        "like_count": 300,
        "reply_count": 40,
        "is_retweet": False,
        "is_reply": False,
        "has_media": True,
        "sentiment_score": 9.8
    },
    {
        "id": "tweet3",
        "user_id": "user3",
        "content": "Kadınların eğitim ve iş hayatında daha fazla fırsat eşitliğine ihtiyacı var. #TürkiyedeKadınOlmak",
        "created_at": "2025-04-01 14:00:00",
        "retweet_count": 200,
        "like_count": 400,
        "reply_count": 50,
        "is_retweet": False,
        "is_reply": False,
        "has_media": False,
        "sentiment_score": 8.5
    },
    {
        "id": "tweet4",
        "user_id": "user4",
        "content": "Kadına şiddet son bulsun! Daha güvenli bir toplum için el ele verelim. #TürkiyedeKadınOlmak",
        "created_at": "2025-04-01 15:00:00",
        "retweet_count": 300,
        "like_count": 500,
        "reply_count": 60,
        "is_retweet": False,
        "is_reply": False,
        "has_media": True,
        "sentiment_score": 7.5
    },
    {
        "id": "tweet5",
        "user_id": "user5",
        "content": "Türk kadını güçlüdür, çalışkandır, fedakardır. Tüm kadınlarımızın yanındayız. #TürkiyedeKadınOlmak",
        "created_at": "2025-04-01 16:00:00",
        "retweet_count": 250,
        "like_count": 450,
        "reply_count": 55,
        "is_retweet": False,
        "is_reply": False,
        "has_media": False,
        "sentiment_score": 9.7
    }
]

for tweet in test_tweets:
    cursor.execute(
        """
        INSERT INTO tweets 
        (id, hashtag_id, user_id, content, created_at, 
        retweet_count, like_count, reply_count, 
        is_retweet, is_reply, has_media, sentiment_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tweet["id"],
            hashtag_id,
            tweet["user_id"],
            tweet["content"],
            tweet["created_at"],
            tweet["retweet_count"],
            tweet["like_count"],
            tweet["reply_count"],
            tweet["is_retweet"],
            tweet["is_reply"],
            tweet["has_media"],
            tweet["sentiment_score"]
        )
    )

# Insert test hashtag stats
cursor.execute(
    """
    INSERT INTO hashtag_stats
    (hashtag_id, timestamp, tweet_count, contributor_count, 
    retweet_count, reply_count, media_count, sentiment_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        hashtag_id,
        "2025-04-03 15:00:00",
        23230,
        3715,
        21685,
        493,
        894,
        9.91
    )
)

# Insert test top contributors
for i, user in enumerate(test_users):
    influence_score = 10.0 - (i * 0.5)  # Decreasing influence score
    cursor.execute(
        """
        INSERT INTO top_contributors
        (hashtag_id, user_id, tweet_count, retweet_count, reply_count, influence_score)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            hashtag_id,
            user["id"],
            100 - (i * 20),  # Decreasing tweet count
            50 - (i * 10),   # Decreasing retweet count
            10 - (i * 2),    # Decreasing reply count
            influence_score
        )
    )

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Test database created at {DB_PATH} with sample data for hashtag #TürkiyedeKadınOlmak")
