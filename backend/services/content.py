"""
Enhanced Content Analysis Service with FAQ Intelligence for AEO
"""

import re
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from .faq_analyzer import IntelligentFAQAnalyzer, FAQAnalysisResult

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Enhanced content analysis with AI-powered FAQ detection and AEO optimization"""
    
    def __init__(self):
        self.faq_analyzer = IntelligentFAQAnalyzer()
    
    def analyze_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Comprehensive content analysis including advanced FAQ intelligence
        
        Args:
            soup: BeautifulSoup object of webpage content
            
        Returns:
            Dict containing comprehensive content analysis results
        """
        try:
            # Get basic content metrics (original functionality)
            basic_metrics = self._get_basic_metrics(soup)
            
            # Enhanced FAQ intelligence analysis
            faq_analysis = self.faq_analyzer.analyze_faq_intelligence(soup)
            
            # Content structure analysis
            structure_analysis = self._analyze_content_structure(soup)
            
            # AEO-specific content analysis
            aeo_metrics = self._analyze_aeo_content(soup, faq_analysis)
            
            # Calculate overall content intelligence score
            intelligence_score = self._calculate_content_intelligence_score(
                basic_metrics, faq_analysis, structure_analysis, aeo_metrics
            )
            
            return {
                'basic_metrics': basic_metrics,
                'faq_analysis': self._serialize_faq_analysis(faq_analysis),
                'structure_analysis': structure_analysis,
                'aeo_metrics': aeo_metrics,
                'content_intelligence_score': intelligence_score,
                'recommendations': self._generate_content_recommendations(
                    basic_metrics, faq_analysis, structure_analysis, aeo_metrics
                )
            }
            
        except Exception as e:
            logger.error(f"Error in content analysis: {e}")
            return self._fallback_analysis(soup)
    
    def _get_basic_metrics(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Get basic content metrics (original functionality enhanced)"""
        text_content = soup.get_text()
        
        # Word and character counts
        words = len(text_content.split())
        characters = len(text_content)
        
        # Heading analysis
        headings = {
            'h1': len(soup.find_all('h1')),
            'h2': len(soup.find_all('h2')),
            'h3': len(soup.find_all('h3')),
            'h4': len(soup.find_all('h4')),
            'h5': len(soup.find_all('h5')),
            'h6': len(soup.find_all('h6'))
        }
        
        # Link analysis
        internal_links = len([link for link in soup.find_all('a', href=True) 
                            if self._is_internal_link(link['href'])])
        external_links = len([link for link in soup.find_all('a', href=True) 
                            if not self._is_internal_link(link['href'])])
        
        # Image analysis
        images = len(soup.find_all('img'))
        images_with_alt = len(soup.find_all('img', alt=True))
        
        # Content density
        content_density = words / max(characters, 1) if characters > 0 else 0
        
        return {
            'word_count': words,
            'character_count': characters,
            'headings': headings,
            'total_headings': sum(headings.values()),
            'internal_links': internal_links,
            'external_links': external_links,
            'total_links': internal_links + external_links,
            'images': images,
            'images_with_alt': images_with_alt,
            'image_optimization_ratio': images_with_alt / max(images, 1),
            'content_density': content_density,
            'reading_time_minutes': max(words / 200, 1)  # Average reading speed
        }
    
    def _analyze_content_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content structure for AEO optimization"""
        
        # Semantic HTML analysis
        semantic_elements = {
            'article': len(soup.find_all('article')),
            'section': len(soup.find_all('section')),
            'aside': len(soup.find_all('aside')),
            'nav': len(soup.find_all('nav')),
            'main': len(soup.find_all('main')),
            'header': len(soup.find_all('header')),
            'footer': len(soup.find_all('footer'))
        }
        
        # Structured data presence
        structured_data = {
            'json_ld': len(soup.find_all('script', type='application/ld+json')),
            'microdata': len(soup.find_all(attrs={'itemscope': True})),
            'rdfa': len(soup.find_all(attrs={'property': True}))
        }
        
        # List structures (good for featured snippets)
        lists = {
            'ordered_lists': len(soup.find_all('ol')),
            'unordered_lists': len(soup.find_all('ul')),
            'definition_lists': len(soup.find_all('dl'))
        }
        
        # Table structures
        tables = len(soup.find_all('table'))
        
        # Content hierarchy score
        hierarchy_score = self._calculate_hierarchy_score(soup)
        
        return {
            'semantic_elements': semantic_elements,
            'semantic_score': sum(1 for count in semantic_elements.values() if count > 0) / len(semantic_elements),
            'structured_data': structured_data,
            'structured_data_score': sum(1 for count in structured_data.values() if count > 0) / len(structured_data),
            'lists': lists,
            'total_lists': sum(lists.values()),
            'tables': tables,
            'hierarchy_score': hierarchy_score
        }
    
    def _analyze_aeo_content(self, soup: BeautifulSoup, faq_analysis: FAQAnalysisResult) -> Dict[str, Any]:
        """Analyze content specifically for Answer Engine Optimization"""
        text_content = soup.get_text()
        
        # Answer-style content patterns
        answer_patterns = {
            'direct_answers': len(re.findall(r'(?i)\b(yes|no),?\s+', text_content)),
            'step_by_step': len(re.findall(r'(?i)\b(step\s+\d+|first|second|third|next|then|finally)\b', text_content)),
            'numbered_points': len(re.findall(r'\d+\.\s+', text_content)),
            'bullet_points': len(soup.find_all('li')),
            'definitions': len(re.findall(r'(?i)\b\w+\s+is\s+(?:a|an|the)\s+', text_content))
        }
        
        # Conversational language score
        conversational_indicators = [
            r'(?i)\byou\s+(?:can|should|need|want|will)',
            r'(?i)\blet\'s\s+',
            r'(?i)\bhere\'s\s+(?:how|what|why)',
            r'(?i)\bto\s+do\s+this',
            r'(?i)\bsimply\s+',
            r'(?i)\bjust\s+',
        ]
        
        conversational_score = 0
        for pattern in conversational_indicators:
            conversational_score += len(re.findall(pattern, text_content))
        
        # Normalize conversational score
        conversational_score = min(conversational_score / 20, 1.0)
        
        # Featured snippet potential analysis
        snippet_elements = {
            'short_paragraphs': len([p for p in soup.find_all('p') 
                                   if 20 <= len(p.get_text().split()) <= 60]),
            'definition_paragraphs': len(re.findall(r'(?i)^.{10,100}\s+is\s+.{10,200}$', text_content, re.MULTILINE)),
            'how_to_content': len(re.findall(r'(?i)\bhow\s+to\s+\w+', text_content)),
            'comparison_content': len(re.findall(r'(?i)\b(?:vs\.?|versus|compared?\s+to|difference\s+between)\b', text_content))
        }
        
        return {
            'answer_patterns': answer_patterns,
            'answer_richness_score': min(sum(answer_patterns.values()) / 50, 1.0),
            'conversational_score': conversational_score,
            'snippet_elements': snippet_elements,
            'snippet_readiness_score': min(sum(snippet_elements.values()) / 20, 1.0),
            'voice_search_signals': faq_analysis.voice_search_readiness,
            'faq_intelligence_score': faq_analysis.faq_intelligence_score / 100
        }
    
    def _calculate_hierarchy_score(self, soup: BeautifulSoup) -> float:
        """Calculate content hierarchy quality score"""
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headings:
            return 0.0
        
        score = 0.0
        h1_count = len(soup.find_all('h1'))
        
        # Ideal: one H1
        if h1_count == 1:
            score += 0.3
        elif h1_count == 0:
            score -= 0.2
        
        # Check for logical hierarchy
        prev_level = 0
        for heading in headings:
            level = int(heading.name[1])
            
            # Good progression
            if level <= prev_level + 1:
                score += 0.1
            else:
                score -= 0.1  # Skipped levels
            
            prev_level = level
        
        return max(min(score, 1.0), 0.0)
    
    def _calculate_content_intelligence_score(self, basic_metrics: Dict, faq_analysis: FAQAnalysisResult, 
                                            structure_analysis: Dict, aeo_metrics: Dict) -> float:
        """Calculate overall content intelligence score (0-100)"""
        score = 0.0
        
        # Basic content quality (25% weight)
        word_count = basic_metrics['word_count']
        if 300 <= word_count <= 2000:
            score += 15
        elif 200 <= word_count < 300 or 2000 < word_count <= 3000:
            score += 10
        elif word_count >= 100:
            score += 5
        
        # Heading structure (10% weight)
        if basic_metrics['total_headings'] >= 3:
            score += 8
            if structure_analysis['hierarchy_score'] > 0.7:
                score += 2
        elif basic_metrics['total_headings'] >= 1:
            score += 5
        
        # FAQ Intelligence (35% weight) - This is the big upgrade!
        score += faq_analysis.faq_intelligence_score * 0.35
        
        # AEO optimization (20% weight)
        score += aeo_metrics['answer_richness_score'] * 8
        score += aeo_metrics['conversational_score'] * 6
        score += aeo_metrics['snippet_readiness_score'] * 6
        
        # Technical structure (10% weight)
        score += structure_analysis['semantic_score'] * 5
        score += structure_analysis['structured_data_score'] * 5
        
        return min(score, 100)
    
    def _generate_content_recommendations(self, basic_metrics: Dict, faq_analysis: FAQAnalysisResult, 
                                        structure_analysis: Dict, aeo_metrics: Dict) -> List[str]:
        """Generate specific content improvement recommendations"""
        recommendations = []
        
        # FAQ-specific recommendations (most important!)
        recommendations.extend(faq_analysis.improvement_suggestions)
        
        # Content length recommendations
        word_count = basic_metrics['word_count']
        if word_count < 200:
            recommendations.append("Increase content length to at least 300 words for better AEO performance")
        elif word_count > 3000:
            recommendations.append("Consider breaking long content into sections or separate pages for better readability")
        
        # Heading structure
        if basic_metrics['total_headings'] < 3:
            recommendations.append("Add more headings (H2, H3) to improve content structure and scannability")
        
        if structure_analysis['hierarchy_score'] < 0.5:
            recommendations.append("Improve heading hierarchy - use H1 for main title, H2 for sections, H3 for subsections")
        
        # AEO-specific recommendations
        if aeo_metrics['conversational_score'] < 0.3:
            recommendations.append("Use more conversational language (you, your, let's, here's how) for better voice search optimization")
        
        if aeo_metrics['answer_richness_score'] < 0.4:
            recommendations.append("Add more direct answers, numbered lists, and step-by-step instructions")
        
        if aeo_metrics['snippet_readiness_score'] < 0.3:
            recommendations.append("Create more concise paragraphs (20-60 words) that directly answer specific questions")
        
        # Structured data
        if structure_analysis['structured_data_score'] == 0:
            recommendations.append("Add structured data markup (JSON-LD, Schema.org) to help search engines understand your content")
        
        # Images
        if basic_metrics['image_optimization_ratio'] < 0.8 and basic_metrics['images'] > 0:
            recommendations.append("Add alt text to all images for better accessibility and SEO")
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def _serialize_faq_analysis(self, faq_analysis: FAQAnalysisResult) -> Dict[str, Any]:
        """Convert FAQ analysis result to serializable format"""
        return {
            'faq_sections_found': faq_analysis.faq_sections_found,
            'qa_pairs_count': len(faq_analysis.qa_pairs_extracted),
            'qa_pairs': [
                {
                    'question': pair.question,
                    'answer': pair.answer,
                    'answer_length': pair.answer_length,
                    'readability_score': round(pair.readability_score, 2),
                    'confidence': round(pair.confidence, 2),
                    'snippet_potential': round(pair.snippet_potential, 2)
                }
                for pair in faq_analysis.qa_pairs_extracted[:10]  # Limit to top 10 for JSON
            ],
            'question_quality_score': round(faq_analysis.question_quality_score, 2),
            'answer_completeness_score': round(faq_analysis.answer_completeness_score, 2),
            'faq_intelligence_score': round(faq_analysis.faq_intelligence_score, 1),
            'voice_search_readiness': round(faq_analysis.voice_search_readiness, 2),
            'featured_snippet_potential': faq_analysis.featured_snippet_potential,
            'improvement_suggestions': faq_analysis.improvement_suggestions
        }
    
    def _is_internal_link(self, href: str) -> bool:
        """Check if a link is internal"""
        if not href:
            return False
        return (href.startswith('/') or 
                href.startswith('#') or 
                href.startswith('mailto:') or
                not href.startswith('http'))
    
    def _fallback_analysis(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Fallback analysis in case of errors"""
        text_content = soup.get_text()
        word_count = len(text_content.split())
        
        return {
            'basic_metrics': {
                'word_count': word_count,
                'character_count': len(text_content),
                'headings': {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0},
                'total_headings': 0,
                'internal_links': 0,
                'external_links': 0,
                'total_links': 0,
                'images': 0,
                'images_with_alt': 0,
                'image_optimization_ratio': 0,
                'content_density': 0,
                'reading_time_minutes': max(word_count / 200, 1)
            },
            'faq_analysis': {
                'faq_sections_found': 0,
                'qa_pairs_count': 0,
                'qa_pairs': [],
                'question_quality_score': 0,
                'answer_completeness_score': 0,
                'faq_intelligence_score': 0,
                'voice_search_readiness': 0,
                'featured_snippet_potential': 0,
                'improvement_suggestions': ["Error in analysis - please check content format"]
            },
            'structure_analysis': {},
            'aeo_metrics': {},
            'content_intelligence_score': 20,  # Basic fallback score
            'recommendations': ["Unable to perform full analysis - please ensure content is properly formatted"]
        } 