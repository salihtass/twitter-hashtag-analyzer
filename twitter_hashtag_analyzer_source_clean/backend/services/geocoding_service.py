import requests
import json
import time

class GeocodingService:
    def __init__(self, cache_file='location_cache.json'):
        """
        Initialize the geocoding service.
        
        Args:
            cache_file (str): Path to the location cache file
        """
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self):
        """Load the location cache from file."""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_cache(self):
        """Save the location cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def geocode(self, location_text):
        """
        Convert a location text to geographic coordinates.
        
        Args:
            location_text (str): Location text to geocode
            
        Returns:
            dict: Location data with coordinates or None if geocoding failed
        """
        if not location_text or location_text.strip() == '':
            return None
        
        # Check cache first
        if location_text in self.cache:
            return self.cache[location_text]
        
        # Use OpenStreetMap Nominatim API for geocoding
        try:
            # Add a small delay to respect rate limits
            time.sleep(1)
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": location_text,
                "format": "json",
                "limit": 1,
                "addressdetails": 1
            }
            headers = {
                "User-Agent": "TwitterHashtagAnalyzer/1.0"
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    result = data[0]
                    
                    # Extract location data
                    location_data = {
                        "latitude": float(result["lat"]),
                        "longitude": float(result["lon"]),
                        "country": result.get("address", {}).get("country", ""),
                        "city": result.get("address", {}).get("city", "") or 
                               result.get("address", {}).get("town", "") or 
                               result.get("address", {}).get("village", "")
                    }
                    
                    # Cache the result
                    self.cache[location_text] = location_data
                    self._save_cache()
                    
                    return location_data
        
        except Exception as e:
            print(f"Error geocoding location '{location_text}': {str(e)}")
        
        # Return None if geocoding failed
        return None
    
    def batch_geocode(self, locations):
        """
        Geocode multiple locations.
        
        Args:
            locations (list): List of location texts to geocode
            
        Returns:
            dict: Dictionary mapping location texts to geocoded data
        """
        results = {}
        
        for location in locations:
            if not location or location.strip() == '':
                continue
                
            results[location] = self.geocode(location)
        
        return results
