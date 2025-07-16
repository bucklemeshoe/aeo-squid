"""
Technical SEO analysis for AEO optimization
"""

import aiohttp
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
from models.analysis import TechnicalResult


logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Technical SEO analysis for AEO optimization"""
    
    def __init__(self):
        """Initialize technical analyzer"""
        pass
    
    async def analyze(self, url: str) -> TechnicalResult:
        """
        Analyze technical SEO aspects important for AEO
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Technical analysis results
        """
        logger.info(f"Starting technical analysis for {url}")
        
        try:
            # Run all technical checks
            https_enabled = self._check_https(url)
            mobile_friendly = await self._check_mobile_friendly(url)
            sitemap_present = await self._check_sitemap(url)
            robots_present = await self._check_robots_txt(url)
            page_speed_score = await self._estimate_page_speed(url)
            cwv_passed = await self._check_core_web_vitals(url)
            
            result = TechnicalResult(
                https_enabled=https_enabled,
                mobile_friendly=mobile_friendly,
                sitemap_present=sitemap_present,
                robots_txt_present=robots_present,
                page_speed_score=page_speed_score,
                core_web_vitals_passed=cwv_passed
            )
            
            logger.info(f"Technical analysis completed for {url}")
            return result
            
        except Exception as e:
            logger.error(f"Technical analysis failed for {url}: {e}")
            return self._get_default_technical_result()
    
    def _check_https(self, url: str) -> bool:
        """
        Check if website uses HTTPS
        
        Args:
            url: Website URL
            
        Returns:
            True if HTTPS is enabled
        """
        try:
            parsed_url = urlparse(url)
            return parsed_url.scheme.lower() == 'https'
        except Exception as e:
            logger.error(f"Error checking HTTPS for {url}: {e}")
            return False
    
    async def _check_mobile_friendly(self, url: str) -> bool:
        """
        Check if website is mobile-friendly
        
        Args:
            url: Website URL
            
        Returns:
            True if mobile-friendly
        """
        try:
            # Fetch page with mobile user agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Check for mobile-friendly indicators
                        mobile_indicators = [
                            'viewport',
                            'responsive',
                            'mobile-friendly',
                            '@media',
                            'device-width'
                        ]
                        
                        content_lower = content.lower()
                        indicator_count = sum(1 for indicator in mobile_indicators if indicator in content_lower)
                        
                        # If we find multiple mobile indicators, likely mobile-friendly
                        return indicator_count >= 2
                    else:
                        return False
                        
        except Exception as e:
            logger.error(f"Error checking mobile-friendliness for {url}: {e}")
            return False
    
    async def _check_sitemap(self, url: str) -> bool:
        """
        Check if XML sitemap exists
        
        Args:
            url: Website URL
            
        Returns:
            True if sitemap found
        """
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Common sitemap locations
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/sitemaps.xml')
            ]
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                for sitemap_url in sitemap_urls:
                    try:
                        async with session.get(sitemap_url) as response:
                            if response.status == 200:
                                content = await response.text()
                                # Check if it's actually XML sitemap content
                                if '<sitemap' in content.lower() or '<urlset' in content.lower():
                                    logger.debug(f"Found sitemap at {sitemap_url}")
                                    return True
                    except Exception:
                        continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking sitemap for {url}: {e}")
            return False
    
    async def _check_robots_txt(self, url: str) -> bool:
        """
        Check if robots.txt exists
        
        Args:
            url: Website URL
            
        Returns:
            True if robots.txt found
        """
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            robots_url = urljoin(base_url, '/robots.txt')
            
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(robots_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        # Check if it's actually robots.txt content
                        robots_indicators = ['user-agent', 'disallow', 'allow', 'sitemap']
                        content_lower = content.lower()
                        
                        if any(indicator in content_lower for indicator in robots_indicators):
                            logger.debug(f"Found robots.txt at {robots_url}")
                            return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking robots.txt for {url}: {e}")
            return False
    
    async def _estimate_page_speed(self, url: str) -> int:
        """
        Estimate page speed score
        
        Args:
            url: Website URL
            
        Returns:
            Estimated page speed score (0-100)
        """
        try:
            import time
            start_time = time.time()
            
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        load_time = time.time() - start_time
                        
                        # Estimate score based on load time and content size
                        content_size = len(content)
                        
                        # Basic scoring algorithm
                        if load_time <= 1.0:
                            base_score = 90
                        elif load_time <= 2.0:
                            base_score = 80
                        elif load_time <= 3.0:
                            base_score = 70
                        elif load_time <= 5.0:
                            base_score = 60
                        else:
                            base_score = 40
                        
                        # Adjust for content size
                        if content_size > 1000000:  # > 1MB
                            base_score -= 10
                        elif content_size > 500000:  # > 500KB
                            base_score -= 5
                        
                        return max(0, min(100, base_score))
                    else:
                        return 0
                        
        except Exception as e:
            logger.error(f"Error estimating page speed for {url}: {e}")
            return 0
    
    async def _check_core_web_vitals(self, url: str) -> bool:
        """
        Basic check for Core Web Vitals readiness
        
        Args:
            url: Website URL
            
        Returns:
            True if likely to pass Core Web Vitals
        """
        try:
            # This is a simplified check - in production, you'd use PageSpeed Insights API
            page_speed = await self._estimate_page_speed(url)
            mobile_friendly = await self._check_mobile_friendly(url)
            
            # Basic heuristic: if page is fast and mobile-friendly, likely to pass CWV
            return page_speed >= 70 and mobile_friendly
            
        except Exception as e:
            logger.error(f"Error checking Core Web Vitals for {url}: {e}")
            return False
    
    async def _check_ssl_certificate(self, url: str) -> Dict[str, Any]:
        """
        Check SSL certificate details
        
        Args:
            url: Website URL
            
        Returns:
            SSL certificate information
        """
        try:
            import ssl
            import socket
            from urllib.parse import urlparse
            
            parsed_url = urlparse(url)
            if parsed_url.scheme != 'https':
                return {'valid': False, 'reason': 'Not HTTPS'}
            
            hostname = parsed_url.netloc.split(':')[0]
            port = parsed_url.port or 443
            
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect and get certificate
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        'valid': True,
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert['version'],
                        'notAfter': cert['notAfter']
                    }
                    
        except Exception as e:
            logger.error(f"Error checking SSL certificate for {url}: {e}")
            return {'valid': False, 'reason': str(e)}
    
    def _get_default_technical_result(self) -> TechnicalResult:
        """
        Return default technical result when analysis fails
        
        Returns:
            Default technical result
        """
        return TechnicalResult(
            https_enabled=False,
            mobile_friendly=False,
            sitemap_present=False,
            robots_txt_present=False,
            page_speed_score=0,
            core_web_vitals_passed=False
        )
    
    async def get_technical_recommendations(self, result: TechnicalResult) -> List[str]:
        """
        Get technical optimization recommendations
        
        Args:
            result: Technical analysis result
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if not result.https_enabled:
            recommendations.append("Enable HTTPS across all pages for security and SEO")
        
        if not result.mobile_friendly:
            recommendations.append("Implement responsive design for mobile optimization")
        
        if not result.sitemap_present:
            recommendations.append("Create and submit XML sitemap to search engines")
        
        if not result.robots_txt_present:
            recommendations.append("Add robots.txt file for crawler guidance")
        
        if result.page_speed_score < 70:
            recommendations.append("Improve page speed through optimization techniques")
        
        if not result.core_web_vitals_passed:
            recommendations.append("Optimize Core Web Vitals (LCP, FID, CLS) for better rankings")
        
        return recommendations 