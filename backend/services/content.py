"""
Content structure analysis for AEO optimization
"""

import re
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import aiohttp
from models.analysis import ContentResult


logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Content structure and AEO analysis"""
    
    def __init__(self):
        """Initialize content analyzer"""
        self.faq_patterns = [
            r'frequently\s+asked\s+questions?',
            r'common\s+questions?',
            r'faq',
            r'q\s*&\s*a',
            r'questions?\s+and\s+answers?'
        ]
        
        self.question_patterns = [
            r'\b(?:what|how|why|when|where|who|which)\b[^?]*\?',
            r'\bis\s+[^?]*\?',
            r'\bcan\s+[^?]*\?',
            r'\bdoes\s+[^?]*\?',
            r'\bdo\s+[^?]*\?'
        ]
    
    async def analyze(self, url: str) -> ContentResult:
        """
        Analyze website content structure for AEO optimization
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Content analysis results
        """
        logger.info(f"Starting content analysis for {url}")
        
        try:
            # Fetch page content
            html_content = await self._fetch_page_content(url)
            if not html_content:
                return self._get_default_content_result()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Analyze different aspects
            heading_score = self._analyze_heading_structure(soup)
            faq_patterns = self._detect_faq_patterns(soup)
            qa_detected = self._detect_qa_content(soup)
            word_count = self._calculate_word_count(soup)
            readability = self._calculate_readability_score(soup)
            conversational_queries = self._count_conversational_queries(soup)
            
            result = ContentResult(
                heading_structure_score=heading_score,
                faq_patterns_found=faq_patterns,
                qa_content_detected=qa_detected,
                word_count=word_count,
                readability_score=readability,
                conversational_queries_optimized=conversational_queries
            )
            
            logger.info(f"Content analysis completed for {url}")
            return result
            
        except Exception as e:
            logger.error(f"Content analysis failed for {url}: {e}")
            return self._get_default_content_result()
    
    async def _fetch_page_content(self, url: str) -> Optional[str]:
        """
        Fetch webpage content
        
        Args:
            url: Website URL
            
        Returns:
            HTML content or None
        """
        try:
            timeout = aiohttp.ClientTimeout(total=20)
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AEO-Analyzer/1.0)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.debug(f"Successfully fetched content from {url}")
                        return content
                    else:
                        logger.warning(f"HTTP {response.status} when fetching {url}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {e}")
            return None
    
    def _analyze_heading_structure(self, soup: BeautifulSoup) -> int:
        """
        Analyze heading structure quality
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            Heading structure score (0-10)
        """
        score = 0
        
        try:
            # Check for H1 tag
            h1_tags = soup.find_all('h1')
            if len(h1_tags) == 1:
                score += 3
            elif len(h1_tags) > 1:
                score += 1  # Multiple H1s are not ideal
            
            # Check heading hierarchy
            headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if len(headings) >= 3:
                score += 2
            
            # Check for question-based headings
            question_headings = 0
            for heading in headings:
                text = heading.get_text().strip()
                if any(re.search(pattern, text.lower()) for pattern in self.question_patterns):
                    question_headings += 1
            
            if question_headings >= 3:
                score += 3
            elif question_headings >= 1:
                score += 2
            
            # Check heading length (not too short, not too long)
            good_length_headings = 0
            for heading in headings:
                text = heading.get_text().strip()
                if 20 <= len(text) <= 100:
                    good_length_headings += 1
            
            if good_length_headings >= len(headings) * 0.7:
                score += 2
            
        except Exception as e:
            logger.error(f"Error analyzing heading structure: {e}")
        
        return min(score, 10)
    
    def _detect_faq_patterns(self, soup: BeautifulSoup) -> int:
        """
        Detect FAQ patterns in content
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            Number of FAQ patterns found
        """
        faq_count = 0
        
        try:
            # Get all text content
            text_content = soup.get_text().lower()
            
            # Check for FAQ section indicators
            for pattern in self.faq_patterns:
                if re.search(pattern, text_content, re.IGNORECASE):
                    faq_count += 1
            
            # Look for question-answer structures
            elements = soup.find_all(['div', 'section', 'article'])
            for element in elements:
                element_text = element.get_text()
                
                # Count question marks followed by content
                questions = re.findall(r'[^.!?]*\?', element_text)
                if len(questions) >= 3:  # At least 3 questions in one section
                    faq_count += 1
            
            # Look for accordion/collapsible FAQ structures
            accordion_elements = soup.find_all(attrs={'class': re.compile(r'(accordion|collapse|faq|toggle)', re.I)})
            faq_count += len(accordion_elements)
            
        except Exception as e:
            logger.error(f"Error detecting FAQ patterns: {e}")
        
        return min(faq_count, 20)  # Cap at 20
    
    def _detect_qa_content(self, soup: BeautifulSoup) -> bool:
        """
        Detect if page has Q&A content structure
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            True if Q&A content detected
        """
        try:
            text_content = soup.get_text().lower()
            
            # Look for Q&A indicators
            qa_indicators = [
                'question:', 'answer:', 'q:', 'a:',
                'ask:', 'reply:', 'response:'
            ]
            
            indicator_count = 0
            for indicator in qa_indicators:
                if indicator in text_content:
                    indicator_count += 1
            
            # If multiple Q&A indicators found
            if indicator_count >= 2:
                return True
            
            # Look for structured Q&A in HTML
            qa_elements = soup.find_all(attrs={'class': re.compile(r'(question|answer|qa)', re.I)})
            if len(qa_elements) >= 4:  # At least 2 Q&A pairs
                return True
            
            # Check for definition lists (often used for Q&A)
            dl_elements = soup.find_all('dl')
            for dl in dl_elements:
                dt_count = len(dl.find_all('dt'))
                dd_count = len(dl.find_all('dd'))
                if dt_count >= 2 and dd_count >= 2:
                    return True
            
        except Exception as e:
            logger.error(f"Error detecting Q&A content: {e}")
        
        return False
    
    def _calculate_word_count(self, soup: BeautifulSoup) -> int:
        """
        Calculate meaningful word count
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            Word count
        """
        try:
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean and count words
            words = re.findall(r'\b\w+\b', text)
            meaningful_words = [word for word in words if len(word) > 2]
            
            return len(meaningful_words)
            
        except Exception as e:
            logger.error(f"Error calculating word count: {e}")
            return 0
    
    def _calculate_readability_score(self, soup: BeautifulSoup) -> float:
        """
        Calculate basic readability score
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            Readability score (approximate)
        """
        try:
            # Get main content text
            text = soup.get_text()
            
            # Count sentences and words
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            words = re.findall(r'\b\w+\b', text)
            
            if not sentences or not words:
                return 0.0
            
            # Average words per sentence
            avg_words_per_sentence = len(words) / len(sentences)
            
            # Simple readability approximation
            # Lower score = easier to read (better for AEO)
            if avg_words_per_sentence <= 15:
                score = 9.0
            elif avg_words_per_sentence <= 20:
                score = 7.0
            elif avg_words_per_sentence <= 25:
                score = 5.0
            else:
                score = 3.0
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating readability: {e}")
            return 0.0
    
    def _count_conversational_queries(self, soup: BeautifulSoup) -> int:
        """
        Count conversational query optimizations
        
        Args:
            soup: Parsed HTML content
            
        Returns:
            Number of conversational queries optimized
        """
        try:
            # Get all text content
            text = soup.get_text()
            
            # Count question patterns
            conversational_count = 0
            
            for pattern in self.question_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                conversational_count += len(matches)
            
            # Look for natural language patterns
            natural_patterns = [
                r'\bhow\s+to\s+\w+',
                r'\bwhat\s+is\s+\w+',
                r'\bwhy\s+does\s+\w+',
                r'\bwhen\s+should\s+\w+',
                r'\bwhere\s+can\s+\w+'
            ]
            
            for pattern in natural_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                conversational_count += len(matches)
            
            return min(conversational_count, 50)  # Cap at 50
            
        except Exception as e:
            logger.error(f"Error counting conversational queries: {e}")
            return 0
    
    def _get_default_content_result(self) -> ContentResult:
        """
        Return default content result when analysis fails
        
        Returns:
            Default content result
        """
        return ContentResult(
            heading_structure_score=0,
            faq_patterns_found=0,
            qa_content_detected=False,
            word_count=0,
            readability_score=0.0,
            conversational_queries_optimized=0
        )
    
    async def get_content_recommendations(self, result: ContentResult) -> List[str]:
        """
        Get content optimization recommendations
        
        Args:
            result: Content analysis result
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if result.heading_structure_score < 6:
            recommendations.append("Improve heading structure with clear H1 and logical hierarchy")
        
        if result.faq_patterns_found < 3:
            recommendations.append("Add dedicated FAQ sections to address common questions")
        
        if not result.qa_content_detected:
            recommendations.append("Create Q&A content structure for better AI understanding")
        
        if result.word_count < 500:
            recommendations.append("Increase content length to provide comprehensive information")
        
        if result.conversational_queries_optimized < 5:
            recommendations.append("Optimize content for conversational search queries")
        
        return recommendations 