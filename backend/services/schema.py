"""
Enhanced Schema markup analysis and validation with AEO Intelligence
"""

import aiohttp
import json
import re
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from models.analysis import SchemaResult
from .schema_intelligence import IntelligentSchemaAnalyzer, IntelligentSchemaResult


logger = logging.getLogger(__name__)


class SchemaAnalyzer:
    """Enhanced schema markup analysis with AEO intelligence"""
    
    def __init__(self):
        """Initialize enhanced schema analyzer"""
        self.session = None
        self.intelligent_analyzer = IntelligentSchemaAnalyzer()
    
    async def analyze(self, url: str) -> SchemaResult:
        """
        Analyze schema markup on the website (legacy compatible)
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Schema analysis results (backward compatible)
        """
        logger.info(f"Starting enhanced schema analysis for {url}")
        
        try:
            # Fetch page content
            html_content = await self._fetch_page_content(url)
            if not html_content:
                return self._get_default_schema_result()
            
            # Run enhanced analysis
            soup = BeautifulSoup(html_content, 'html.parser')
            enhanced_result = self.intelligent_analyzer.analyze_schema_intelligence(soup, url)
            
            # Convert to legacy format for backward compatibility
            legacy_result = self._convert_to_legacy_format(enhanced_result)
            
            logger.info(f"Enhanced schema analysis completed for {url}. Intelligence Score: {enhanced_result.schema_intelligence_score:.1f}/100")
            return legacy_result
            
        except Exception as e:
            logger.error(f"Enhanced schema analysis failed for {url}: {e}")
            return self._get_default_schema_result()
    
    async def analyze_with_intelligence(self, url: str) -> Dict[str, Any]:
        """
        Analyze schema markup with full intelligence capabilities
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Enhanced schema analysis results with intelligence
        """
        logger.info(f"Starting full intelligence schema analysis for {url}")
        
        try:
            # Fetch page content
            html_content = await self._fetch_page_content(url)
            if not html_content:
                return self._get_default_enhanced_result()
            
            # Run enhanced analysis
            soup = BeautifulSoup(html_content, 'html.parser')
            enhanced_result = self.intelligent_analyzer.analyze_schema_intelligence(soup, url)
            
            # Convert to legacy format for compatibility
            legacy_result = self._convert_to_legacy_format(enhanced_result)
            
            # Return both enhanced and legacy results
            result = {
                'enhanced': self._convert_enhanced_to_dict(enhanced_result),
                'legacy': self._convert_legacy_to_dict(legacy_result),
                'intelligence_upgrade': True,
                'schema_intelligence_score': enhanced_result.schema_intelligence_score,
                'aeo_readiness_score': enhanced_result.aeo_readiness_score
            }
            
            logger.info(f"Full intelligence schema analysis completed for {url}. Intelligence: {enhanced_result.schema_intelligence_score:.1f}/100, AEO Readiness: {enhanced_result.aeo_readiness_score:.1f}/100")
            return result
            
        except Exception as e:
            logger.error(f"Full intelligence schema analysis failed for {url}: {e}")
            return self._get_default_enhanced_result()
    
    def _convert_to_legacy_format(self, enhanced_result: IntelligentSchemaResult) -> SchemaResult:
        """
        Convert enhanced results to legacy SchemaResult format
        
        Args:
            enhanced_result: Enhanced analysis results
            
        Returns:
            Legacy SchemaResult object
        """
        # Analyze detected schemas for legacy boolean flags
        schema_types = {schema['schema_type'].lower() for schema in enhanced_result.schemas_detected}
        
        # Extract validation errors
        validation_errors = []
        for validation in enhanced_result.validation_results:
            validation_errors.extend(validation.errors)
        
        return SchemaResult(
            faq_schema_present=any('faq' in schema_type for schema_type in schema_types),
            qa_schema_present=any('qa' in schema_type or 'question' in schema_type for schema_type in schema_types),
            howto_schema_present=any('howto' in schema_type for schema_type in schema_types),
            organization_schema_present=any('organization' in schema_type for schema_type in schema_types),
            local_business_schema_present=any('localbusiness' in schema_type or 'local' in schema_type for schema_type in schema_types),
            validation_errors=validation_errors[:10],  # Limit for legacy compatibility
            total_schemas_found=len(enhanced_result.schemas_detected)
        )
    
    def _convert_enhanced_to_dict(self, enhanced_result: IntelligentSchemaResult) -> Dict[str, Any]:
        """Convert enhanced result to dictionary format"""
        return {
            'schemas_detected': enhanced_result.schemas_detected,
            'validation_results': [
                {
                    'schema_type': v.schema_type,
                    'is_valid': v.is_valid,
                    'completeness_score': v.completeness_score,
                    'aeo_optimization_score': v.aeo_optimization_score,
                    'errors': v.errors,
                    'warnings': v.warnings,
                    'suggestions': v.suggestions,
                    'content_match_score': v.content_match_score
                } for v in enhanced_result.validation_results
            ],
            'opportunities': [
                {
                    'schema_type': o.schema_type,
                    'confidence': o.confidence,
                    'content_patterns_found': o.content_patterns_found,
                    'implementation_difficulty': o.implementation_difficulty,
                    'aeo_impact': o.aeo_impact,
                    'code_example': o.code_example
                } for o in enhanced_result.opportunities
            ],
            'schema_intelligence_score': enhanced_result.schema_intelligence_score,
            'aeo_readiness_score': enhanced_result.aeo_readiness_score,
            'missing_critical_schemas': enhanced_result.missing_critical_schemas,
            'implementation_recommendations': enhanced_result.implementation_recommendations,
            'content_analysis': enhanced_result.content_analysis
        }
    
    def _convert_legacy_to_dict(self, legacy_result: SchemaResult) -> Dict[str, Any]:
        """Convert legacy result to dictionary format"""
        return {
            'faq_schema_present': legacy_result.faq_schema_present,
            'qa_schema_present': legacy_result.qa_schema_present,
            'howto_schema_present': legacy_result.howto_schema_present,
            'organization_schema_present': legacy_result.organization_schema_present,
            'local_business_schema_present': legacy_result.local_business_schema_present,
            'validation_errors': legacy_result.validation_errors,
            'total_schemas_found': legacy_result.total_schemas_found
        }
    
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
                'User-Agent': 'Mozilla/5.0 (compatible; AEO-Analyzer/2.0)',
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
    
    # Legacy methods (maintained for backward compatibility)
    def _extract_jsonld_schemas(self, html_content: str) -> List[Dict[Any, Any]]:
        """
        Extract JSON-LD schemas from HTML (legacy method)
        
        Args:
            html_content: HTML content
            
        Returns:
            List of JSON-LD schema objects
        """
        schemas = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all JSON-LD script tags
            jsonld_scripts = soup.find_all('script', type='application/ld+json')
            
            for script in jsonld_scripts:
                try:
                    schema_data = json.loads(script.string or '{}')
                    if schema_data:
                        # Handle both single objects and arrays
                        if isinstance(schema_data, list):
                            schemas.extend(schema_data)
                        else:
                            schemas.append(schema_data)
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON-LD found: {e}")
                    continue
            
            logger.debug(f"Found {len(schemas)} JSON-LD schemas")
            
        except Exception as e:
            logger.error(f"Error extracting JSON-LD schemas: {e}")
        
        return schemas
    
    def _extract_microdata_schemas(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Extract microdata schemas from HTML (legacy method)
        
        Args:
            html_content: HTML content
            
        Returns:
            List of microdata schema objects
        """
        schemas = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find elements with itemscope attribute
            itemscope_elements = soup.find_all(attrs={'itemscope': True})
            
            for element in itemscope_elements:
                schema = {}
                
                # Get itemtype
                itemtype = element.get('itemtype')
                if itemtype:
                    schema['@type'] = itemtype.split('/')[-1]  # Extract type name
                
                # Extract properties
                properties = {}
                for prop_element in element.find_all(attrs={'itemprop': True}):
                    prop_name = prop_element.get('itemprop')
                    prop_value = prop_element.get_text(strip=True)
                    if prop_name and prop_value:
                        properties[prop_name] = prop_value
                
                if properties:
                    schema.update(properties)
                
                if schema:
                    schemas.append(schema)
            
            logger.debug(f"Found {len(schemas)} microdata schemas")
            
        except Exception as e:
            logger.error(f"Error extracting microdata schemas: {e}")
        
        return schemas
    
    def _analyze_schema_types(self, schemas: List[Dict[Any, Any]]) -> Dict[str, bool]:
        """
        Analyze schema types to identify AEO-relevant markup (legacy method)
        
        Args:
            schemas: List of schema objects
            
        Returns:
            Dictionary indicating presence of different schema types
        """
        analysis = {
            'faq_present': False,
            'qa_present': False,
            'howto_present': False,
            'organization_present': False,
            'local_business_present': False
        }
        
        for schema in schemas:
            schema_type = self._get_schema_type(schema)
            
            if schema_type:
                type_lower = schema_type.lower()
                
                if 'faq' in type_lower or 'faqpage' in type_lower:
                    analysis['faq_present'] = True
                elif 'qa' in type_lower or 'question' in type_lower or 'qapage' in type_lower:
                    analysis['qa_present'] = True
                elif 'howto' in type_lower:
                    analysis['howto_present'] = True
                elif 'organization' in type_lower:
                    analysis['organization_present'] = True
                elif 'localbusiness' in type_lower or 'local' in type_lower:
                    analysis['local_business_present'] = True
        
        return analysis
    
    def _get_schema_type(self, schema: Dict[Any, Any]) -> Optional[str]:
        """
        Extract schema type from schema object (legacy method)
        
        Args:
            schema: Schema object
            
        Returns:
            Schema type string or None
        """
        # Check common type fields
        for type_field in ['@type', 'type', 'itemtype']:
            if type_field in schema:
                schema_type = schema[type_field]
                if isinstance(schema_type, str):
                    return schema_type
                elif isinstance(schema_type, list) and schema_type:
                    return schema_type[0]
        
        return None
    
    def _validate_schemas(self, schemas: List[Dict[Any, Any]]) -> List[str]:
        """
        Validate schema markup for common issues (legacy method)
        
        Args:
            schemas: List of schema objects
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        for i, schema in enumerate(schemas):
            schema_type = self._get_schema_type(schema)
            
            # Check for required @context in JSON-LD
            if '@context' not in schema:
                errors.append(f"Schema {i+1}: Missing @context property")
            
            # Check for @type
            if not schema_type:
                errors.append(f"Schema {i+1}: Missing @type property")
            
            # Validate FAQ schema structure
            if schema_type and 'faq' in schema_type.lower():
                if 'mainEntity' not in schema and 'mainContent' not in schema:
                    errors.append(f"FAQ Schema {i+1}: Missing mainEntity or mainContent")
            
            # Validate Question schema structure
            if schema_type and 'question' in schema_type.lower():
                if 'name' not in schema and 'text' not in schema:
                    errors.append(f"Question Schema {i+1}: Missing name or text property")
                if 'acceptedAnswer' not in schema:
                    errors.append(f"Question Schema {i+1}: Missing acceptedAnswer property")
        
        return errors[:10]  # Limit to first 10 errors
    
    def _get_default_schema_result(self) -> SchemaResult:
        """
        Return default schema result when analysis fails
        
        Returns:
            Default schema result
        """
        return SchemaResult(
            faq_schema_present=False,
            qa_schema_present=False,
            howto_schema_present=False,
            organization_schema_present=False,
            local_business_schema_present=False,
            validation_errors=[],
            total_schemas_found=0
        )
    
    def _get_default_enhanced_result(self) -> Dict[str, Any]:
        """
        Return default enhanced result when analysis fails
        
        Returns:
            Default enhanced analysis result
        """
        default_legacy = self._get_default_schema_result()
        
        return {
            'enhanced': {
                'schemas_detected': [],
                'validation_results': [],
                'opportunities': [],
                'schema_intelligence_score': 0.0,
                'aeo_readiness_score': 0.0,
                'missing_critical_schemas': ['FAQPage', 'HowTo', 'QAPage'],
                'implementation_recommendations': [
                    "Unable to analyze schemas - please check page accessibility",
                    "Consider implementing FAQ schema for AEO optimization"
                ],
                'content_analysis': {}
            },
            'legacy': self._convert_legacy_to_dict(default_legacy),
            'intelligence_upgrade': False,
            'schema_intelligence_score': 0.0,
            'aeo_readiness_score': 0.0
        }
    
    async def get_schema_recommendations(self, result: SchemaResult) -> List[str]:
        """
        Get schema markup recommendations (enhanced with intelligence)
        
        Args:
            result: Schema analysis result
            
        Returns:
            List of enhanced recommendations
        """
        recommendations = []
        
        # Enhanced recommendations based on AEO priorities
        if not result.faq_schema_present:
            recommendations.append("🔥 HIGH PRIORITY: Add FAQ schema markup to boost voice search visibility")
        
        if not result.qa_schema_present:
            recommendations.append("⭐ RECOMMENDED: Implement QAPage schema for individual question pages")
        
        if not result.howto_schema_present:
            recommendations.append("📋 VALUABLE: Add HowTo schema to step-by-step guides for featured snippets")
        
        if not result.organization_schema_present:
            recommendations.append("🏢 FOUNDATION: Add Organization schema to improve brand recognition")
        
        if result.validation_errors:
            recommendations.append("⚠️ CRITICAL: Fix schema validation errors to ensure proper AI understanding")
        
        # Add advanced recommendations
        if result.total_schemas_found == 0:
            recommendations.append("🚀 START HERE: Begin with FAQ schema - it has the highest AEO impact")
        elif result.total_schemas_found < 3:
            recommendations.append("📈 EXPAND: Add more schema types to increase content intelligence")
        
        return recommendations
    
    async def get_intelligent_recommendations(self, enhanced_result: Dict[str, Any]) -> List[str]:
        """
        Get intelligent schema recommendations based on enhanced analysis
        
        Args:
            enhanced_result: Enhanced analysis results
            
        Returns:
            List of intelligent recommendations
        """
        if not enhanced_result.get('intelligence_upgrade', False):
            # Fallback to basic recommendations
            legacy_result = SchemaResult(**enhanced_result.get('legacy', {}))
            return await self.get_schema_recommendations(legacy_result)
        
        enhanced_data = enhanced_result.get('enhanced', {})
        recommendations = enhanced_data.get('implementation_recommendations', [])
        
        # Add intelligence-based insights
        intelligence_score = enhanced_data.get('schema_intelligence_score', 0)
        aeo_score = enhanced_data.get('aeo_readiness_score', 0)
        
        insights = []
        
        if intelligence_score < 30:
            insights.append("🎯 FOCUS: Your schema intelligence is below 30% - prioritize critical AEO schemas")
        elif intelligence_score < 50:
            insights.append("📊 PROGRESS: Good start! Add more detailed properties to reach 50%+ intelligence")
        elif intelligence_score < 70:
            insights.append("⚡ ALMOST THERE: You're close to advanced intelligence - optimize existing schemas")
        else:
            insights.append("🏆 EXCELLENT: Advanced schema intelligence achieved! Focus on content alignment")
        
        if aeo_score < 50:
            insights.append("🎤 VOICE SEARCH: Low AEO readiness - implement FAQ and HowTo schemas")
        
        return insights + recommendations[:4]  # Combine insights with top recommendations 