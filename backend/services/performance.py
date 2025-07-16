"""
Performance analysis using Google PageSpeed Insights
"""

import aiohttp
import logging
from typing import Dict, Any, Optional, List
from models.analysis import PerformanceResult
from config import get_settings
import asyncio


logger = logging.getLogger(__name__)
settings = get_settings()


class PerformanceAnalyzer:
    """Website performance analysis"""
    
    def __init__(self):
        """Initialize performance analyzer"""
        self.api_key = settings.GOOGLE_PAGESPEED_API_KEY
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    async def analyze(self, url: str) -> PerformanceResult:
        """
        Analyze website performance using PageSpeed Insights
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Performance analysis results
        """
        logger.info(f"Starting PageSpeed analysis for {url}")
        
        try:
            # If no API key, return mock data
            if not self.api_key:
                logger.warning("No PageSpeed API key configured, returning mock data")
                return self._get_mock_performance_data()
            
            # Run both mobile and desktop analysis
            mobile_result = await self._run_pagespeed_analysis(url, 'mobile')
            desktop_result = await self._run_pagespeed_analysis(url, 'desktop')
            
            # Extract metrics
            mobile_metrics = self._extract_metrics(mobile_result) if mobile_result else {}
            desktop_metrics = self._extract_metrics(desktop_result) if desktop_result else {}
            
            # Combine results
            result = PerformanceResult(
                lcp=mobile_metrics.get('lcp', 5.0),
                fid=mobile_metrics.get('fid', 300),
                cls=mobile_metrics.get('cls', 0.25),
                score=mobile_metrics.get('score', 50),
                mobile_score=mobile_metrics.get('score', 50),
                desktop_score=desktop_metrics.get('score', 50)
            )
            
            logger.info(f"PageSpeed analysis completed for {url}")
            return result
            
        except Exception as e:
            logger.error(f"PageSpeed analysis failed for {url}: {e}")
            return self._get_mock_performance_data()
    
    async def _run_pagespeed_analysis(self, url: str, strategy: str) -> Optional[Dict[Any, Any]]:
        """
        Run PageSpeed Insights analysis for specific strategy
        
        Args:
            url: Website URL
            strategy: 'mobile' or 'desktop'
            
        Returns:
            PageSpeed API response or None
        """
        params = {
            'url': url,
            'key': self.api_key,
            'strategy': strategy,
            'category': ['PERFORMANCE'],
            'locale': 'en'
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.debug(f"PageSpeed API success for {url} ({strategy})")
                        return data
                    else:
                        logger.error(f"PageSpeed API error {response.status} for {url}")
                        return None
                        
        except asyncio.TimeoutError:
            logger.error(f"PageSpeed API timeout for {url}")
            return None
        except Exception as e:
            logger.error(f"PageSpeed API request failed for {url}: {e}")
            return None
    
    def _extract_metrics(self, pagespeed_data: Dict[Any, Any]) -> Dict[str, Any]:
        """
        Extract Core Web Vitals and performance metrics
        
        Args:
            pagespeed_data: Raw PageSpeed API response
            
        Returns:
            Extracted metrics
        """
        try:
            lighthouse_result = pagespeed_data.get('lighthouseResult', {})
            audits = lighthouse_result.get('audits', {})
            categories = lighthouse_result.get('categories', {})
            
            # Performance score
            performance = categories.get('performance', {})
            score = int(performance.get('score', 0) * 100) if performance.get('score') else 0
            
            # Core Web Vitals
            lcp_audit = audits.get('largest-contentful-paint', {})
            lcp = lcp_audit.get('numericValue', 5000) / 1000  # Convert to seconds
            
            fid_audit = audits.get('max-potential-fid', {})  # Use max potential FID as proxy
            fid = fid_audit.get('numericValue', 300)
            
            cls_audit = audits.get('cumulative-layout-shift', {})
            cls = cls_audit.get('numericValue', 0.25)
            
            return {
                'score': score,
                'lcp': lcp,
                'fid': fid,
                'cls': cls
            }
            
        except Exception as e:
            logger.error(f"Error extracting PageSpeed metrics: {e}")
            return {
                'score': 0,
                'lcp': 5.0,
                'fid': 300,
                'cls': 0.25
            }
    
    def _get_mock_performance_data(self) -> PerformanceResult:
        """
        Return mock performance data for testing
        
        Returns:
            Mock performance result
        """
        return PerformanceResult(
            lcp=3.2,
            fid=150,
            cls=0.15,
            score=65,
            mobile_score=62,
            desktop_score=68
        )
    
    async def get_performance_suggestions(self, url: str) -> List[str]:
        """
        Get performance improvement suggestions
        
        Args:
            url: Website URL
            
        Returns:
            List of performance suggestions
        """
        suggestions = [
            "Optimize images and use next-gen formats (WebP, AVIF)",
            "Minimize and compress CSS and JavaScript files",
            "Enable browser caching and compression",
            "Use a Content Delivery Network (CDN)",
            "Optimize server response times",
            "Reduce render-blocking resources",
            "Implement lazy loading for images and videos"
        ]
        
        return suggestions 