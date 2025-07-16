"""
Advanced Content Intelligence & Entity Recognition Service
Adds semantic analysis and dynamic recommendations for 70%+ AEO intelligence
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from bs4 import BeautifulSoup
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class EntityMatch:
    """Represents a recognized entity in content"""
    entity: str
    entity_type: str
    confidence: float
    context: str
    positions: List[int]
    relevance_score: float


@dataclass
class SemanticInsight:
    """Semantic analysis insight"""
    topic: str
    confidence: float
    keywords: List[str]
    semantic_density: float
    content_depth: str


@dataclass
class DynamicRecommendation:
    """AI-generated dynamic recommendation"""
    title: str
    description: str
    impact_score: float
    implementation_effort: str
    code_example: Optional[str]
    expected_improvement: str
    category: str


@dataclass
class AdvancedContentResult:
    """Advanced content intelligence analysis results"""
    content_intelligence_score: float
    semantic_insights: List[SemanticInsight]
    entities_detected: List[EntityMatch]
    topic_authority_score: float
    content_depth_analysis: Dict[str, Any]
    voice_search_optimization: Dict[str, Any]
    dynamic_recommendations: List[DynamicRecommendation]
    competitive_advantages: List[str]
    content_gaps: List[str]


class AdvancedContentIntelligence:
    """Advanced content analysis with semantic understanding and entity recognition"""
    
    def __init__(self):
        """Initialize advanced content intelligence"""
        
        # Entity recognition patterns (simplified)
        self.entity_patterns = {
            'ORGANIZATION': [
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|LLC|Corp|Company|Ltd|Limited)\b',
                r'\b(?:Google|Facebook|Microsoft|Amazon|Apple|IBM|Oracle)\b',
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\s+(?:Agency|Group|Solutions|Technologies)\b'
            ],
            'TECHNOLOGY': [
                r'\b(?:AI|ML|API|SEO|AEO|NLP|JSON-LD|schema|markup|algorithm)\b',
                r'\b(?:artificial\s+intelligence|machine\s+learning|natural\s+language)\b',
                r'\b(?:voice\s+search|featured\s+snippets|answer\s+engine)\b'
            ],
            'PRODUCT': [
                r'\b(?:software|platform|tool|service|application|system)\b',
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Pro|Premium|Enterprise|Basic)\b'
            ],
            'PERSON': [
                r'\b(?:CEO|CTO|founder|developer|engineer|analyst|expert)\b',
                r'\bDr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
                r'\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:,\s+(?:PhD|MD|MBA))?\b'
            ]
        }
        
        # Semantic topic patterns
        self.topic_patterns = {
            'SEO_OPTIMIZATION': [
                r'(?i)\b(?:seo|search\s+engine\s+optimization|ranking|serp)\b',
                r'(?i)\b(?:keywords?|meta\s+tags?|title\s+tags?)\b',
                r'(?i)\b(?:backlinks?|link\s+building|page\s+authority)\b'
            ],
            'AEO_STRATEGY': [
                r'(?i)\b(?:aeo|answer\s+engine\s+optimization|voice\s+search)\b',
                r'(?i)\b(?:featured\s+snippets?|rich\s+results?|ai\s+overviews?)\b',
                r'(?i)\b(?:conversational\s+queries?|question\s+answering)\b'
            ],
            'CONTENT_MARKETING': [
                r'(?i)\b(?:content\s+marketing|content\s+strategy|blog\s+posts?)\b',
                r'(?i)\b(?:storytelling|engagement|audience|personas?)\b',
                r'(?i)\b(?:editorial\s+calendar|content\s+planning)\b'
            ],
            'TECHNICAL_SEO': [
                r'(?i)\b(?:technical\s+seo|site\s+speed|core\s+web\s+vitals)\b',
                r'(?i)\b(?:schema\s+markup|structured\s+data|json-ld)\b',
                r'(?i)\b(?:crawling|indexing|robots\.txt|sitemap)\b'
            ],
            'ANALYTICS': [
                r'(?i)\b(?:analytics|tracking|metrics|kpis?|data)\b',
                r'(?i)\b(?:conversion|ctr|bounce\s+rate|traffic)\b',
                r'(?i)\b(?:reporting|dashboard|insights)\b'
            ]
        }
        
        # Voice search optimization patterns
        self.voice_search_patterns = {
            'QUESTION_WORDS': [
                r'\b(?:what|how|why|when|where|who|which|can|should|will|does|is|are)\b',
                r'\b(?:what\'s|how\'s|why\'s|when\'s|where\'s|who\'s)\b'
            ],
            'LOCAL_INTENT': [
                r'\b(?:near\s+me|nearby|local|in\s+my\s+area)\b',
                r'\b(?:directions\s+to|hours|address|phone\s+number)\b'
            ],
            'CONVERSATIONAL': [
                r'\b(?:tell\s+me|show\s+me|help\s+me|I\s+need|I\s+want)\b',
                r'\b(?:best\s+way\s+to|easiest\s+way\s+to|fastest\s+way\s+to)\b'
            ],
            'LONG_TAIL': [
                r'\b\w+\s+\w+\s+\w+\s+\w+\s+\w+\b',  # 5+ word phrases
                r'\b(?:step\s+by\s+step|detailed\s+guide|complete\s+tutorial)\b'
            ]
        }
        
        # Content depth indicators
        self.depth_indicators = {
            'COMPREHENSIVE': [
                r'\b(?:comprehensive|complete|detailed|thorough|in-depth)\b',
                r'\b(?:everything\s+you\s+need|ultimate\s+guide|complete\s+guide)\b'
            ],
            'TUTORIAL': [
                r'\b(?:tutorial|guide|how-to|step-by-step|walkthrough)\b',
                r'\b(?:instructions|directions|procedure)\b'
            ],
            'ANALYSIS': [
                r'\b(?:analysis|research|study|comparison|review)\b',
                r'\b(?:data|statistics|findings|results)\b'
            ],
            'EXPERT_CONTENT': [
                r'\b(?:expert|professional|industry|authority)\b',
                r'\b(?:certification|accredited|verified|proven)\b'
            ]
        }
        
    def analyze_advanced_content(self, soup: BeautifulSoup, basic_analysis: Dict[str, Any]) -> AdvancedContentResult:
        """
        Perform advanced content intelligence analysis
        
        Args:
            soup: BeautifulSoup object of webpage content
            basic_analysis: Basic content analysis results
            
        Returns:
            AdvancedContentResult with comprehensive intelligence
        """
        logger.info("Starting advanced content intelligence analysis")
        
        try:
            text_content = soup.get_text()
            
            # 1. Entity Recognition
            entities = self._recognize_entities(text_content)
            
            # 2. Semantic Analysis
            semantic_insights = self._analyze_semantic_topics(text_content)
            
            # 3. Topic Authority Assessment
            topic_authority = self._calculate_topic_authority(text_content, entities, semantic_insights)
            
            # 4. Content Depth Analysis
            depth_analysis = self._analyze_content_depth(text_content, soup)
            
            # 5. Voice Search Optimization Analysis
            voice_optimization = self._analyze_voice_search_optimization(text_content, soup)
            
            # 6. Generate Dynamic Recommendations
            dynamic_recommendations = self._generate_dynamic_recommendations(
                entities, semantic_insights, depth_analysis, voice_optimization, basic_analysis
            )
            
            # 7. Identify Competitive Advantages and Gaps
            competitive_advantages, content_gaps = self._analyze_competitive_positioning(
                text_content, semantic_insights, depth_analysis
            )
            
            # 8. Calculate Overall Content Intelligence Score
            content_intelligence_score = self._calculate_content_intelligence_score(
                entities, semantic_insights, topic_authority, depth_analysis, 
                voice_optimization, basic_analysis
            )
            
            result = AdvancedContentResult(
                content_intelligence_score=content_intelligence_score,
                semantic_insights=semantic_insights,
                entities_detected=entities,
                topic_authority_score=topic_authority,
                content_depth_analysis=depth_analysis,
                voice_search_optimization=voice_optimization,
                dynamic_recommendations=dynamic_recommendations,
                competitive_advantages=competitive_advantages,
                content_gaps=content_gaps
            )
            
            logger.info(f"Advanced content analysis complete. Intelligence Score: {content_intelligence_score:.1f}/100")
            return result
            
        except Exception as e:
            logger.error(f"Advanced content analysis failed: {e}")
            return self._get_default_advanced_result()
    
    def _recognize_entities(self, text: str) -> List[EntityMatch]:
        """Recognize entities in content using pattern matching"""
        entities = []
        text_lower = text.lower()
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group().strip()
                    
                    # Calculate confidence based on context and frequency
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(text), match.end() + 50)
                    context = text[context_start:context_end]
                    
                    confidence = self._calculate_entity_confidence(entity_text, context, entity_type)
                    relevance = self._calculate_entity_relevance(entity_text, text_lower, entity_type)
                    
                    if confidence > 0.6:  # Minimum confidence threshold
                        entities.append(EntityMatch(
                            entity=entity_text,
                            entity_type=entity_type,
                            confidence=confidence,
                            context=context,
                            positions=[match.start()],
                            relevance_score=relevance
                        ))
        
        # Deduplicate and sort by relevance
        unique_entities = {}
        for entity in entities:
            key = (entity.entity.lower(), entity.entity_type)
            if key not in unique_entities or entity.confidence > unique_entities[key].confidence:
                unique_entities[key] = entity
        
        return sorted(unique_entities.values(), key=lambda x: x.relevance_score, reverse=True)[:20]
    
    def _calculate_entity_confidence(self, entity: str, context: str, entity_type: str) -> float:
        """Calculate confidence score for entity recognition"""
        confidence = 0.7  # Base confidence
        
        # Boost confidence based on context keywords
        context_lower = context.lower()
        entity_lower = entity.lower()
        
        if entity_type == 'TECHNOLOGY':
            tech_keywords = ['software', 'platform', 'api', 'algorithm', 'system']
            if any(keyword in context_lower for keyword in tech_keywords):
                confidence += 0.2
        
        elif entity_type == 'ORGANIZATION':
            org_keywords = ['company', 'business', 'enterprise', 'corporation']
            if any(keyword in context_lower for keyword in org_keywords):
                confidence += 0.15
        
        # Penalize very short entities
        if len(entity) < 3:
            confidence -= 0.3
        
        # Boost confidence for entities with multiple words
        if len(entity.split()) > 1:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_entity_relevance(self, entity: str, text: str, entity_type: str) -> float:
        """Calculate relevance of entity to overall content"""
        entity_lower = entity.lower()
        
        # Count occurrences
        occurrence_count = text.count(entity_lower)
        
        # Calculate frequency-based relevance
        frequency_score = min(occurrence_count * 0.1, 1.0)
        
        # Weight by entity type importance for AEO
        type_weights = {
            'TECHNOLOGY': 1.0,
            'ORGANIZATION': 0.8,
            'PRODUCT': 0.9,
            'PERSON': 0.6
        }
        
        type_weight = type_weights.get(entity_type, 0.5)
        
        return frequency_score * type_weight
    
    def _analyze_semantic_topics(self, text: str) -> List[SemanticInsight]:
        """Analyze semantic topics and themes in content"""
        insights = []
        text_lower = text.lower()
        
        for topic, patterns in self.topic_patterns.items():
            matches = []
            keywords = []
            
            for pattern in patterns:
                pattern_matches = re.findall(pattern, text_lower)
                matches.extend(pattern_matches)
                
                # Extract keywords from matches
                for match in pattern_matches:
                    if isinstance(match, str):
                        keywords.extend(match.split())
                    elif isinstance(match, tuple):
                        keywords.extend(' '.join(match).split())
            
            if matches:
                # Calculate topic confidence and density
                unique_matches = set(matches)
                confidence = min(len(unique_matches) * 0.15, 1.0)
                semantic_density = len(matches) / len(text.split()) * 1000  # Density per 1000 words
                
                # Determine content depth for this topic
                depth = self._determine_topic_depth(topic, matches, text_lower)
                
                insights.append(SemanticInsight(
                    topic=topic.replace('_', ' ').title(),
                    confidence=confidence,
                    keywords=list(set(keywords))[:10],  # Top 10 unique keywords
                    semantic_density=semantic_density,
                    content_depth=depth
                ))
        
        return sorted(insights, key=lambda x: x.confidence, reverse=True)[:8]
    
    def _determine_topic_depth(self, topic: str, matches: List[str], text: str) -> str:
        """Determine depth of coverage for a topic"""
        match_count = len(matches)
        unique_count = len(set(matches))
        
        if unique_count >= 8 and match_count >= 15:
            return "Comprehensive"
        elif unique_count >= 5 and match_count >= 8:
            return "Detailed"
        elif unique_count >= 3 and match_count >= 5:
            return "Moderate"
        else:
            return "Basic"
    
    def _calculate_topic_authority(self, text: str, entities: List[EntityMatch], 
                                  insights: List[SemanticInsight]) -> float:
        """Calculate topic authority score"""
        score = 0.0
        
        # Entity authority (30% weight)
        high_relevance_entities = [e for e in entities if e.relevance_score > 0.7]
        entity_score = min(len(high_relevance_entities) * 0.1, 0.3)
        score += entity_score
        
        # Semantic depth (40% weight)
        comprehensive_topics = [i for i in insights if i.content_depth in ['Comprehensive', 'Detailed']]
        depth_score = min(len(comprehensive_topics) * 0.1, 0.4)
        score += depth_score
        
        # Content length authority (20% weight)
        word_count = len(text.split())
        if word_count >= 2000:
            length_score = 0.2
        elif word_count >= 1000:
            length_score = 0.15
        elif word_count >= 500:
            length_score = 0.1
        else:
            length_score = 0.05
        score += length_score
        
        # Expert indicators (10% weight)
        expert_patterns = [
            r'\b(?:according\s+to\s+experts?|research\s+shows|studies\s+indicate)\b',
            r'\b(?:data\s+reveals|statistics\s+show|proven\s+methods?)\b',
            r'\b(?:industry\s+standards?|best\s+practices?|professional)\b'
        ]
        
        expert_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                           for pattern in expert_patterns)
        expert_score = min(expert_matches * 0.02, 0.1)
        score += expert_score
        
        return min(score * 100, 100)  # Convert to 0-100 scale
    
    def _analyze_content_depth(self, text: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content depth and structure"""
        analysis = {
            'depth_indicators': {},
            'structure_score': 0,
            'comprehensiveness': 0,
            'detail_level': 'Basic'
        }
        
        text_lower = text.lower()
        
        # Analyze depth indicators
        for depth_type, patterns in self.depth_indicators.items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, text_lower))
            
            analysis['depth_indicators'][depth_type] = len(matches)
        
        # Calculate structure score
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        lists = soup.find_all(['ul', 'ol', 'dl'])
        paragraphs = soup.find_all('p')
        
        structure_elements = len(headings) + len(lists) + len(paragraphs)
        analysis['structure_score'] = min(structure_elements * 2, 100)
        
        # Calculate comprehensiveness
        word_count = len(text.split())
        total_depth_indicators = sum(analysis['depth_indicators'].values())
        
        comprehensiveness = 0
        if word_count >= 2000 and total_depth_indicators >= 10:
            comprehensiveness = 90
            analysis['detail_level'] = 'Comprehensive'
        elif word_count >= 1000 and total_depth_indicators >= 5:
            comprehensiveness = 70
            analysis['detail_level'] = 'Detailed'
        elif word_count >= 500 and total_depth_indicators >= 3:
            comprehensiveness = 50
            analysis['detail_level'] = 'Moderate'
        else:
            comprehensiveness = 30
            analysis['detail_level'] = 'Basic'
        
        analysis['comprehensiveness'] = comprehensiveness
        
        return analysis
    
    def _analyze_voice_search_optimization(self, text: str, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze voice search optimization potential"""
        analysis = {
            'question_optimization': 0,
            'conversational_score': 0,
            'local_intent_score': 0,
            'long_tail_optimization': 0,
            'voice_readiness_score': 0,
            'improvement_areas': []
        }
        
        text_lower = text.lower()
        
        # Analyze each voice search pattern category
        for category, patterns in self.voice_search_patterns.items():
            matches = []
            for pattern in patterns:
                matches.extend(re.findall(pattern, text_lower))
            
            match_count = len(matches)
            category_score = min(match_count * 5, 100)
            
            if category == 'QUESTION_WORDS':
                analysis['question_optimization'] = category_score
            elif category == 'CONVERSATIONAL':
                analysis['conversational_score'] = category_score
            elif category == 'LOCAL_INTENT':
                analysis['local_intent_score'] = category_score
            elif category == 'LONG_TAIL':
                analysis['long_tail_optimization'] = category_score
        
        # Calculate overall voice readiness
        scores = [
            analysis['question_optimization'],
            analysis['conversational_score'],
            analysis['long_tail_optimization']
        ]
        
        analysis['voice_readiness_score'] = sum(scores) / len(scores)
        
        # Identify improvement areas
        if analysis['question_optimization'] < 40:
            analysis['improvement_areas'].append("Add more question-based headings and content")
        
        if analysis['conversational_score'] < 30:
            analysis['improvement_areas'].append("Use more conversational language and natural phrases")
        
        if analysis['long_tail_optimization'] < 50:
            analysis['improvement_areas'].append("Target more long-tail, specific queries")
        
        return analysis
    
    def _generate_dynamic_recommendations(self, entities: List[EntityMatch], 
                                        insights: List[SemanticInsight],
                                        depth_analysis: Dict[str, Any],
                                        voice_optimization: Dict[str, Any],
                                        basic_analysis: Dict[str, Any]) -> List[DynamicRecommendation]:
        """Generate AI-powered dynamic recommendations"""
        recommendations = []
        
        # Entity-based recommendations
        tech_entities = [e for e in entities if e.entity_type == 'TECHNOLOGY']
        if len(tech_entities) >= 3:
            recommendations.append(DynamicRecommendation(
                title="Leverage Technology Entity Authority",
                description=f"You mention {len(tech_entities)} technology entities. Create dedicated content around these to build topical authority.",
                impact_score=0.8,
                implementation_effort="Medium",
                code_example=None,
                expected_improvement="15-25% increase in technical query rankings",
                category="Content Strategy"
            ))
        
        # Semantic insight recommendations
        high_confidence_topics = [i for i in insights if i.confidence > 0.7]
        if high_confidence_topics:
            topic_names = [t.topic for t in high_confidence_topics]
            recommendations.append(DynamicRecommendation(
                title="Expand High-Authority Topics",
                description=f"Your content shows strong authority in: {', '.join(topic_names)}. Create supporting content to dominate these topics.",
                impact_score=0.9,
                implementation_effort="High",
                code_example=None,
                expected_improvement="20-35% increase in topic-related organic traffic",
                category="Topic Authority"
            ))
        
        # Content depth recommendations
        if depth_analysis['comprehensiveness'] < 60:
            recommendations.append(DynamicRecommendation(
                title="Enhance Content Depth for AEO",
                description="Increase content comprehensiveness to improve answer engine visibility. Add more detailed explanations and examples.",
                impact_score=0.7,
                implementation_effort="Medium",
                code_example="""
<!-- Add detailed sections like this -->
<section class="detailed-explanation">
    <h3>Detailed Implementation Guide</h3>
    <ol>
        <li>Step 1: Comprehensive explanation...</li>
        <li>Step 2: Detailed process...</li>
        <li>Step 3: Advanced techniques...</li>
    </ol>
</section>
                """,
                expected_improvement="10-20% increase in featured snippet chances",
                category="Content Enhancement"
            ))
        
        # Voice search recommendations
        if voice_optimization['voice_readiness_score'] < 60:
            recommendations.append(DynamicRecommendation(
                title="Optimize for Voice Search Queries",
                description="Improve voice search readiness by adding more conversational language and question-based content.",
                impact_score=0.8,
                implementation_effort="Easy",
                code_example="""
<!-- Add conversational FAQ sections -->
<div class="voice-optimized-faq">
    <h3>What is the best way to...?</h3>
    <p>The best way to achieve this is by following these simple steps...</p>
    
    <h3>How can I quickly improve...?</h3>
    <p>You can quickly improve this by...</p>
</div>
                """,
                expected_improvement="15-30% increase in voice search visibility",
                category="Voice Search"
            ))
        
        # FAQ enhancement recommendations
        faq_data = basic_analysis.get('faq_analysis', {})
        if faq_data.get('qa_pairs_count', 0) < 5:
            recommendations.append(DynamicRecommendation(
                title="Add More FAQ Content for AEO Dominance",
                description="Increase your FAQ content to capture more answer engine queries. Target questions your audience actually asks.",
                impact_score=0.9,
                implementation_effort="Easy",
                code_example="""
<section class="expanded-faq">
    <h2>Frequently Asked Questions</h2>
    
    <div class="faq-item">
        <h3>What are the benefits of...?</h3>
        <p>The key benefits include: [detailed answer in 20-150 words]</p>
    </div>
    
    <div class="faq-item">
        <h3>How long does it take to...?</h3>
        <p>Typically, you can expect... [specific timeframe and factors]</p>
    </div>
</section>
                """,
                expected_improvement="25-40% increase in question-based search visibility",
                category="FAQ Enhancement"
            ))
        
        return sorted(recommendations, key=lambda x: x.impact_score, reverse=True)[:6]
    
    def _analyze_competitive_positioning(self, text: str, insights: List[SemanticInsight],
                                       depth_analysis: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyze competitive advantages and content gaps"""
        advantages = []
        gaps = []
        
        # Identify advantages
        comprehensive_topics = [i for i in insights if i.content_depth == 'Comprehensive']
        if comprehensive_topics:
            topic_names = [t.topic for t in comprehensive_topics]
            advantages.append(f"Comprehensive coverage of: {', '.join(topic_names)}")
        
        if depth_analysis['comprehensiveness'] > 70:
            advantages.append("High content comprehensiveness and detail level")
        
        # Identify gaps
        basic_topics = [i for i in insights if i.content_depth == 'Basic']
        if basic_topics:
            topic_names = [t.topic for t in basic_topics]
            gaps.append(f"Shallow coverage of: {', '.join(topic_names)}")
        
        if len(insights) < 3:
            gaps.append("Limited topic diversity - expand to more relevant topics")
        
        if depth_analysis['comprehensiveness'] < 50:
            gaps.append("Content lacks depth and comprehensive coverage")
        
        return advantages[:5], gaps[:5]
    
    def _calculate_content_intelligence_score(self, entities: List[EntityMatch],
                                            insights: List[SemanticInsight],
                                            topic_authority: float,
                                            depth_analysis: Dict[str, Any],
                                            voice_optimization: Dict[str, Any],
                                            basic_analysis: Dict[str, Any]) -> float:
        """Calculate overall content intelligence score"""
        score = 0.0
        
        # Entity recognition score (15% weight)
        high_quality_entities = [e for e in entities if e.confidence > 0.8 and e.relevance_score > 0.6]
        entity_score = min(len(high_quality_entities) * 5, 15)
        score += entity_score
        
        # Semantic insights score (20% weight)
        high_confidence_insights = [i for i in insights if i.confidence > 0.6]
        semantic_score = min(len(high_confidence_insights) * 3, 20)
        score += semantic_score
        
        # Topic authority score (25% weight)
        authority_score = (topic_authority / 100) * 25
        score += authority_score
        
        # Content depth score (20% weight)
        depth_score = (depth_analysis['comprehensiveness'] / 100) * 20
        score += depth_score
        
        # Voice search optimization score (20% weight)
        voice_score = (voice_optimization['voice_readiness_score'] / 100) * 20
        score += voice_score
        
        return min(score, 100)
    
    def _get_default_advanced_result(self) -> AdvancedContentResult:
        """Return default result when analysis fails"""
        return AdvancedContentResult(
            content_intelligence_score=0.0,
            semantic_insights=[],
            entities_detected=[],
            topic_authority_score=0.0,
            content_depth_analysis={
                'depth_indicators': {},
                'structure_score': 0,
                'comprehensiveness': 0,
                'detail_level': 'Basic'
            },
            voice_search_optimization={
                'question_optimization': 0,
                'conversational_score': 0,
                'local_intent_score': 0,
                'long_tail_optimization': 0,
                'voice_readiness_score': 0,
                'improvement_areas': ["Unable to analyze content"]
            },
            dynamic_recommendations=[],
            competitive_advantages=[],
            content_gaps=["Content analysis failed"]
        )