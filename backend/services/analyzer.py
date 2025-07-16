"""
Main website analyzer orchestrator - Enhanced with FAQ Intelligence
"""

import uuid
import logging
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup

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
    """Main website analysis orchestrator with enhanced FAQ intelligence"""
    
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
        self.content_analyzer = ContentAnalyzer()  # Now uses enhanced FAQ intelligence
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
    
    async def analyze_schema(self) -> Dict[str, Any]:
        """
        Analyze schema markup with enhanced intelligence
        
        Returns:
            Enhanced schema analysis results
        """
        logger.info(f"Starting enhanced schema analysis for {self.url}")
        
        try:
            # Use enhanced schema analysis
            enhanced_result = await self.schema_analyzer.analyze_with_intelligence(self.url)
            
            # Create legacy result for backward compatibility
            legacy_result = enhanced_result.get('legacy', {})
            
            # Return enhanced format
            result = {
                'enhanced': enhanced_result.get('enhanced', {}),
                'legacy': legacy_result,
                'intelligence_upgrade': enhanced_result.get('intelligence_upgrade', False),
                'schema_intelligence_score': enhanced_result.get('schema_intelligence_score', 0),
                'aeo_readiness_score': enhanced_result.get('aeo_readiness_score', 0)
            }
            
            logger.info(f"Enhanced schema analysis completed for {self.url}")
            logger.info(f"Schema Intelligence Score: {result['schema_intelligence_score']:.1f}/100")
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced schema analysis failed for {self.url}: {e}")
            # Return default enhanced format
            default_legacy = {
                'faq_schema_present': False,
                'qa_schema_present': False,
                'howto_schema_present': False,
                'organization_schema_present': False,
                'local_business_schema_present': False,
                'validation_errors': [],
                'total_schemas_found': 0
            }
            
            return {
                'enhanced': {
                    'schemas_detected': [],
                    'validation_results': [],
                    'opportunities': [],
                    'schema_intelligence_score': 0.0,
                    'aeo_readiness_score': 0.0,
                    'missing_critical_schemas': ['FAQPage', 'HowTo', 'QAPage'],
                    'implementation_recommendations': [
                        "Schema analysis failed - please verify URL is accessible"
                    ],
                    'content_analysis': {}
                },
                'legacy': default_legacy,
                'intelligence_upgrade': False,
                'schema_intelligence_score': 0.0,
                'aeo_readiness_score': 0.0
            }
    
    async def analyze_content(self) -> Dict[str, Any]:
        """
        Analyze content structure with enhanced FAQ intelligence
        
        Returns:
            Enhanced content analysis results with FAQ intelligence
        """
        logger.info(f"Starting enhanced content analysis for {self.url}")
        
        try:
            # Fetch webpage content
            soup = await self._fetch_page_content()
            if not soup:
                return self._get_default_content_analysis()
            
            # Use the enhanced content analyzer
            enhanced_results = self.content_analyzer.analyze_content(soup)
            
            # Create backward-compatible ContentResult for scoring
            legacy_result = self._create_legacy_content_result(enhanced_results)
            
            # Return both enhanced and legacy results
            result = {
                'enhanced': enhanced_results,
                'legacy': legacy_result,
                'intelligence_upgrade': True
            }
            
            logger.info(f"Enhanced content analysis completed for {self.url}")
            logger.info(f"FAQ Intelligence Score: {enhanced_results.get('faq_analysis', {}).get('faq_intelligence_score', 0)}/100")
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced content analysis failed for {self.url}: {e}")
            return self._get_default_content_analysis()
    
    async def _fetch_page_content(self) -> Optional[BeautifulSoup]:
        """
        Fetch webpage content for analysis
        
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            timeout = aiohttp.ClientTimeout(total=20)
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AEO-Analyzer/1.0)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        content = await response.text()
                        return BeautifulSoup(content, 'html.parser')
                    else:
                        logger.warning(f"HTTP {response.status} when fetching {self.url}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching content from {self.url}: {e}")
            return None
    
    def _create_legacy_content_result(self, enhanced_results: Dict[str, Any]) -> ContentResult:
        """
        Create legacy ContentResult from enhanced analysis for backward compatibility
        
        Args:
            enhanced_results: Enhanced content analysis results
            
        Returns:
            Legacy ContentResult object
        """
        basic_metrics = enhanced_results.get('basic_metrics', {})
        faq_analysis = enhanced_results.get('faq_analysis', {})
        structure_analysis = enhanced_results.get('structure_analysis', {})
        
        # Map enhanced data to legacy format
        return ContentResult(
            heading_structure_score=min(int(structure_analysis.get('hierarchy_score', 0) * 10), 10),
            faq_patterns_found=faq_analysis.get('faq_sections_found', 0),
            qa_content_detected=faq_analysis.get('qa_pairs_count', 0) > 0,
            word_count=basic_metrics.get('word_count', 0),
            readability_score=faq_analysis.get('answer_completeness_score', 0) * 10,
            conversational_queries_optimized=max(int(faq_analysis.get('voice_search_readiness', 0) * 20), 0)
        )
    
    def _get_default_content_analysis(self) -> Dict[str, Any]:
        """
        Return default content analysis when analysis fails
        
        Returns:
            Default enhanced content analysis
        """
        default_legacy = ContentResult(
            heading_structure_score=0,
            faq_patterns_found=0,
            qa_content_detected=False,
            word_count=0,
            readability_score=0.0,
            conversational_queries_optimized=0
        )
        
        default_enhanced = {
            'basic_metrics': {
                'word_count': 0,
                'total_headings': 0,
                'content_intelligence_score': 0
            },
            'faq_analysis': {
                'faq_intelligence_score': 0,
                'qa_pairs_count': 0,
                'voice_search_readiness': 0,
                'featured_snippet_potential': 0,
                'improvement_suggestions': ["Unable to analyze content - please check URL accessibility"]
            },
            'structure_analysis': {},
            'aeo_metrics': {},
            'content_intelligence_score': 0,
            'recommendations': ["Content analysis failed - please verify URL is accessible"]
        }
        
        return {
            'enhanced': default_enhanced,
            'legacy': default_legacy,
            'intelligence_upgrade': False
        }
    
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
        Calculate category and overall scores with enhanced intelligence
        
        Args:
            results: Dictionary containing all analysis results
            
        Returns:
            Dictionary with calculated scores
        """
        logger.info(f"Calculating enhanced scores for {self.url}")
        
        # Performance score (0-25)
        performance_score = self._calculate_performance_score(results['performance'])
        
        # Enhanced schema score (0-25) - Now uses Schema Intelligence!
        schema_score = self._calculate_enhanced_schema_score(results['schema'])
        
        # Enhanced content score (0-25) - Now uses FAQ intelligence!
        content_score = self._calculate_enhanced_content_score(results['content'])
        
        # Technical score (0-25)
        technical_score = self._calculate_technical_score(results['technical'])
        
        # Overall score (0-100)
        overall_score = performance_score + schema_score + content_score + technical_score
        
        # Calculate intelligence level based on enhanced metrics
        intelligence_level = self._calculate_intelligence_level(results)
        
        scores = {
            'performance': performance_score,
            'schema': schema_score,
            'content': content_score,
            'technical': technical_score,
            'overall': overall_score,
            'intelligence_level': intelligence_level,  # NEW!
            'faq_intelligence': self._get_faq_intelligence_score(results['content']),  # NEW!
            'schema_intelligence': self._get_schema_intelligence_score(results['schema']),  # NEW!
            'aeo_readiness': self._get_aeo_readiness_score(results['schema'])  # NEW!
        }
        
        logger.info(f"Enhanced scores calculated for {self.url}: {scores}")
        return scores
    
    def _calculate_enhanced_content_score(self, content_results: Dict[str, Any]) -> int:
        """
        Calculate enhanced content score using FAQ intelligence
        
        Args:
            content_results: Enhanced content analysis results
            
        Returns:
            Content score (0-25)
        """
        if not content_results.get('intelligence_upgrade', False):
            # Fallback to legacy scoring
            return self._calculate_content_score(content_results.get('legacy'))
        
        enhanced = content_results.get('enhanced', {})
        faq_analysis = enhanced.get('faq_analysis', {})
        basic_metrics = enhanced.get('basic_metrics', {})
        aeo_metrics = enhanced.get('aeo_metrics', {})
        
        score = 0
        
        # FAQ Intelligence (40% of content score) - This is the big upgrade!
        faq_intelligence = faq_analysis.get('faq_intelligence_score', 0) / 100
        score += int(faq_intelligence * 10)  # 0-10 points
        
        # Voice Search Readiness (20% of content score)
        voice_readiness = faq_analysis.get('voice_search_readiness', 0)
        score += int(voice_readiness * 5)  # 0-5 points
        
        # Featured Snippet Potential (20% of content score)
        snippet_potential = min(faq_analysis.get('featured_snippet_potential', 0), 5)
        score += snippet_potential  # 0-5 points
        
        # Content Quality (20% of content score)
        word_count = basic_metrics.get('word_count', 0)
        if word_count >= 1000:
            score += 5
        elif word_count >= 500:
            score += 3
        elif word_count >= 200:
            score += 1
        
        return min(score, 25)
    
    def _calculate_intelligence_level(self, results: Dict[str, Any]) -> str:
        """
        Calculate overall intelligence level of the website
        
        Args:
            results: All analysis results
            
        Returns:
            Intelligence level string
        """
        content_results = results.get('content', {})
        schema_results = results.get('schema', {})
        
        # Check if we have enhanced analysis
        has_content_intelligence = content_results.get('intelligence_upgrade', False)
        has_schema_intelligence = schema_results.get('intelligence_upgrade', False)
        
        if not (has_content_intelligence or has_schema_intelligence):
            return "Basic"
        
        intelligence_scores = []
        
        # Content intelligence
        if has_content_intelligence:
            enhanced_content = content_results.get('enhanced', {})
            content_intelligence = enhanced_content.get('content_intelligence_score', 0)
            faq_intelligence = enhanced_content.get('faq_analysis', {}).get('faq_intelligence_score', 0)
            content_avg = (content_intelligence + faq_intelligence) / 2
            intelligence_scores.append(content_avg)
        
        # Schema intelligence
        if has_schema_intelligence:
            enhanced_schema = schema_results.get('enhanced', {})
            schema_intelligence = enhanced_schema.get('schema_intelligence_score', 0)
            aeo_readiness = enhanced_schema.get('aeo_readiness_score', 0)
            schema_avg = (schema_intelligence + aeo_readiness) / 2
            intelligence_scores.append(schema_avg)
        
        # Calculate overall intelligence score
        if intelligence_scores:
            combined_score = sum(intelligence_scores) / len(intelligence_scores)
        else:
            combined_score = 0
        
        if combined_score >= 75:
            return "Advanced"
        elif combined_score >= 55:
            return "Intermediate"
        elif combined_score >= 35:
            return "Developing"
        else:
            return "Basic"
    
    def _get_faq_intelligence_score(self, content_results: Dict[str, Any]) -> int:
        """
        Extract FAQ intelligence score for display
        
        Args:
            content_results: Content analysis results
            
        Returns:
            FAQ intelligence score (0-100)
        """
        if content_results.get('intelligence_upgrade', False):
            enhanced = content_results.get('enhanced', {})
            return int(enhanced.get('faq_analysis', {}).get('faq_intelligence_score', 0))
        return 0
    
    def _get_schema_intelligence_score(self, schema_results: Dict[str, Any]) -> int:
        """
        Extract schema intelligence score for display
        
        Args:
            schema_results: Schema analysis results
            
        Returns:
            Schema intelligence score (0-100)
        """
        if schema_results.get('intelligence_upgrade', False):
            enhanced = schema_results.get('enhanced', {})
            return int(enhanced.get('schema_intelligence_score', 0))
        return 0
    
    def _get_aeo_readiness_score(self, schema_results: Dict[str, Any]) -> int:
        """
        Extract AEO readiness score for display
        
        Args:
            schema_results: Schema analysis results
            
        Returns:
            AEO readiness score (0-100)
        """
        if schema_results.get('intelligence_upgrade', False):
            enhanced = schema_results.get('enhanced', {})
            return int(enhanced.get('aeo_readiness_score', 0))
        return 0
    
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
    
    def _calculate_enhanced_schema_score(self, schema_results: Dict[str, Any]) -> int:
        """Calculate enhanced schema score using intelligence"""
        if not schema_results.get('intelligence_upgrade', False):
            # Fallback to legacy scoring
            legacy_data = schema_results.get('legacy', {})
            legacy_result = type('SchemaResult', (), legacy_data)()
            return self._calculate_schema_score(legacy_result)
        
        enhanced_data = schema_results.get('enhanced', {})
        score = 0
        
        # Base score from schema intelligence (60% weight)
        schema_intelligence = enhanced_data.get('schema_intelligence_score', 0) / 100
        score += int(schema_intelligence * 15)  # 0-15 points
        
        # AEO readiness bonus (25% weight)
        aeo_readiness = enhanced_data.get('aeo_readiness_score', 0) / 100
        score += int(aeo_readiness * 6)  # 0-6 points
        
        # Implementation opportunity bonus (15% weight)
        opportunities = enhanced_data.get('opportunities', [])
        high_confidence_ops = [op for op in opportunities if op.get('confidence', 0) > 0.7]
        score += min(len(high_confidence_ops), 4)  # 0-4 points
        
        return min(score, 25)
    
    def _calculate_schema_score(self, result) -> int:
        """Calculate legacy schema category score (fallback)"""
        score = 0
        
        # FAQ schema (high value for AEO)
        if getattr(result, 'faq_schema_present', False):
            score += 8
        
        # Q&A schema
        if getattr(result, 'qa_schema_present', False):
            score += 6
        
        # How-to schema
        if getattr(result, 'howto_schema_present', False):
            score += 5
        
        # Organization schema
        if getattr(result, 'organization_schema_present', False):
            score += 3
        
        # Local business schema (if applicable)
        if getattr(result, 'local_business_schema_present', False):
            score += 3
        
        # Deduct points for validation errors
        validation_errors = getattr(result, 'validation_errors', [])
        score -= min(len(validation_errors) * 2, 10)
        
        return max(0, min(score, 25))
    
    def _calculate_content_score(self, result: ContentResult) -> int:
        """Calculate legacy content category score (fallback)"""
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
    
    def generate_recommendations(self, scores: Dict[str, int], results: Dict[str, Any]) -> List[Recommendation]:
        """
        Generate enhanced prioritized recommendations based on FAQ intelligence
        
        Args:
            scores: Calculated scores for each category
            results: Full analysis results including enhanced content data
            
        Returns:
            List of prioritized recommendations
        """
        logger.info(f"Generating enhanced recommendations for {self.url}")
        
        recommendations = []
        
        # Enhanced FAQ Intelligence Recommendations (NEW!)
        content_results = results.get('content', {})
        if content_results.get('intelligence_upgrade', False):
            enhanced = content_results.get('enhanced', {})
            faq_suggestions = enhanced.get('faq_analysis', {}).get('improvement_suggestions', [])
            
            if faq_suggestions:
                recommendations.append(Recommendation(
                    category="FAQ Intelligence",
                    title="Enhance FAQ Content for AEO",
                    description="AI-powered analysis found specific opportunities to improve your FAQ content for Answer Engine Optimization.",
                    impact="High",
                    difficulty="Easy",
                    action_items=faq_suggestions[:5]  # Top 5 AI-generated suggestions
                ))
        
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
        
        # Enhanced Schema Intelligence Recommendations (NEW!)
        schema_results = results.get('schema', {})
        if schema_results.get('intelligence_upgrade', False):
            enhanced_schema = schema_results.get('enhanced', {})
            schema_recommendations = enhanced_schema.get('implementation_recommendations', [])
            
            if schema_recommendations and scores['schema'] < 20:
                recommendations.append(Recommendation(
                    category="Schema Intelligence",
                    title="Enhance Schema Markup with AI Optimization",
                    description="AI-powered analysis found specific opportunities to improve your schema markup for better answer engine understanding.",
                    impact="High",
                    difficulty="Medium",
                    action_items=schema_recommendations[:5]  # Top 5 AI-generated suggestions
                ))
        
        # Schema recommendations (enhanced)
        if scores['schema'] < 15:
            schema_intelligence = scores.get('schema_intelligence', 0)
            if schema_intelligence < 30:
                recommendations.append(Recommendation(
                    category="Schema",
                    title="Implement Critical AEO Schema Markup",
                    description="Add essential schema types to dramatically improve your answer engine optimization.",
                    impact="High",
                    difficulty="Medium",
                    action_items=[
                        "Start with FAQ schema for immediate voice search boost",
                        "Add How-To schema for step-by-step content",
                        "Implement QA schema for question-answer pairs",
                        "Validate all schemas with Google's Rich Results Test"
                    ]
                ))
            else:
                recommendations.append(Recommendation(
                    category="Schema",
                    title="Optimize Existing Schema Markup",
                    description="Enhance your current schema implementation for better AI understanding.",
                    impact="High",
                    difficulty="Easy",
                    action_items=[
                        "Add missing required properties to existing schemas",
                        "Improve content-schema alignment",
                        "Implement AEO-optimal properties for better ranking"
                    ]
                ))
        
        # Content recommendations (enhanced)
        if scores['content'] < 15:
            faq_score = scores.get('faq_intelligence', 0)
            if faq_score < 50:
                recommendations.append(Recommendation(
                    category="Content",
                    title="Develop Intelligent FAQ Content",
                    description="Create AI-optimized FAQ content that answers questions the way people naturally ask them.",
                    impact="High",
                    difficulty="Easy",
                    action_items=[
                        "Research conversational queries in your industry",
                        "Create question-based headings with natural language",
                        "Structure answers in 20-150 words for featured snippets",
                        "Use step-by-step formats and direct answers"
                    ]
                ))
            else:
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
        
        logger.info(f"Generated {len(recommendations)} enhanced recommendations for {self.url}")
        return recommendations[:6]  # Return top 6 recommendations 