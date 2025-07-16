"""
URL validation utilities
"""

import re
from urllib.parse import urlparse, urlunparse
from typing import Optional


class URLValidator:
    """URL validation and normalization utilities"""
    
    ALLOWED_SCHEMES = ['http', 'https']
    BLOCKED_DOMAINS = [
        'localhost', '127.0.0.1', '10.', '192.168.', '172.',
        'internal', 'local', 'test'
    ]
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL for analysis
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid for analysis
        """
        try:
            # Basic URL parsing
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in URLValidator.ALLOWED_SCHEMES:
                return False
            
            # Check if domain is present
            if not parsed.netloc:
                return False
            
            # Check for blocked domains (prevent SSRF)
            netloc_lower = parsed.netloc.lower()
            for blocked in URLValidator.BLOCKED_DOMAINS:
                if blocked in netloc_lower:
                    return False
            
            # Basic domain validation
            domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-._]*[a-zA-Z0-9]$'
            if not re.match(domain_pattern, parsed.netloc.split(':')[0]):
                return False
            
            # Check for reasonable domain length
            if len(parsed.netloc) > 253:  # Max domain length
                return False
            
            return True
            
        except Exception:
            return False
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize URL for consistent caching
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        try:
            parsed = urlparse(url)
            
            # Normalize scheme to lowercase
            scheme = parsed.scheme.lower()
            
            # Normalize netloc to lowercase
            netloc = parsed.netloc.lower()
            
            # Remove default ports
            if (scheme == 'http' and netloc.endswith(':80')) or \
               (scheme == 'https' and netloc.endswith(':443')):
                netloc = netloc.rsplit(':', 1)[0]
            
            # Normalize path
            path = parsed.path or '/'
            if not path.startswith('/'):
                path = '/' + path
            
            # Remove fragment
            fragment = ''
            
            # Keep query parameters but sort them for consistency
            query = parsed.query
            
            normalized = urlunparse((
                scheme, netloc, path, parsed.params, query, fragment
            ))
            
            return normalized
            
        except Exception:
            return url
    
    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """
        Extract domain from URL
        
        Args:
            url: URL to extract domain from
            
        Returns:
            Domain name or None if invalid
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc.split(':')[0].lower()
        except Exception:
            return None
    
    @staticmethod
    def is_same_domain(url1: str, url2: str) -> bool:
        """
        Check if two URLs belong to the same domain
        
        Args:
            url1: First URL
            url2: Second URL
            
        Returns:
            True if same domain
        """
        domain1 = URLValidator.extract_domain(url1)
        domain2 = URLValidator.extract_domain(url2)
        
        return domain1 is not None and domain1 == domain2 