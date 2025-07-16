"""
AI-Powered Content Analysis for AEO Assessment
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
import aiohttp
from bs4 import BeautifulSoup
import openai
from models.analysis import ContentResult
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class AIContentAnalyzer:
    """AI-powered content analysis for AEO optimization"""
    
    def __init__(self):
        """Initialize AI analyzer"""
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # AEO Assessment Criteria
        self.aeo_criteria = """
        Answer Engine Optimization (AEO) Criteria:
        
        1. FAQ Content Quality:
           - Clear, conversational questions that people actually ask
           - Comprehensive, helpful answers
           - Natural language patterns
           - Questions address user intent
        
        2. Conversational Query Optimization:
           - Content answers "how", "what", "why", "when" questions
           - Uses natural, spoken language patterns
           - Addresses long-tail, voice search queries
           - Provides direct, concise answers
        
        3. Content Structure for AI:
           - Clear heading hierarchy (H1-H6)
           - Logical information flow
           - Easy to extract key facts
           - Summary-friendly format
        
        4. Authority & Expertise:
           - Demonstrates subject matter expertise
           - Provides detailed, accurate information
           - Includes examples and explanations
           - Shows credibility signals
        """
    
    async def analyze_with_ai(self, url: str, content: str) -> Dict[str, Any]:
        """
        Use GPT to analyze content for AEO readiness
        
        Args:
            url: Website URL
            content: Cleaned text content from the webpage
            
        Returns:
            AI analysis results
        """
        
        # Create analysis prompt
        prompt = f"""
        Analyze this webpage content for Answer Engine Optimization (AEO) readiness.
        
        URL: {url}
        
        CONTENT:
        {content[:4000]}  # Limit content to stay within token limits
        
        {self.aeo_criteria}
        
        Provide a detailed analysis in JSON format:
        {{
            "faq_quality_score": 0-25,
            "faq_analysis": "detailed explanation of FAQ content quality",
            "conversational_optimization_score": 0-25, 
            "conversational_analysis": "how well content answers natural questions",
            "content_structure_score": 0-25,
            "structure_analysis": "evaluation of heading hierarchy and organization",
            "authority_expertise_score": 0-25,
            "expertise_analysis": "assessment of content depth and credibility",
            "overall_ai_score": 0-100,
            "key_strengths": ["list", "of", "strengths"],
            "improvement_recommendations": [
                {{
                    "priority": "High/Medium/Low",
                    "action": "specific recommendation",
                    "reasoning": "why this helps AEO"
                }}
            ],
            "ai_readiness_level": "Excellent/Good/Fair/Poor"
        }}
        
        Be specific and actionable in your recommendations.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",  # Use GPT-4 for better analysis
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert in Answer Engine Optimization (AEO) and AI search readiness. Analyze content for how well it would perform in AI-powered search engines like ChatGPT, Bard, and Perplexity."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for consistent analysis
                max_tokens=1500
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
                return analysis_data
            else:
                # Fallback if JSON parsing fails
                return self._create_fallback_analysis(analysis_text)
                
        except Exception as e:
            logger.error(f"AI analysis failed for {url}: {e}")
            return self._create_error_analysis()
    
    async def analyze(self, url: str) -> ContentResult:
        """
        Analyze website content using AI
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Enhanced content analysis results
        """
        logger.info(f"Starting AI content analysis for {url}")
        
        try:
            # Fetch page content
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch {url}: HTTP {response.status}")
                    
                    html_content = await response.text()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get clean text content
            clean_text = soup.get_text()
            clean_text = ' '.join(clean_text.split())  # Clean whitespace
            
            # Run AI analysis
            ai_results = await self.analyze_with_ai(url, clean_text)
            
            # Convert AI results to ContentResult format
            return ContentResult(
                heading_structure_score=ai_results.get('content_structure_score', 0),
                faq_patterns_found=self._count_faq_patterns(clean_text),
                qa_content_detected=ai_results.get('faq_quality_score', 0) > 10,
                word_count=len(clean_text.split()),
                readability_score=ai_results.get('overall_ai_score', 0) / 100,
                conversational_queries_optimized=ai_results.get('conversational_optimization_score', 0),
                ai_analysis=ai_results  # Store full AI analysis
            )
            
        except Exception as e:
            logger.error(f"AI content analysis failed for {url}: {e}")
            return ContentResult(
                heading_structure_score=0,
                faq_patterns_found=0,
                qa_content_detected=False,
                word_count=0,
                readability_score=0.0,
                conversational_queries_optimized=0
            )
    
    def _count_faq_patterns(self, text: str) -> int:
        """Count FAQ patterns in text"""
        import re
        faq_indicators = ['faq', 'frequently asked', 'common questions', 'q&a']
        count = 0
        for indicator in faq_indicators:
            count += len(re.findall(indicator, text, re.IGNORECASE))
        return count
    
    def _create_fallback_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Create fallback analysis when JSON parsing fails"""
        return {
            "faq_quality_score": 10,
            "faq_analysis": "Analysis completed but JSON parsing failed",
            "conversational_optimization_score": 10,
            "conversational_analysis": analysis_text[:200],
            "content_structure_score": 10,
            "structure_analysis": "Structure analysis available in raw text",
            "authority_expertise_score": 10,
            "expertise_analysis": "Content appears to have moderate expertise",
            "overall_ai_score": 40,
            "key_strengths": ["Content analyzed", "Basic structure present"],
            "improvement_recommendations": [
                {
                    "priority": "Medium",
                    "action": "Review AI analysis output formatting",
                    "reasoning": "Ensure consistent JSON response format"
                }
            ],
            "ai_readiness_level": "Fair"
        }
    
    def _create_error_analysis(self) -> Dict[str, Any]:
        """Create error analysis when AI call fails"""
        return {
            "faq_quality_score": 0,
            "faq_analysis": "Unable to analyze FAQ content due to technical error",
            "conversational_optimization_score": 0,
            "conversational_analysis": "AI analysis unavailable",
            "content_structure_score": 0,
            "structure_analysis": "Could not evaluate content structure", 
            "authority_expertise_score": 0,
            "expertise_analysis": "Expertise evaluation failed",
            "overall_ai_score": 0,
            "key_strengths": [],
            "improvement_recommendations": [
                {
                    "priority": "High",
                    "action": "Configure OpenAI API key and retry analysis",
                    "reasoning": "AI analysis requires valid API configuration"
                }
            ],
            "ai_readiness_level": "Unknown"
        } 