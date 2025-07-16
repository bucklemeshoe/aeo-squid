"""
Main website analyzer orchestrator
"""

import uuid
import logging
import asyncio
from typing import Dict, List, Any
from datetime import datetime

from models.analysis import (
    PerformanceResult, SchemaResult, ContentResult, TechnicalResult,
    Recommendation
)
from .performance import PerformanceAnalyzer
from .schema import SchemaAnalyzer
from .content import ContentAnalyzer
from .technical import TechnicalAnalyzer


logger = logging.getLogger(__name__)


class WebsiteAnalyzer:
    """Main website analysis orchestrator"""
    
    def __init__(self, url: str):
        """
        Initialize analyzer for a specific URL
        
        Args:
            url: Website URL to analyze
        """
        self.url = url
        self.analysis_id = None
        
        # Initialize sub-analyzers
        self.performance_analyzer = PerformanceAnalyzer()
        self.schema_analyzer = SchemaAnalyzer()
        self.content_analyzer = ContentAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
    
    def generate_analysis_id(self) -> str:
        """
        Generate unique analysis ID
        
        Returns:
            Unique analysis ID
        """
        self.analysis_id = str(uuid.uuid4())
        return self.analysis_id
    
    async def analyze_performance(self) -> PerformanceResult:
        """
        Analyze website performance
        
        Returns:
            Performance analysis results
        """
        logger.info(f"Starting performance analysis for {self.url}")
        
        try:
            result = await self.performance_analyzer.analyze(self.url)
            logger.info(f"Performance analysis completed for {self.url}")
            return result
        except Exception as e:
            logger.error(f"Performance analysis failed for {self.url}: {e}")
            # Return default values on failure
            return PerformanceResult(
                lcp=5.0,
                fid=300,
                cls=0.25,
                score=0,
                mobile_score=0,
                desktop_score=0
            )
    
    async def analyze_schema(self) -> SchemaResult:
        """
        Analyze schema markup
        
        Returns:
            Schema analysis results
        """
        logger.info(f"Starting schema analysis for {self.url}")
        
        try:
            result = await self.schema_analyzer.analyze(self.url)
            logger.info(f"Schema analysis completed for {self.url}")
            return result
        except Exception as e:
            logger.error(f"Schema analysis failed for {self.url}: {e}")
            # Return default values on failure
            return SchemaResult(
                faq_schema_present=False,
                qa_schema_present=False,
                howto_schema_present=False,
                organization_schema_present=False,
                local_business_schema_present=False,
                validation_errors=[],
                total_schemas_found=0
            )
    
    async def analyze_content(self) -> ContentResult:
        """
        Analyze content structure
        
        Returns:
            Content analysis results
        """
        logger.info(f"Starting content analysis for {self.url}")
        
        try:
            result = await self.content_analyzer.analyze(self.url)
            logger.info(f"Content analysis completed for {self.url}")
            return result
        except Exception as e:
            logger.error(f"Content analysis failed for {self.url}: {e}")
            # Return default values on failure
            return ContentResult(
                heading_structure_score=0,
                faq_patterns_found=0,
                qa_content_detected=False,
                word_count=0,
                readability_score=0.0,
                conversational_queries_optimized=0
            )
    
    async def analyze_technical(self) -> TechnicalResult:
        """
        Analyze technical SEO aspects
        
        Returns:
            Technical analysis results
        """
        logger.info(f"Starting technical analysis for {self.url}")
        
        try:
            result = await self.technical_analyzer.analyze(self.url)
            logger.info(f"Technical analysis completed for {self.url}")
            return result
        except Exception as e:
            logger.error(f"Technical analysis failed for {self.url}: {e}")
            # Return default values on failure
            return TechnicalResult(
                https_enabled=False,
                mobile_friendly=False,
                sitemap_present=False,
                robots_txt_present=False,
                page_speed_score=0,
                core_web_vitals_passed=False
            )
    
    def calculate_scores(self, results: Dict[str, Any]) -> Dict[str, int]:
        """
        Calculate category and overall scores
        
        Args:
            results: Dictionary containing all analysis results
            
        Returns:
            Dictionary with calculated scores
        """
        logger.info(f"Calculating scores for {self.url}")
        
        # Performance score (0-25)
        performance_score = self._calculate_performance_score(results['performance'])
        
        # Schema score (0-25)
        schema_score = self._calculate_schema_score(results['schema'])
        
        # Content score (0-25)
        content_score = self._calculate_content_score(results['content'])
        
        # Technical score (0-25)
        technical_score = self._calculate_technical_score(results['technical'])
        
        # Overall score (0-100)
        overall_score = performance_score + schema_score + content_score + technical_score
        
        scores = {
            'performance': performance_score,
            'schema': schema_score,
            'content': content_score,
            'technical': technical_score,
            'overall': overall_score
        }
        
        logger.info(f"Scores calculated for {self.url}: {scores}")
        return scores
    
    def _calculate_performance_score(self, result: PerformanceResult) -> int:
        """Calculate performance category score"""
        score = 0
        
        # Core Web Vitals scoring
        if result.lcp <= 2.5:
            score += 8
        elif result.lcp <= 4.0:
            score += 5
        else:
            score += 2
        
        if result.fid <= 100:
            score += 8
        elif result.fid <= 300:
            score += 5
        else:
            score += 2
        
        if result.cls <= 0.1:
            score += 9
        elif result.cls <= 0.25:
            score += 6
        else:
            score += 3
        
        return min(score, 25)
    
    def _calculate_schema_score(self, result: SchemaResult) -> int:
        """Calculate schema category score"""
        score = 0
        
        # FAQ schema (high value for AEO)
        if result.faq_schema_present:
            score += 8
        
        # Q&A schema
        if result.qa_schema_present:
            score += 6
        
        # How-to schema
        if result.howto_schema_present:
            score += 5
        
        # Organization schema
        if result.organization_schema_present:
            score += 3
        
        # Local business schema (if applicable)
        if result.local_business_schema_present:
            score += 3
        
        # Deduct points for validation errors
        score -= min(len(result.validation_errors) * 2, 10)
        
        return max(0, min(score, 25))
    
    def _calculate_content_score(self, result: ContentResult) -> int:
        """Calculate content category score"""
        score = 0
        
        # Heading structure
        score += min(result.heading_structure_score, 8)
        
        # FAQ patterns
        if result.faq_patterns_found >= 5:
            score += 6
        elif result.faq_patterns_found >= 3:
            score += 4
        elif result.faq_patterns_found >= 1:
            score += 2
        
        # Q&A content detection
        if result.qa_content_detected:
            score += 5
        
        # Word count (sufficient content)
        if result.word_count >= 1000:
            score += 4
        elif result.word_count >= 500:
            score += 2
        
        # Conversational queries
        score += min(result.conversational_queries_optimized // 2, 2)
        
        return min(score, 25)
    
    def _calculate_technical_score(self, result: TechnicalResult) -> int:
        """Calculate technical category score"""
        score = 0
        
        # HTTPS
        if result.https_enabled:
            score += 5
        
        # Mobile friendly
        if result.mobile_friendly:
            score += 6
        
        # Sitemap
        if result.sitemap_present:
            score += 4
        
        # Robots.txt
        if result.robots_txt_present:
            score += 2
        
        # Core Web Vitals
        if result.core_web_vitals_passed:
            score += 8
        
        return min(score, 25)
    
    def generate_recommendations(self, scores: Dict[str, int]) -> List[Recommendation]:
        """
        Generate prioritized recommendations based on analysis results
        
        Args:
            scores: Calculated scores for each category
            
        Returns:
            List of prioritized recommendations
        """
        logger.info(f"Generating recommendations for {self.url}")
        
        recommendations = []
        
        # Performance recommendations
        if scores['performance'] < 15:
            recommendations.append(Recommendation(
                category="Performance",
                title="Improve Core Web Vitals",
                description="Your website's Core Web Vitals need improvement for better AI search visibility.",
                impact="High",
                difficulty="Medium",
                action_items=[
                    "Optimize Largest Contentful Paint (LCP) to under 2.5 seconds",
                    "Reduce First Input Delay (FID) to under 100ms",
                    "Minimize Cumulative Layout Shift (CLS) to under 0.1"
                ]
            ))
        
        # Schema recommendations
        if scores['schema'] < 15:
            recommendations.append(Recommendation(
                category="Schema",
                title="Add FAQ Schema Markup",
                description="Implement structured data to help AI engines understand your Q&A content.",
                impact="High",
                difficulty="Medium",
                action_items=[
                    "Identify your top 5 FAQ pages",
                    "Add JSON-LD FAQ schema markup",
                    "Validate with Google's Rich Results Test"
                ]
            ))
        
        # Content recommendations
        if scores['content'] < 15:
            recommendations.append(Recommendation(
                category="Content",
                title="Optimize for Conversational Queries",
                description="Create content that answers questions the way people naturally ask them.",
                impact="High",
                difficulty="Easy",
                action_items=[
                    "Research common questions in your industry",
                    "Create dedicated Q&A sections",
                    "Use natural language and question-based headings"
                ]
            ))
        
        # Technical recommendations
        if scores['technical'] < 15:
            recommendations.append(Recommendation(
                category="Technical",
                title="Fix Technical SEO Issues",
                description="Address technical issues that prevent AI crawlers from understanding your site.",
                impact="Medium",
                difficulty="Easy",
                action_items=[
                    "Ensure HTTPS is enabled across all pages",
                    "Implement mobile-responsive design",
                    "Create and submit XML sitemap"
                ]
            ))
        
        # Sort by impact priority
        impact_priority = {"High": 3, "Medium": 2, "Low": 1}
        recommendations.sort(key=lambda x: impact_priority.get(x.impact, 0), reverse=True)
        
        logger.info(f"Generated {len(recommendations)} recommendations for {self.url}")
        return recommendations[:5]  # Return top 5 recommendations 