import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient
import json
from datetime import datetime

class TwitterService:
    def __init__(self):
        """Initialize the Twitter API client."""
        self.client = ApiClient()
    
    def search_hashtag(self, hashtag, count=100, search_type="Latest", cursor=None):
        """
        Search for tweets containing a specific hashtag.
        
        Args:
            hashtag (str): The hashtag to search for (with or without #)
            count (int): Number of tweets to retrieve
            search_type (str): Type of search (Top, Latest, Photos, Videos, People)
            cursor (str): Pagination cursor for retrieving more results
            
        Returns:
            dict: Search results containing tweets and user data
        """
        # Ensure hashtag format is correct (with #)
        if not hashtag.startswith('#'):
            hashtag = f"#{hashtag}"
            
        # Call Twitter search API
        response = self.client.call_api(
            'Twitter/search_twitter', 
            query={
                'query': hashtag,
                'count': count,
                'type': search_type,
                'cursor': cursor if cursor else ''
            }
        )
        
        # Process and return the results
        return self._process_search_results(response, hashtag)
    
    def get_user_profile(self, username):
        """
        Get detailed profile information for a Twitter user.
        
        Args:
            username (str): Twitter username (without @)
            
        Returns:
            dict: User profile data
        """
        # Remove @ if present
        if username.startswith('@'):
            username = username[1:]
            
        # Call Twitter user profile API
        response = self.client.call_api(
            'Twitter/get_user_profile_by_username',
            query={'username': username}
        )
        
        # Process and return the user data
        return self._process_user_profile(response)
    
    def _process_search_results(self, response, hashtag):
        """
        Process raw Twitter search API response into structured data.
        
        Args:
            response (dict): Raw API response
            hashtag (str): The hashtag that was searched
            
        Returns:
            dict: Processed tweets and user data
        """
        processed_data = {
            'tweets': [],
            'users': {},
            'cursor': None
        }
        
        if not response or 'result' not in response:
            return processed_data
            
        # Extract cursor for pagination
        if 'cursor' in response:
            processed_data['cursor'] = {
                'top': response['cursor'].get('top', ''),
                'bottom': response['cursor'].get('bottom', '')
            }
        
        # Extract tweets and user data from the timeline
        try:
            timeline = response['result']['timeline']
            instructions = timeline.get('instructions', [])
            
            for instruction in instructions:
                if 'entries' not in instruction:
                    continue
                    
                for entry in instruction['entries']:
                    if 'content' not in entry:
                        continue
                        
                    content = entry['content']
                    
                    # Skip non-tweet entries
                    if content.get('entryType') != 'TimelineTimelineItem':
                        continue
                        
                    # Process tweet items
                    if 'items' in content:
                        for item_wrapper in content['items']:
                            if 'item' not in item_wrapper:
                                continue
                                
                            item = item_wrapper['item']
                            if 'itemContent' not in item:
                                continue
                                
                            item_content = item['itemContent']
                            
                            # Skip non-tweet content
                            if item_content.get('itemType') != 'TimelineTweet':
                                continue
                                
                            # Extract user data
                            if 'user_results' in item_content and 'result' in item_content['user_results']:
                                user_data = item_content['user_results']['result']
                                user = self._extract_user_data(user_data)
                                if user:
                                    processed_data['users'][user['id']] = user
                            
                            # Extract tweet data
                            if 'tweet_results' in item_content and 'result' in item_content['tweet_results']:
                                tweet_data = item_content['tweet_results']['result']
                                tweet = self._extract_tweet_data(tweet_data, hashtag)
                                if tweet:
                                    processed_data['tweets'].append(tweet)
        except Exception as e:
            print(f"Error processing search results: {str(e)}")
        
        return processed_data
    
    def _process_user_profile(self, response):
        """
        Process raw Twitter user profile API response.
        
        Args:
            response (dict): Raw API response
            
        Returns:
            dict: Processed user profile data
        """
        if not response or 'result' not in response or 'data' not in response['result']:
            return None
            
        try:
            user_data = response['result']['data']['user']['result']
            return self._extract_user_data(user_data)
        except Exception as e:
            print(f"Error processing user profile: {str(e)}")
            return None
    
    def _extract_user_data(self, user_data):
        """
        Extract relevant user data from Twitter API response.
        
        Args:
            user_data (dict): Raw user data from API
            
        Returns:
            dict: Processed user data
        """
        if not user_data or '__typename' not in user_data:
            return None
            
        try:
            user = {}
            
            # Basic user info
            user['id'] = user_data.get('rest_id', '')
            
            # Legacy data contains most user information
            if 'legacy' in user_data:
                legacy = user_data['legacy']
                user['username'] = legacy.get('screen_name', '')
                user['display_name'] = legacy.get('name', '')
                user['profile_image_url'] = legacy.get('profile_image_url_https', '')
                user['followers_count'] = legacy.get('followers_count', 0)
                user['following_count'] = legacy.get('friends_count', 0)
                user['tweet_count'] = legacy.get('statuses_count', 0)
                user['location'] = legacy.get('location', '')
                
                # Parse created_at date
                if 'created_at' in legacy:
                    try:
                        created_at = datetime.strptime(legacy['created_at'], '%a %b %d %H:%M:%S %z %Y')
                        user['account_created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        user['account_created_at'] = ''
                
                user['is_verified'] = legacy.get('verified', False) or user_data.get('is_blue_verified', False)
            
            return user
        except Exception as e:
            print(f"Error extracting user data: {str(e)}")
            return None
    
    def _extract_tweet_data(self, tweet_data, hashtag):
        """
        Extract relevant tweet data from Twitter API response.
        
        Args:
            tweet_data (dict): Raw tweet data from API
            hashtag (str): The hashtag that was searched
            
        Returns:
            dict: Processed tweet data
        """
        if not tweet_data or '__typename' not in tweet_data:
            return None
            
        try:
            tweet = {}
            
            # Core tweet data
            tweet['id'] = tweet_data.get('rest_id', '')
            
            # Legacy data contains most tweet information
            if 'legacy' in tweet_data:
                legacy = tweet_data['legacy']
                tweet['content'] = legacy.get('full_text', '')
                tweet['retweet_count'] = legacy.get('retweet_count', 0)
                tweet['like_count'] = legacy.get('favorite_count', 0)
                tweet['reply_count'] = legacy.get('reply_count', 0)
                
                # Parse created_at date
                if 'created_at' in legacy:
                    try:
                        created_at = datetime.strptime(legacy['created_at'], '%a %b %d %H:%M:%S %z %Y')
                        tweet['created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        tweet['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    tweet['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Check if it's a retweet
                tweet['is_retweet'] = 'retweeted_status_result' in legacy
                
                # Check if it's a reply
                tweet['is_reply'] = legacy.get('in_reply_to_status_id_str', '') != ''
                
                # Check if it has media
                tweet['has_media'] = 'entities' in legacy and 'media' in legacy['entities']
                
                # Get user ID
                tweet['user_id'] = legacy.get('user_id_str', '')
                
                # Set hashtag
                tweet['hashtag'] = hashtag
            
            return tweet
        except Exception as e:
            print(f"Error extracting tweet data: {str(e)}")
            return None
