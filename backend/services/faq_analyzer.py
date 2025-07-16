"""
Intelligent FAQ Detection and Analysis Service for AEO Optimization
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from bs4 import BeautifulSoup
import spacy
import textstat
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QAPair:
    """Represents a question-answer pair with quality metrics"""
    question: str
    answer: str
    answer_length: int
    readability_score: float
    position: int
    confidence: float
    snippet_potential: float


@dataclass
class FAQAnalysisResult:
    """Comprehensive FAQ analysis results"""
    faq_sections_found: int
    qa_pairs_extracted: List[QAPair]
    question_quality_score: float
    answer_completeness_score: float
    faq_intelligence_score: float
    voice_search_readiness: float
    featured_snippet_potential: int
    improvement_suggestions: List[str]


class IntelligentFAQAnalyzer:
    """Advanced FAQ detection and analysis using NLP"""
    
    def __init__(self):
        """Initialize the FAQ analyzer with NLP capabilities"""
        try:
            # Load spaCy English model
            self.nlp = spacy.load("en_core_web_sm")
        except IOError:
            logger.error("spaCy English model not found. Please install: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Enhanced FAQ detection patterns
        self.faq_section_patterns = [
            r'(?i)frequently\s+asked\s+questions?',
            r'(?i)common\s+questions?',
            r'(?i)f\.?a\.?q\.?s?',
            r'(?i)q\s*&\s*a',
            r'(?i)questions?\s+(?:and\s+)?answers?',
            r'(?i)help\s+(?:center|section)',
            r'(?i)knowledge\s+base',
            r'(?i)support\s+questions?',
            r'(?i)customer\s+(?:questions?|support)',
        ]
        
        # Question starter patterns (comprehensive)
        self.question_starters = [
            r'(?i)^(what|how|why|when|where|who|which|can|do|does|is|are|will|would|should|could)\s',
            r'(?i)^(have\s+you|did\s+you|are\s+you|would\s+you)',
            r'(?i)^(is\s+it|can\s+i|how\s+do\s+i|what\s+if|how\s+can)',
            r'(?i)^(may\s+i|might\s+i|shall\s+i)',
        ]
        
        # Conversational patterns for voice search
        self.conversational_patterns = [
            r'(?i)\bhow\s+to\s+\w+',
            r'(?i)\bwhat\s+is\s+(?:the\s+)?best\s+',
            r'(?i)\bwhere\s+(?:can\s+i|do\s+i|to)\s+',
            r'(?i)\bwhen\s+should\s+(?:i|you)\s+',
            r'(?i)\bwhy\s+(?:does|do|is|are)\s+',
        ]
    
    def analyze_faq_intelligence(self, soup: BeautifulSoup) -> FAQAnalysisResult:
        """
        Comprehensive FAQ intelligence analysis
        
        Args:
            soup: BeautifulSoup object of webpage content
            
        Returns:
            FAQAnalysisResult with detailed analysis
        """
        if not self.nlp:
            logger.warning("spaCy model not available, using basic analysis")
            return self._basic_faq_analysis(soup)
        
        text_content = soup.get_text()
        
        # 1. Detect FAQ sections using multiple strategies
        faq_sections = self._detect_faq_sections(soup)
        
        # 2. Extract and analyze Q&A pairs
        qa_pairs = self._extract_qa_pairs(soup, text_content)
        
        # 3. Analyze question quality
        question_quality = self._analyze_question_quality(qa_pairs)
        
        # 4. Assess answer completeness
        answer_completeness = self._assess_answer_completeness(qa_pairs)
        
        # 5. Calculate voice search readiness
        voice_readiness = self._calculate_voice_search_readiness(qa_pairs, text_content)
        
        # 6. Assess featured snippet potential
        snippet_potential = self._assess_featured_snippet_potential(qa_pairs)
        
        # 7. Calculate overall FAQ intelligence score
        faq_score = self._calculate_faq_intelligence_score(
            faq_sections, qa_pairs, question_quality, answer_completeness, voice_readiness
        )
        
        # 8. Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(
            faq_sections, qa_pairs, question_quality, answer_completeness
        )
        
        return FAQAnalysisResult(
            faq_sections_found=len(faq_sections),
            qa_pairs_extracted=qa_pairs,
            question_quality_score=question_quality,
            answer_completeness_score=answer_completeness,
            faq_intelligence_score=faq_score,
            voice_search_readiness=voice_readiness,
            featured_snippet_potential=snippet_potential,
            improvement_suggestions=suggestions
        )
    
    def _detect_faq_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Detect FAQ sections using multiple strategies"""
        faq_sections = []
        
        # Strategy 1: Text pattern matching
        for pattern in self.faq_section_patterns:
            elements = soup.find_all(text=re.compile(pattern))
            for element in elements:
                parent = element.parent
                if parent:
                    faq_sections.append({
                        'type': 'text_pattern',
                        'element': parent,
                        'confidence': 0.9,
                        'pattern': pattern
                    })
        
        # Strategy 2: Semantic HTML structure
        semantic_selectors = [
            'section[aria-label*="faq" i]',
            'div[class*="faq" i]',
            'div[id*="faq" i]',
            'details',  # Accordion structures
            'div[class*="accordion" i]',
            'div[class*="question" i]',
            'section[class*="help" i]',
        ]
        
        for selector in semantic_selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    faq_sections.append({
                        'type': 'semantic_html',
                        'element': element,
                        'confidence': 0.8,
                        'selector': selector
                    })
            except Exception as e:
                logger.debug(f"Error with selector {selector}: {e}")
        
        # Strategy 3: Question density analysis
        all_sections = soup.find_all(['section', 'div', 'article'])
        for section in all_sections:
            text = section.get_text()
            question_count = sum(1 for pattern in self.question_starters 
                               if re.search(pattern, text))
            if question_count >= 3:  # High question density
                faq_sections.append({
                    'type': 'question_density',
                    'element': section,
                    'confidence': min(0.5 + (question_count * 0.1), 0.9),
                    'question_count': question_count
                })
        
        return faq_sections
    
    def _extract_qa_pairs(self, soup: BeautifulSoup, text: str) -> List[QAPair]:
        """Extract question-answer pairs using advanced NLP"""
        qa_pairs = []
        
        try:
            # Process text with spaCy for advanced analysis
            doc = self.nlp(text[:1000000])  # Limit text length for performance
            
            # Find sentences that are questions
            questions = []
            sentences = list(doc.sents)
            
            for i, sent in enumerate(sentences):
                sent_text = sent.text.strip()
                
                # Check if sentence is a question
                if (sent_text.endswith('?') or 
                    any(re.match(pattern, sent_text) for pattern in self.question_starters)):
                    
                    # Calculate question confidence
                    confidence = self._calculate_question_confidence(sent_text)
                    if confidence > 0.3:
                        questions.append({
                            'text': sent_text,
                            'index': i,
                            'confidence': confidence
                        })
            
            # For each question, find the following answer
            for question_data in questions:
                q_index = question_data['index']
                question = question_data['text']
                
                # Look for answer in next 1-5 sentences
                answer_sentences = sentences[q_index+1:q_index+6]
                
                if answer_sentences:
                    answer_texts = []
                    total_words = 0
                    
                    for ans_sent in answer_sentences:
                        ans_text = ans_sent.text.strip()
                        word_count = len(ans_text.split())
                        
                        # Stop if we hit another question
                        if (ans_text.endswith('?') or 
                            any(re.match(pattern, ans_text) for pattern in self.question_starters)):
                            break
                        
                        answer_texts.append(ans_text)
                        total_words += word_count
                        
                        # Stop if answer is getting too long
                        if total_words > 200:
                            break
                    
                    if answer_texts:
                        answer = ' '.join(answer_texts)
                        
                        # Calculate readability and snippet potential
                        readability = self._calculate_readability(answer)
                        snippet_potential = self._calculate_snippet_potential(question, answer)
                        
                        qa_pair = QAPair(
                            question=question,
                            answer=answer,
                            answer_length=total_words,
                            readability_score=readability,
                            position=q_index,
                            confidence=question_data['confidence'],
                            snippet_potential=snippet_potential
                        )
                        
                        qa_pairs.append(qa_pair)
        
        except Exception as e:
            logger.error(f"Error in Q&A extraction: {e}")
        
        return qa_pairs[:20]  # Limit to top 20 pairs
    
    def _calculate_question_confidence(self, question: str) -> float:
        """Calculate confidence score for a question"""
        score = 0.0
        
        # Base score for question mark
        if question.endswith('?'):
            score += 0.3
        
        # Score for question starters
        for pattern in self.question_starters:
            if re.match(pattern, question):
                score += 0.4
                break
        
        # Score for question length (5-20 words is ideal)
        word_count = len(question.split())
        if 5 <= word_count <= 20:
            score += 0.3
        elif word_count < 5:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score using textstat"""
        try:
            # Flesch Reading Ease (higher is more readable)
            flesch_score = textstat.flesch_reading_ease(text)
            # Convert to 0-1 scale (60+ is good, 80+ is very good)
            return min(max(flesch_score / 100, 0), 1)
        except:
            return 0.5  # Default moderate readability
    
    def _calculate_snippet_potential(self, question: str, answer: str) -> float:
        """Calculate potential for featured snippets"""
        score = 0.0
        
        # Answer length (40-60 words is ideal for snippets)
        word_count = len(answer.split())
        if 30 <= word_count <= 80:
            score += 0.4
        elif 20 <= word_count <= 100:
            score += 0.2
        
        # Question quality
        if any(pattern in question.lower() for pattern in ['how to', 'what is', 'how do', 'why does']):
            score += 0.3
        
        # Answer structure
        if any(indicator in answer.lower() for indicator in [
            'first', 'second', 'next', 'then', 'finally', 'step'
        ]):
            score += 0.2
        
        # Readability
        readability = self._calculate_readability(answer)
        score += readability * 0.1
        
        return min(score, 1.0)
    
    def _analyze_question_quality(self, qa_pairs: List[QAPair]) -> float:
        """Analyze overall quality of questions for AEO"""
        if not qa_pairs:
            return 0.0
        
        quality_scores = []
        
        for pair in qa_pairs:
            score = 0.0
            question = pair.question.lower()
            
            # Conversational language patterns
            for pattern in self.conversational_patterns:
                if re.search(pattern, question):
                    score += 0.2
                    break
            
            # Natural question starters
            natural_starters = ['how do i', 'what is', 'why does', 'when should', 'where can']
            if any(starter in question for starter in natural_starters):
                score += 0.3
            
            # Question specificity (not too vague)
            if len(question.split()) >= 4:
                score += 0.2
            
            # Use confidence from extraction
            score += pair.confidence * 0.3
            
            quality_scores.append(min(score, 1.0))
        
        return sum(quality_scores) / len(quality_scores)
    
    def _assess_answer_completeness(self, qa_pairs: List[QAPair]) -> float:
        """Assess completeness and quality of answers"""
        if not qa_pairs:
            return 0.0
        
        completeness_scores = []
        
        for pair in qa_pairs:
            score = 0.0
            
            # Answer length (20-150 words ideal for featured snippets)
            word_count = pair.answer_length
            if 20 <= word_count <= 150:
                score += 0.4
            elif 10 <= word_count < 20:
                score += 0.2
            elif 150 < word_count <= 200:
                score += 0.3
            
            # Readability
            if pair.readability_score > 0.6:
                score += 0.3
            elif pair.readability_score > 0.4:
                score += 0.2
            
            # Actionable content indicators
            actionable_indicators = [
                'step', 'first', 'next', 'then', 'finally',
                'you can', 'you should', 'you need to', 'to do this'
            ]
            if any(indicator in pair.answer.lower() for indicator in actionable_indicators):
                score += 0.3
            
            completeness_scores.append(min(score, 1.0))
        
        return sum(completeness_scores) / len(completeness_scores)
    
    def _calculate_voice_search_readiness(self, qa_pairs: List[QAPair], text: str) -> float:
        """Calculate readiness for voice search optimization"""
        score = 0.0
        
        # Conversational query presence
        conversational_count = 0
        for pattern in self.conversational_patterns:
            conversational_count += len(re.findall(pattern, text.lower()))
        
        # Normalize conversational score
        conversational_score = min(conversational_count / 10, 1.0)
        score += conversational_score * 0.4
        
        # Natural language questions
        natural_questions = sum(1 for pair in qa_pairs 
                              if any(starter in pair.question.lower() 
                                   for starter in ['how do', 'what is', 'why does', 'when should']))
        
        if qa_pairs:
            natural_ratio = natural_questions / len(qa_pairs)
            score += natural_ratio * 0.3
        
        # Answer format for voice
        voice_friendly_answers = sum(1 for pair in qa_pairs 
                                   if 20 <= pair.answer_length <= 50)  # Ideal for voice
        
        if qa_pairs:
            voice_ratio = voice_friendly_answers / len(qa_pairs)
            score += voice_ratio * 0.3
        
        return min(score, 1.0)
    
    def _assess_featured_snippet_potential(self, qa_pairs: List[QAPair]) -> int:
        """Count potential featured snippets"""
        return sum(1 for pair in qa_pairs if pair.snippet_potential > 0.6)
    
    def _calculate_faq_intelligence_score(self, faq_sections: List[Dict], qa_pairs: List[QAPair], 
                                        question_quality: float, answer_completeness: float, 
                                        voice_readiness: float) -> float:
        """Calculate overall FAQ intelligence score (0-100)"""
        score = 0.0
        
        # FAQ section presence (0-20 points)
        if faq_sections:
            section_score = min(len(faq_sections) * 5, 20)
            high_confidence_sections = sum(1 for section in faq_sections if section.get('confidence', 0) > 0.8)
            section_score += min(high_confidence_sections * 5, 10)
            score += min(section_score, 30)
        
        # Q&A pairs quantity and quality (0-30 points)
        if qa_pairs:
            pair_count_score = min(len(qa_pairs) * 2, 15)
            high_quality_pairs = sum(1 for pair in qa_pairs if pair.confidence > 0.7)
            quality_score = min(high_quality_pairs * 3, 15)
            score += pair_count_score + quality_score
        
        # Question quality (0-20 points)
        score += question_quality * 20
        
        # Answer completeness (0-20 points)
        score += answer_completeness * 20
        
        return min(score, 100)
    
    def _generate_improvement_suggestions(self, faq_sections: List[Dict], qa_pairs: List[QAPair], 
                                        question_quality: float, answer_completeness: float) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        if len(faq_sections) == 0:
            suggestions.append("Add a dedicated FAQ section to your website with clear headings and structure")
        
        if len(qa_pairs) < 5:
            suggestions.append("Increase the number of question-answer pairs to at least 5-10 for better AEO coverage")
        
        if question_quality < 0.6:
            suggestions.append("Improve question quality by using more natural, conversational language (how do I, what is, etc.)")
        
        if answer_completeness < 0.6:
            suggestions.append("Enhance answer completeness with 20-150 word responses that include actionable steps")
        
        snippet_ready = sum(1 for pair in qa_pairs if pair.snippet_potential > 0.6)
        if snippet_ready < 3:
            suggestions.append("Optimize more answers for featured snippets with concise, well-structured responses")
        
        low_readability = sum(1 for pair in qa_pairs if pair.readability_score < 0.4)
        if low_readability > len(qa_pairs) * 0.3:
            suggestions.append("Improve answer readability by using simpler language and shorter sentences")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _basic_faq_analysis(self, soup: BeautifulSoup) -> FAQAnalysisResult:
        """Fallback basic analysis when spaCy is not available"""
        text_content = soup.get_text()
        
        # Basic FAQ section detection
        faq_count = 0
        for pattern in self.faq_section_patterns:
            if re.search(pattern, text_content, re.IGNORECASE):
                faq_count += 1
        
        # Basic question counting
        question_count = 0
        for pattern in self.question_starters:
            question_count += len(re.findall(pattern, text_content))
        
        # Simple scoring
        basic_score = min((faq_count * 20) + (min(question_count, 10) * 5), 100)
        
        return FAQAnalysisResult(
            faq_sections_found=faq_count,
            qa_pairs_extracted=[],
            question_quality_score=0.5,
            answer_completeness_score=0.5,
            faq_intelligence_score=basic_score,
            voice_search_readiness=0.3,
            featured_snippet_potential=0,
            improvement_suggestions=["Install spaCy English model for advanced analysis"]
        )