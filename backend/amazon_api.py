"""Amazon Product Advertising API Integration for Gift Recommender System"""

import os
import time
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

try:
    from amazon_paapi import AmazonApi
except ImportError:
    AmazonApi = None
    print("⚠️  amazon_paapi not installed. Run: pip install python-amazon-paapi")

@dataclass
class AmazonProduct:
    """Amazon product data structure"""
    asin: str
    title: str
    price: float
    currency: str = "USD"
    image_url: str = ""
    rating: float = 0.0
    review_count: int = 0
    affiliate_url: str = ""
    availability: str = "Available"
    brand: str = ""
    color: str = ""
    category: str = ""
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'asin': self.asin,
            'title': self.title,
            'price': self.price,
            'currency': self.currency,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'affiliate_url': self.affiliate_url,
            'availability': self.availability,
            'brand': self.brand,
            'color': self.color,
            'category': self.category,
            'description': self.description,
            'keywords': self.keywords
        }

class AmazonAPIManager:
    """Manages Amazon Product Advertising API interactions"""
    
    def __init__(self):
        self.api: Optional[AmazonApi] = None
        self.last_request_time = 0
        self.throttle_delay = 1.5  # seconds between requests
        self.cache: Dict[str, Dict] = {}
        self.cache_ttl = 3600  # 1 hour cache
        self.logger = logging.getLogger(__name__)
        
        # Initialize API if credentials are available
        self._initialize_api()
    
    def _initialize_api(self) -> bool:
        """Initialize Amazon API with credentials"""
        try:
            # Try to get credentials from environment variables
            key = os.getenv('AMAZON_API_KEY')
            secret = os.getenv('AMAZON_API_SECRET')
            tag = os.getenv('AMAZON_ASSOCIATE_TAG')
            country = os.getenv('AMAZON_COUNTRY', 'US')
            
            if not all([key, secret, tag]):
                self.logger.warning("Amazon API credentials not found in environment variables")
                return False
            
            if not AmazonApi:
                self.logger.error("amazon_paapi package not installed")
                return False
            
            self.api = AmazonApi(
                key=key,
                secret=secret, 
                tag=tag,
                country=country,
                throttling=self.throttle_delay
            )
            
            self.logger.info(f"Amazon API initialized for country: {country}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Amazon API: {e}")
            return False
    
    def _wait_for_throttle(self):
        """Implement throttling to respect API limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.throttle_delay:
            wait_time = self.throttle_delay - time_since_last
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        cache_time = self.cache[key].get('timestamp', 0)
        return time.time() - cache_time < self.cache_ttl
    
    def search_products(self, 
                      keywords: str, 
                      category: str = None,
                      min_price: int = None,
                      max_price: int = None,
                      max_results: int = 10) -> List[AmazonProduct]:
        """Search Amazon products by keywords"""
        
        if not self.api:
            self.logger.warning("Amazon API not available, returning empty results")
            return []
        
        # Create cache key
        cache_key = f"{keywords}_{category}_{min_price}_{max_price}_{max_results}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            self.logger.info(f"Returning cached results for: {keywords}")
            return [AmazonProduct(**item) for item in self.cache[cache_key]['data']]
        
        try:
            self._wait_for_throttle()
            
            # Search parameters
            search_params = {
                'keywords': keywords,
                'item_count': max_results
            }
            
            if min_price:
                search_params['min_price'] = min_price * 100  # Convert to cents
            if max_price:
                search_params['max_price'] = max_price * 100  # Convert to cents
            
            # Execute search
            search_result = self.api.search_items(**search_params)
            
            products = []
            for item in search_result.items:
                try:
                    product = self._parse_amazon_item(item)
                    if product:
                        products.append(product)
                except Exception as e:
                    self.logger.error(f"Error parsing item: {e}")
                    continue
            
            # Cache results
            self.cache[cache_key] = {
                'data': [p.to_dict() for p in products],
                'timestamp': time.time()
            }
            
            self.logger.info(f"Found {len(products)} products for: {keywords}")
            return products
            
        except Exception as e:
            self.logger.error(f"Amazon API search failed: {e}")
            return []
    
    def get_product_details(self, asins: List[str]) -> List[AmazonProduct]:
        """Get detailed product information by ASINs"""
        
        if not self.api:
            return []
        
        try:
            self._wait_for_throttle()
            items = self.api.get_items(asins)
            
            products = []
            for item in items:
                product = self._parse_amazon_item(item)
                if product:
                    products.append(product)
            
            return products
            
        except Exception as e:
            self.logger.error(f"Failed to get product details: {e}")
            return []
    
    def _parse_amazon_item(self, item) -> Optional[AmazonProduct]:
        """Parse Amazon API item response into AmazonProduct"""
        try:
            # Basic product info
            asin = getattr(item, 'asin', '')
            title = ''
            if hasattr(item, 'item_info') and hasattr(item.item_info, 'title'):
                title = getattr(item.item_info.title, 'display_value', '')
            
            # Price information
            price = 0.0
            currency = 'USD'
            
            if hasattr(item, 'offers') and item.offers and item.offers.listings:
                listing = item.offers.listings[0]
                if hasattr(listing, 'price') and listing.price:
                    price = float(listing.price.amount or 0) / 100  # Convert from cents
                    currency = getattr(listing.price, 'currency', 'USD')
            
            # Images
            image_url = ''
            if hasattr(item, 'images') and item.images and hasattr(item.images, 'primary'):
                if hasattr(item.images.primary, 'large'):
                    image_url = getattr(item.images.primary.large, 'url', '')
                elif hasattr(item.images.primary, 'medium'):
                    image_url = getattr(item.images.primary.medium, 'url', '')
            
            # Reviews and ratings
            rating = 0.0
            review_count = 0
            
            if hasattr(item, 'customer_reviews') and item.customer_reviews:
                if hasattr(item.customer_reviews, 'star_rating'):
                    rating_text = getattr(item.customer_reviews.star_rating, 'value', '0')
                    try:
                        rating = float(rating_text.split()[0]) if rating_text else 0.0
                    except:
                        rating = 0.0
                
                if hasattr(item.customer_reviews, 'count'):
                    review_count = getattr(item.customer_reviews.count, 'value', 0) or 0
            
            # Affiliate URL
            affiliate_url = getattr(item, 'detail_page_url', '')
            
            # Additional product info
            brand = ''
            color = ''
            if hasattr(item, 'item_info'):
                if hasattr(item.item_info, 'by_line_info'):
                    brand = getattr(item.item_info.by_line_info, 'brand', {}).get('display_value', '')
                
                if hasattr(item.item_info, 'product_info'):
                    color = getattr(item.item_info.product_info, 'color', {}).get('display_value', '')
            
            return AmazonProduct(
                asin=asin,
                title=title,
                price=price,
                currency=currency,
                image_url=image_url,
                rating=rating,
                review_count=review_count,
                affiliate_url=affiliate_url,
                brand=brand,
                color=color,
                keywords=[]
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing Amazon item: {e}")
            return None
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get API status information"""
        return {
            'api_available': self.api is not None,
            'cache_entries': len(self.cache),
            'last_request_time': self.last_request_time,
            'throttle_delay': self.throttle_delay
        }

# Global API manager instance
amazon_api = AmazonAPIManager()
