"""
Schema markup analysis and validation
"""

import aiohttp
import json
import re
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from models.analysis import SchemaResult


logger = logging.getLogger(__name__)


class SchemaAnalyzer:
    """Schema markup analysis and validation"""
    
    def __init__(self):
        """Initialize schema analyzer"""
        self.session = None
    
    async def analyze(self, url: str) -> SchemaResult:
        """
        Analyze schema markup on the website
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Schema analysis results
        """
        logger.info(f"Starting schema analysis for {url}")
        
        try:
            # Fetch page content
            html_content = await self._fetch_page_content(url)
            if not html_content:
                return self._get_default_schema_result()
            
            # Extract schemas
            jsonld_schemas = self._extract_jsonld_schemas(html_content)
            microdata_schemas = self._extract_microdata_schemas(html_content)
            
            # Analyze schema types
            schema_analysis = self._analyze_schema_types(jsonld_schemas + microdata_schemas)
            
            # Validate schemas
            validation_errors = self._validate_schemas(jsonld_schemas)
            
            result = SchemaResult(
                faq_schema_present=schema_analysis['faq_present'],
                qa_schema_present=schema_analysis['qa_present'],
                howto_schema_present=schema_analysis['howto_present'],
                organization_schema_present=schema_analysis['organization_present'],
                local_business_schema_present=schema_analysis['local_business_present'],
                validation_errors=validation_errors,
                total_schemas_found=len(jsonld_schemas) + len(microdata_schemas)
            )
            
            logger.info(f"Schema analysis completed for {url}")
            return result
            
        except Exception as e:
            logger.error(f"Schema analysis failed for {url}: {e}")
            return self._get_default_schema_result()
    
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
    
    def _extract_jsonld_schemas(self, html_content: str) -> List[Dict[Any, Any]]:
        """
        Extract JSON-LD schemas from HTML
        
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
        Extract microdata schemas from HTML
        
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
        Analyze schema types to identify AEO-relevant markup
        
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
        Extract schema type from schema object
        
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
        Validate schema markup for common issues
        
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
    
    async def get_schema_recommendations(self, result: SchemaResult) -> List[str]:
        """
        Get schema markup recommendations
        
        Args:
            result: Schema analysis result
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if not result.faq_schema_present:
            recommendations.append("Add FAQ schema markup to your Q&A content")
        
        if not result.qa_schema_present:
            recommendations.append("Implement QAPage schema for individual question pages")
        
        if not result.howto_schema_present:
            recommendations.append("Add HowTo schema to step-by-step guides")
        
        if not result.organization_schema_present:
            recommendations.append("Add Organization schema to improve brand recognition")
        
        if result.validation_errors:
            recommendations.append("Fix schema validation errors to ensure proper indexing")
        
        return recommendations 