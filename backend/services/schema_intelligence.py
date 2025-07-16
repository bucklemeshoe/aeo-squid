"""
Intelligent Schema Analysis Service for Advanced AEO
Detects, validates, and optimizes schema markup for answer engines
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Set
from bs4 import BeautifulSoup
from dataclasses import dataclass
import requests
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


@dataclass
class SchemaValidationResult:
    """Schema validation result with intelligence scoring"""
    schema_type: str
    is_valid: bool
    completeness_score: float
    aeo_optimization_score: float
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    content_match_score: float


@dataclass
class SchemaOpportunity:
    """Potential schema implementation opportunity"""
    schema_type: str
    confidence: float
    content_patterns_found: List[str]
    implementation_difficulty: str
    aeo_impact: str
    code_example: str


@dataclass
class IntelligentSchemaResult:
    """Comprehensive intelligent schema analysis results"""
    schemas_detected: List[Dict[str, Any]]
    validation_results: List[SchemaValidationResult]
    opportunities: List[SchemaOpportunity]
    schema_intelligence_score: float
    aeo_readiness_score: float
    missing_critical_schemas: List[str]
    implementation_recommendations: List[str]
    content_analysis: Dict[str, Any]


class IntelligentSchemaAnalyzer:
    """Advanced schema analysis with AEO intelligence"""
    
    def __init__(self):
        """Initialize the intelligent schema analyzer"""
        
        # Critical AEO schema types with intelligence weights
        self.aeo_critical_schemas = {
            'FAQPage': {
                'weight': 0.30,  # 30% of schema intelligence
                'aeo_impact': 'Critical',
                'voice_search_boost': True
            },
            'QAPage': {
                'weight': 0.25,
                'aeo_impact': 'High',
                'voice_search_boost': True
            },
            'HowTo': {
                'weight': 0.20,
                'aeo_impact': 'High',
                'voice_search_boost': True
            },
            'Article': {
                'weight': 0.10,
                'aeo_impact': 'Medium',
                'voice_search_boost': False
            },
            'Organization': {
                'weight': 0.05,
                'aeo_impact': 'Medium',
                'voice_search_boost': False
            },
            'WebPage': {
                'weight': 0.05,
                'aeo_impact': 'Low',
                'voice_search_boost': False
            },
            'LocalBusiness': {
                'weight': 0.05,
                'aeo_impact': 'Medium',
                'voice_search_boost': True
            }
        }
        
        # Content patterns that suggest schema opportunities
        self.content_patterns = {
            'FAQPage': [
                r'(?i)frequently\s+asked\s+questions?',
                r'(?i)common\s+questions?',
                r'(?i)f\.?a\.?q\.?s?',
                r'(?i)q\s*&\s*a',
                r'(?i)questions?\s+(?:and\s+)?answers?'
            ],
            'QAPage': [
                r'(?i)question:',
                r'(?i)answer:',
                r'(?i)q:\s*',
                r'(?i)a:\s*'
            ],
            'HowTo': [
                r'(?i)how\s+to\s+',
                r'(?i)step\s+\d+',
                r'(?i)instructions?',
                r'(?i)tutorial',
                r'(?i)\d+\.\s+',
                r'(?i)first.*second.*third',
                r'(?i)next.*then.*finally'
            ],
            'Article': [
                r'(?i)published',
                r'(?i)author',
                r'(?i)article',
                r'(?i)blog\s+post'
            ],
            'LocalBusiness': [
                r'(?i)address',
                r'(?i)phone',
                r'(?i)hours?',
                r'(?i)location',
                r'(?i)contact',
                r'(?i)directions'
            ]
        }
        
        # Required properties for complete schema implementation
        self.required_properties = {
            'FAQPage': {
                'critical': ['mainEntity'],
                'recommended': ['url', 'name', 'description'],
                'aeo_optimal': ['author', 'datePublished', 'dateModified']
            },
            'QAPage': {
                'critical': ['mainEntity'],
                'recommended': ['url', 'name'],
                'aeo_optimal': ['author', 'datePublished']
            },
            'HowTo': {
                'critical': ['name', 'step'],
                'recommended': ['description', 'totalTime'],
                'aeo_optimal': ['tool', 'supply', 'image']
            },
            'Article': {
                'critical': ['headline', 'author'],
                'recommended': ['datePublished', 'image'],
                'aeo_optimal': ['publisher', 'mainEntityOfPage']
            }
        }
    
    def analyze_schema_intelligence(self, soup: BeautifulSoup, url: str = "") -> IntelligentSchemaResult:
        """
        Comprehensive intelligent schema analysis for AEO
        
        Args:
            soup: BeautifulSoup object of webpage content
            url: Website URL for context
            
        Returns:
            IntelligentSchemaResult with comprehensive analysis
        """
        logger.info("Starting intelligent schema analysis")
        
        try:
            # 1. Detect existing schemas
            schemas_detected = self._detect_schemas(soup)
            
            # 2. Analyze content for schema opportunities
            content_analysis = self._analyze_content_for_schemas(soup)
            
            # 3. Validate existing schemas
            validation_results = self._validate_schemas(schemas_detected, soup)
            
            # 4. Identify schema opportunities
            opportunities = self._identify_schema_opportunities(content_analysis, schemas_detected)
            
            # 5. Calculate intelligence scores
            schema_intelligence_score = self._calculate_schema_intelligence_score(
                schemas_detected, validation_results, opportunities
            )
            
            aeo_readiness_score = self._calculate_aeo_readiness_score(
                schemas_detected, content_analysis, validation_results
            )
            
            # 6. Identify missing critical schemas
            missing_critical = self._identify_missing_critical_schemas(schemas_detected, content_analysis)
            
            # 7. Generate implementation recommendations
            recommendations = self._generate_implementation_recommendations(
                schemas_detected, opportunities, validation_results, content_analysis
            )
            
            result = IntelligentSchemaResult(
                schemas_detected=schemas_detected,
                validation_results=validation_results,
                opportunities=opportunities,
                schema_intelligence_score=schema_intelligence_score,
                aeo_readiness_score=aeo_readiness_score,
                missing_critical_schemas=missing_critical,
                implementation_recommendations=recommendations,
                content_analysis=content_analysis
            )
            
            logger.info(f"Schema intelligence analysis complete. Score: {schema_intelligence_score:.1f}/100")
            return result
            
        except Exception as e:
            logger.error(f"Schema intelligence analysis failed: {e}")
            return self._get_default_schema_result()
    
    def _detect_schemas(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Detect and parse existing schema markup"""
        schemas = []
        
        # JSON-LD schemas (most common and preferred)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                schema_data = json.loads(script.string)
                if isinstance(schema_data, dict):
                    schemas.append({
                        'type': 'json-ld',
                        'schema_type': schema_data.get('@type', 'Unknown'),
                        'data': schema_data,
                        'raw': script.string,
                        'location': 'head' if script.find_parent('head') else 'body'
                    })
                elif isinstance(schema_data, list):
                    for item in schema_data:
                        if isinstance(item, dict):
                            schemas.append({
                                'type': 'json-ld',
                                'schema_type': item.get('@type', 'Unknown'),
                                'data': item,
                                'raw': json.dumps(item),
                                'location': 'head' if script.find_parent('head') else 'body'
                            })
            except json.JSONDecodeError:
                logger.warning("Invalid JSON-LD schema found")
        
        # Microdata schemas
        itemscope_elements = soup.find_all(attrs={'itemscope': True})
        for element in itemscope_elements:
            itemtype = element.get('itemtype', '')
            if itemtype:
                schema_type = itemtype.split('/')[-1] if '/' in itemtype else itemtype
                schemas.append({
                    'type': 'microdata',
                    'schema_type': schema_type,
                    'data': self._extract_microdata_properties(element),
                    'element': str(element)[:200] + '...' if len(str(element)) > 200 else str(element),
                    'location': 'content'
                })
        
        # RDFa schemas
        rdfa_elements = soup.find_all(attrs={'typeof': True})
        for element in rdfa_elements:
            schema_type = element.get('typeof', '')
            schemas.append({
                'type': 'rdfa',
                'schema_type': schema_type,
                'data': self._extract_rdfa_properties(element),
                'element': str(element)[:200] + '...' if len(str(element)) > 200 else str(element),
                'location': 'content'
            })
        
        logger.info(f"Detected {len(schemas)} schemas: {[s['schema_type'] for s in schemas]}")
        return schemas
    
    def _extract_microdata_properties(self, element) -> Dict[str, Any]:
        """Extract properties from microdata element"""
        properties = {}
        
        # Find all property elements within this scope
        property_elements = element.find_all(attrs={'itemprop': True})
        for prop_elem in property_elements:
            prop_name = prop_elem.get('itemprop')
            
            # Get property value
            if prop_elem.get('content'):
                prop_value = prop_elem.get('content')
            elif prop_elem.get('href'):
                prop_value = prop_elem.get('href')
            elif prop_elem.get('src'):
                prop_value = prop_elem.get('src')
            else:
                prop_value = prop_elem.get_text().strip()
            
            properties[prop_name] = prop_value
        
        return properties
    
    def _extract_rdfa_properties(self, element) -> Dict[str, Any]:
        """Extract properties from RDFa element"""
        properties = {}
        
        # Extract basic RDFa properties
        for attr in ['property', 'rel', 'resource', 'content']:
            if element.get(attr):
                properties[attr] = element.get(attr)
        
        return properties
    
    def _analyze_content_for_schemas(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content to identify schema opportunities"""
        text_content = soup.get_text().lower()
        
        analysis = {
            'content_types_detected': [],
            'pattern_matches': {},
            'structural_elements': {},
            'question_answer_pairs': 0,
            'how_to_steps': 0,
            'faq_sections': 0,
            'article_indicators': 0
        }
        
        # Analyze for each schema type
        for schema_type, patterns in self.content_patterns.items():
            matches = []
            for pattern in patterns:
                pattern_matches = re.findall(pattern, text_content)
                matches.extend(pattern_matches)
            
            if matches:
                analysis['content_types_detected'].append(schema_type)
                analysis['pattern_matches'][schema_type] = len(matches)
        
        # Specific structural analysis
        analysis['structural_elements'] = {
            'headings': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            'lists': len(soup.find_all(['ul', 'ol', 'dl'])),
            'questions': len(re.findall(r'[^.!?]*\?', text_content)),
            'numbered_steps': len(re.findall(r'\d+\.\s+', text_content)),
            'definition_lists': len(soup.find_all('dl'))
        }
        
        # Count specific content patterns
        analysis['question_answer_pairs'] = len(re.findall(r'(?i)(question|q):\s*.*?(answer|a):\s*', text_content))
        analysis['how_to_steps'] = len(re.findall(r'(?i)(step\s+\d+|first.*second|next.*then)', text_content))
        analysis['faq_sections'] = len(re.findall(r'(?i)(faq|frequently\s+asked)', text_content))
        analysis['article_indicators'] = len(re.findall(r'(?i)(published|author|article)', text_content))
        
        return analysis
    
    def _validate_schemas(self, schemas: List[Dict[str, Any]], soup: BeautifulSoup) -> List[SchemaValidationResult]:
        """Validate existing schemas for completeness and AEO optimization"""
        validation_results = []
        
        for schema in schemas:
            if schema['type'] == 'json-ld':
                result = self._validate_json_ld_schema(schema, soup)
                validation_results.append(result)
            elif schema['type'] == 'microdata':
                result = self._validate_microdata_schema(schema, soup)
                validation_results.append(result)
        
        return validation_results
    
    def _validate_json_ld_schema(self, schema: Dict[str, Any], soup: BeautifulSoup) -> SchemaValidationResult:
        """Validate JSON-LD schema"""
        schema_type = schema['schema_type']
        schema_data = schema['data']
        
        errors = []
        warnings = []
        suggestions = []
        
        # Check for required properties
        required_props = self.required_properties.get(schema_type, {})
        critical_props = required_props.get('critical', [])
        recommended_props = required_props.get('recommended', [])
        aeo_optimal_props = required_props.get('aeo_optimal', [])
        
        # Validate critical properties
        missing_critical = [prop for prop in critical_props if prop not in schema_data]
        if missing_critical:
            errors.extend([f"Missing critical property: {prop}" for prop in missing_critical])
        
        # Check recommended properties
        missing_recommended = [prop for prop in recommended_props if prop not in schema_data]
        if missing_recommended:
            warnings.extend([f"Missing recommended property: {prop}" for prop in missing_recommended])
        
        # Check AEO optimal properties
        missing_aeo_optimal = [prop for prop in aeo_optimal_props if prop not in schema_data]
        if missing_aeo_optimal:
            suggestions.extend([f"Add AEO-optimal property: {prop}" for prop in missing_aeo_optimal])
        
        # Calculate scores
        total_props = len(critical_props) + len(recommended_props) + len(aeo_optimal_props)
        present_props = (len(critical_props) - len(missing_critical) + 
                        len(recommended_props) - len(missing_recommended) + 
                        len(aeo_optimal_props) - len(missing_aeo_optimal))
        
        completeness_score = (present_props / total_props) if total_props > 0 else 1.0
        
        # AEO optimization score based on schema type importance and completeness
        aeo_weight = self.aeo_critical_schemas.get(schema_type, {}).get('weight', 0.05)
        aeo_optimization_score = completeness_score * aeo_weight * 100
        
        # Content match score
        content_match_score = self._calculate_content_match_score(schema, soup)
        
        return SchemaValidationResult(
            schema_type=schema_type,
            is_valid=len(errors) == 0,
            completeness_score=completeness_score,
            aeo_optimization_score=aeo_optimization_score,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            content_match_score=content_match_score
        )
    
    def _validate_microdata_schema(self, schema: Dict[str, Any], soup: BeautifulSoup) -> SchemaValidationResult:
        """Validate microdata schema (simplified)"""
        schema_type = schema['schema_type']
        
        # Basic validation for microdata
        completeness_score = 0.7  # Microdata generally less complete than JSON-LD
        aeo_optimization_score = completeness_score * 0.05 * 100  # Lower weight for microdata
        
        suggestions = [
            "Consider migrating to JSON-LD format for better AEO optimization",
            "Add more detailed properties for better AI understanding"
        ]
        
        return SchemaValidationResult(
            schema_type=schema_type,
            is_valid=True,
            completeness_score=completeness_score,
            aeo_optimization_score=aeo_optimization_score,
            errors=[],
            warnings=["Microdata format detected - JSON-LD is preferred for AEO"],
            suggestions=suggestions,
            content_match_score=0.6  # Default for microdata
        )
    
    def _calculate_content_match_score(self, schema: Dict[str, Any], soup: BeautifulSoup) -> float:
        """Calculate how well schema matches actual content"""
        schema_type = schema['schema_type']
        schema_data = schema['data']
        content_text = soup.get_text().lower()
        
        score = 0.0
        
        # Check if schema content appears in actual page content
        if schema_type == 'FAQPage' and 'mainEntity' in schema_data:
            main_entities = schema_data['mainEntity']
            if isinstance(main_entities, list):
                for entity in main_entities:
                    if isinstance(entity, dict):
                        question = entity.get('name', '')
                        answer = entity.get('acceptedAnswer', {}).get('text', '')
                        if question.lower() in content_text and answer.lower() in content_text:
                            score += 0.2
            score = min(score, 1.0)
        
        elif schema_type == 'HowTo' and 'step' in schema_data:
            steps = schema_data['step']
            if isinstance(steps, list):
                for step in steps:
                    if isinstance(step, dict):
                        step_text = step.get('text', '')
                        if step_text.lower() in content_text:
                            score += 0.1
            score = min(score, 1.0)
        
        else:
            # Generic content matching
            if 'name' in schema_data:
                name_text = schema_data['name'].lower()
                if name_text in content_text:
                    score += 0.3
            
            if 'description' in schema_data:
                desc_text = schema_data['description'].lower()
                if desc_text in content_text:
                    score += 0.3
            
            score = min(score, 0.8)  # Cap generic matching
        
        return score
    
    def _identify_schema_opportunities(self, content_analysis: Dict[str, Any], 
                                     existing_schemas: List[Dict[str, Any]]) -> List[SchemaOpportunity]:
        """Identify potential schema implementation opportunities"""
        opportunities = []
        existing_types = {schema['schema_type'] for schema in existing_schemas}
        
        # Check each potential schema type
        for schema_type in self.aeo_critical_schemas.keys():
            if schema_type in existing_types:
                continue  # Already implemented
            
            confidence = self._calculate_implementation_confidence(schema_type, content_analysis)
            
            if confidence > 0.3:  # Minimum confidence threshold
                opportunity = SchemaOpportunity(
                    schema_type=schema_type,
                    confidence=confidence,
                    content_patterns_found=self._get_matching_patterns(schema_type, content_analysis),
                    implementation_difficulty=self._get_implementation_difficulty(schema_type, confidence),
                    aeo_impact=self.aeo_critical_schemas[schema_type]['aeo_impact'],
                    code_example=self._generate_code_example(schema_type, content_analysis)
                )
                opportunities.append(opportunity)
        
        # Sort by confidence and AEO impact
        opportunities.sort(key=lambda x: (x.confidence, x.aeo_impact == 'Critical'), reverse=True)
        return opportunities[:5]  # Top 5 opportunities
    
    def _calculate_implementation_confidence(self, schema_type: str, content_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for implementing a schema type"""
        confidence = 0.0
        
        # Pattern matching confidence
        pattern_matches = content_analysis.get('pattern_matches', {}).get(schema_type, 0)
        if pattern_matches > 0:
            confidence += min(pattern_matches * 0.1, 0.4)
        
        # Structural confidence
        structural = content_analysis.get('structural_elements', {})
        
        if schema_type == 'FAQPage':
            if structural.get('questions', 0) >= 3:
                confidence += 0.3
            if content_analysis.get('faq_sections', 0) > 0:
                confidence += 0.3
        
        elif schema_type == 'QAPage':
            if content_analysis.get('question_answer_pairs', 0) > 0:
                confidence += 0.4
            if structural.get('definition_lists', 0) > 0:
                confidence += 0.2
        
        elif schema_type == 'HowTo':
            if structural.get('numbered_steps', 0) >= 3:
                confidence += 0.4
            if content_analysis.get('how_to_steps', 0) > 0:
                confidence += 0.3
        
        elif schema_type == 'Article':
            if content_analysis.get('article_indicators', 0) > 0:
                confidence += 0.3
            if structural.get('headings', 0) >= 2:
                confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _get_matching_patterns(self, schema_type: str, content_analysis: Dict[str, Any]) -> List[str]:
        """Get content patterns that match the schema type"""
        patterns = []
        
        if schema_type in content_analysis.get('content_types_detected', []):
            patterns.append(f"{schema_type} content patterns detected")
        
        structural = content_analysis.get('structural_elements', {})
        
        if schema_type == 'FAQPage':
            if structural.get('questions', 0) > 0:
                patterns.append(f"{structural['questions']} questions found")
            if content_analysis.get('faq_sections', 0) > 0:
                patterns.append("FAQ sections detected")
        
        elif schema_type == 'HowTo':
            if structural.get('numbered_steps', 0) > 0:
                patterns.append(f"{structural['numbered_steps']} numbered steps found")
            if content_analysis.get('how_to_steps', 0) > 0:
                patterns.append("How-to instruction patterns detected")
        
        return patterns
    
    def _get_implementation_difficulty(self, schema_type: str, confidence: float) -> str:
        """Determine implementation difficulty"""
        if confidence >= 0.7:
            return "Easy"
        elif confidence >= 0.5:
            return "Medium"
        else:
            return "Hard"
    
    def _generate_code_example(self, schema_type: str, content_analysis: Dict[str, Any]) -> str:
        """Generate basic code example for schema implementation"""
        
        examples = {
            'FAQPage': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Your question here?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Your answer here."
    }
  }]
}
</script>''',
            
            'QAPage': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "QAPage",
  "mainEntity": {
    "@type": "Question",
    "name": "Your question here?",
    "answerCount": 1,
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Your answer here."
    }
  }
}
</script>''',
            
            'HowTo': '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to do something",
  "description": "Step-by-step guide",
  "step": [{
    "@type": "HowToStep",
    "name": "Step 1",
    "text": "Do this first."
  }]
}
</script>'''
        }
        
        return examples.get(schema_type, "Schema code example not available")
    
    def _calculate_schema_intelligence_score(self, schemas: List[Dict[str, Any]], 
                                           validation_results: List[SchemaValidationResult],
                                           opportunities: List[SchemaOpportunity]) -> float:
        """Calculate overall schema intelligence score (0-100)"""
        score = 0.0
        
        # Existing schemas score (60% weight)
        if validation_results:
            avg_aeo_score = sum(r.aeo_optimization_score for r in validation_results) / len(validation_results)
            score += avg_aeo_score * 0.6
        
        # Schema diversity score (20% weight)
        unique_types = {schema['schema_type'] for schema in schemas}
        critical_types_present = sum(1 for schema_type in unique_types 
                                   if schema_type in self.aeo_critical_schemas)
        diversity_score = min(critical_types_present * 20, 100)
        score += diversity_score * 0.2
        
        # Implementation potential score (20% weight)
        if opportunities:
            avg_confidence = sum(op.confidence for op in opportunities) / len(opportunities)
            potential_score = avg_confidence * 100
            score += potential_score * 0.2
        
        return min(score, 100)
    
    def _calculate_aeo_readiness_score(self, schemas: List[Dict[str, Any]], 
                                     content_analysis: Dict[str, Any],
                                     validation_results: List[SchemaValidationResult]) -> float:
        """Calculate AEO readiness score (0-100)"""
        score = 0.0
        
        # Critical AEO schemas present
        present_critical = 0
        for schema in schemas:
            if schema['schema_type'] in ['FAQPage', 'QAPage', 'HowTo']:
                present_critical += 1
        
        score += min(present_critical * 30, 90)  # Up to 90 points for critical schemas
        
        # Content-schema alignment
        if validation_results:
            avg_content_match = sum(r.content_match_score for r in validation_results) / len(validation_results)
            score += avg_content_match * 10  # Up to 10 points for content alignment
        
        return min(score, 100)
    
    def _identify_missing_critical_schemas(self, schemas: List[Dict[str, Any]], 
                                         content_analysis: Dict[str, Any]) -> List[str]:
        """Identify missing critical schemas based on content analysis"""
        existing_types = {schema['schema_type'] for schema in schemas}
        missing = []
        
        # Check for FAQ content without FAQPage schema
        if ('FAQPage' not in existing_types and 
            (content_analysis.get('faq_sections', 0) > 0 or 
             content_analysis.get('structural_elements', {}).get('questions', 0) >= 3)):
            missing.append('FAQPage')
        
        # Check for How-To content without HowTo schema
        if ('HowTo' not in existing_types and 
            (content_analysis.get('how_to_steps', 0) > 0 or 
             content_analysis.get('structural_elements', {}).get('numbered_steps', 0) >= 3)):
            missing.append('HowTo')
        
        # Check for Q&A content without QAPage schema
        if ('QAPage' not in existing_types and 
            content_analysis.get('question_answer_pairs', 0) > 0):
            missing.append('QAPage')
        
        return missing
    
    def _generate_implementation_recommendations(self, schemas: List[Dict[str, Any]], 
                                               opportunities: List[SchemaOpportunity],
                                               validation_results: List[SchemaValidationResult],
                                               content_analysis: Dict[str, Any]) -> List[str]:
        """Generate specific implementation recommendations"""
        recommendations = []
        
        # Validation-based recommendations
        for result in validation_results:
            if result.errors:
                recommendations.append(f"Fix {result.schema_type} schema errors: {', '.join(result.errors[:2])}")
            
            if result.completeness_score < 0.7:
                recommendations.append(f"Enhance {result.schema_type} schema completeness by adding missing properties")
            
            if result.content_match_score < 0.5:
                recommendations.append(f"Improve {result.schema_type} schema content alignment with actual page content")
        
        # Opportunity-based recommendations
        for opportunity in opportunities[:3]:  # Top 3 opportunities
            if opportunity.confidence > 0.6:
                recommendations.append(
                    f"Implement {opportunity.schema_type} schema ({opportunity.implementation_difficulty} difficulty, "
                    f"{opportunity.aeo_impact} AEO impact)"
                )
        
        # Strategic recommendations
        critical_present = sum(1 for schema in schemas if schema['schema_type'] in ['FAQPage', 'QAPage', 'HowTo'])
        if critical_present == 0:
            recommendations.append("Prioritize implementing FAQ or How-To schema for maximum AEO impact")
        
        if not any(r.is_valid for r in validation_results):
            recommendations.append("Fix existing schema validation errors to improve search engine understanding")
        
        return recommendations[:6]  # Top 6 recommendations
    
    def _get_default_schema_result(self) -> IntelligentSchemaResult:
        """Return default result when analysis fails"""
        return IntelligentSchemaResult(
            schemas_detected=[],
            validation_results=[],
            opportunities=[],
            schema_intelligence_score=0.0,
            aeo_readiness_score=0.0,
            missing_critical_schemas=['FAQPage', 'HowTo', 'QAPage'],
            implementation_recommendations=[
                "Unable to analyze schemas - please check page accessibility",
                "Consider implementing FAQ schema for AEO optimization"
            ],
            content_analysis={}
        )