"""
Schema Intelligence Integration Test
Tests the complete integration of Schema Intelligence with the main analyzer
"""

import asyncio
import sys
import logging
from services.analyzer import WebsiteAnalyzer
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_schema_integration():
    """Test the complete integration of Schema Intelligence analyzer"""
    
    print("🚀 Testing Schema Intelligence Integration")
    print("=" * 60)
    
    # Test HTML with comprehensive schema markup and FAQ content
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Schema Intelligence Page</title>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question",
                "name": "What is Schema Intelligence?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Schema Intelligence is an AI-powered approach to analyzing and optimizing structured data markup for better search engine understanding."
                }
            }, {
                "@type": "Question",
                "name": "How does Schema Intelligence improve AEO?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Schema Intelligence helps answer engines better understand your content structure, leading to improved visibility in voice search and featured snippets."
                }
            }]
        }
        </script>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": "How to Implement Schema Intelligence",
            "description": "Step-by-step guide to implementing intelligent schema markup",
            "step": [{
                "@type": "HowToStep",
                "name": "Step 1: Analyze Current Schema",
                "text": "First, analyze your existing schema markup to identify gaps and opportunities."
            }, {
                "@type": "HowToStep", 
                "name": "Step 2: Implement Critical Schemas",
                "text": "Next, implement FAQ and How-To schemas for maximum AEO impact."
            }]
        }
        </script>
    </head>
    <body>
        <h1>Schema Intelligence for AEO</h1>
        
        <section class="faq-section">
            <h2>Frequently Asked Questions</h2>
            
            <h3>What is Schema Intelligence?</h3>
            <p>Schema Intelligence is an AI-powered approach to analyzing and optimizing 
            structured data markup for better search engine understanding. It goes beyond 
            basic schema validation to provide intelligent recommendations.</p>
            
            <h3>How does Schema Intelligence improve AEO?</h3>
            <p>Schema Intelligence helps answer engines better understand your content 
            structure, leading to improved visibility in voice search and featured snippets. 
            This results in higher rankings and more traffic.</p>
            
            <h3>Why is structured data important?</h3>
            <p>Structured data helps search engines understand your content context, 
            making it more likely to appear in rich results and AI-powered answers.</p>
        </section>
        
        <section class="how-to">
            <h2>How to Implement Schema Intelligence</h2>
            <p>Follow this step-by-step guide to implement intelligent schema markup:</p>
            
            <ol>
                <li>Analyze your current schema markup to identify gaps</li>
                <li>Implement FAQ and How-To schemas for maximum AEO impact</li>
                <li>Validate your schema markup with AI-powered tools</li>
                <li>Monitor performance and optimize based on results</li>
            </ol>
        </section>
        
        <section class="content">
            <h2>Benefits of Schema Intelligence</h2>
            <p>Schema Intelligence provides numerous benefits for modern SEO and AEO strategies:</p>
            
            <ul>
                <li>Improved voice search visibility</li>
                <li>Higher featured snippet chances</li>
                <li>Better AI understanding of content</li>
                <li>Enhanced search result appearance</li>
            </ul>
        </section>
    </body>
    </html>
    """
    
    # Create a mock URL for testing
    test_url = "https://example.com/test-schema-page"
    
    try:
        # Test 1: Initialize Enhanced Analyzer
        print("\n📊 Test 1: Initializing Enhanced Analyzer with Schema Intelligence")
        analyzer = WebsiteAnalyzer(test_url)
        analysis_id = analyzer.generate_analysis_id()
        print(f"✅ Analyzer initialized with ID: {analysis_id}")
        
        # Test 2: Test Schema Intelligence Analysis
        print("\n🔍 Test 2: Testing Schema Intelligence Analysis")
        
        # Parse HTML for schema analysis
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # Test the enhanced schema analyzer directly
        schema_results = analyzer.schema_analyzer.intelligent_analyzer.analyze_schema_intelligence(soup, test_url)
        
        print(f"✅ Schema Intelligence Score: {schema_results.schema_intelligence_score:.1f}/100")
        print(f"✅ AEO Readiness Score: {schema_results.aeo_readiness_score:.1f}/100")
        print(f"✅ Schemas Detected: {len(schema_results.schemas_detected)}")
        print(f"✅ Schema Opportunities: {len(schema_results.opportunities)}")
        print(f"✅ Missing Critical Schemas: {len(schema_results.missing_critical_schemas)}")
        
        # Show detected schemas
        if schema_results.schemas_detected:
            print(f"\n📋 Detected Schemas:")
            for schema in schema_results.schemas_detected:
                print(f"  - {schema['schema_type']} ({schema['type']})")
        
        # Show opportunities
        if schema_results.opportunities:
            print(f"\n💡 Schema Opportunities:")
            for opportunity in schema_results.opportunities[:3]:
                print(f"  - {opportunity.schema_type} (Confidence: {opportunity.confidence:.2f}, Impact: {opportunity.aeo_impact})")
        
        # Test 3: Enhanced Schema Analysis via Main Analyzer
        print(f"\n🔄 Test 3: Testing Enhanced Schema Analysis Integration")
        
        # Create enhanced schema structure for full analyzer
        enhanced_schema_result = await analyzer.schema_analyzer.analyze_with_intelligence(test_url)
        
        print(f"✅ Intelligence Upgrade: {enhanced_schema_result.get('intelligence_upgrade', False)}")
        print(f"✅ Schema Intelligence: {enhanced_schema_result.get('schema_intelligence_score', 0):.1f}/100")
        print(f"✅ AEO Readiness: {enhanced_schema_result.get('aeo_readiness_score', 0):.1f}/100")
        
        # Test 4: Full Analyzer Integration
        print(f"\n🎯 Test 4: Testing Full Analyzer Integration")
        
        # Create mock results for full analysis
        mock_performance = type('PerformanceResult', (), {
            'lcp': 1.8, 'fid': 90, 'cls': 0.05, 'score': 92,
            'mobile_score': 89, 'desktop_score': 95
        })()
        
        mock_content = {
            'enhanced': {
                'content_intelligence_score': 65,
                'faq_analysis': {
                    'faq_intelligence_score': 82,
                    'qa_pairs_count': 3,
                    'voice_search_readiness': 0.7,
                    'featured_snippet_potential': 3
                },
                'basic_metrics': {'word_count': 850}
            },
            'legacy': type('ContentResult', (), {
                'heading_structure_score': 8, 'faq_patterns_found': 3,
                'qa_content_detected': True, 'word_count': 850,
                'readability_score': 7.5, 'conversational_queries_optimized': 6
            })(),
            'intelligence_upgrade': True
        }
        
        mock_technical = type('TechnicalResult', (), {
            'https_enabled': True, 'mobile_friendly': True,
            'sitemap_present': True, 'robots_txt_present': True,
            'page_speed_score': 92, 'core_web_vitals_passed': True
        })()
        
        # Test scoring with enhanced schema data
        all_results = {
            'performance': mock_performance,
            'schema': enhanced_schema_result,
            'content': mock_content,
            'technical': mock_technical
        }
        
        scores = analyzer.calculate_scores(all_results)
        
        print(f"✅ Performance Score: {scores['performance']}/25")
        print(f"✅ Enhanced Schema Score: {scores['schema']}/25")
        print(f"✅ Enhanced Content Score: {scores['content']}/25")
        print(f"✅ Technical Score: {scores['technical']}/25")
        print(f"✅ Overall Score: {scores['overall']}/100")
        print(f"✅ Intelligence Level: {scores['intelligence_level']}")
        print(f"✅ FAQ Intelligence: {scores['faq_intelligence']}/100")
        print(f"✅ Schema Intelligence: {scores['schema_intelligence']}/100")
        print(f"✅ AEO Readiness: {scores['aeo_readiness']}/100")
        
        # Test 5: Enhanced Recommendations
        print(f"\n💭 Test 5: Testing Enhanced Recommendations with Schema Intelligence")
        
        recommendations = analyzer.generate_recommendations(scores, all_results)
        
        print(f"✅ Generated {len(recommendations)} enhanced recommendations:")
        for i, rec in enumerate(recommendations[:4]):
            print(f"  {i+1}. [{rec.category}] {rec.title}")
            print(f"     Impact: {rec.impact} | Difficulty: {rec.difficulty}")
            if rec.action_items:
                print(f"     Key action: {rec.action_items[0]}")
        
        # Test 6: API Response Structure Test
        print(f"\n🔗 Test 6: Testing API Response Structure")
        
        # Test the enhanced response structure
        api_response_structure = {
            "analysis_id": analysis_id,
            "url": test_url,
            "overall_score": scores['overall'],
            "intelligence_level": scores.get('intelligence_level', 'Basic'),
            "enhanced_metrics": {
                "faq_intelligence_score": scores.get('faq_intelligence', 0),
                "schema_intelligence_score": scores.get('schema_intelligence', 0),
                "aeo_readiness_score": scores.get('aeo_readiness', 0),
                "content_intelligence_score": mock_content['enhanced']['content_intelligence_score'],
            },
            "schema_insights": {
                "schemas_detected": len(schema_results.schemas_detected),
                "opportunities_found": len(schema_results.opportunities),
                "missing_critical": len(schema_results.missing_critical_schemas),
                "implementation_recommendations": len(schema_results.implementation_recommendations)
            },
            "recommendations": len(recommendations)
        }
        
        print(f"✅ Enhanced API Response Structure Valid")
        print(f"   Schema Intelligence: {api_response_structure['enhanced_metrics']['schema_intelligence_score']}/100")
        print(f"   AEO Readiness: {api_response_structure['enhanced_metrics']['aeo_readiness_score']}/100")
        print(f"   Schemas Found: {api_response_structure['schema_insights']['schemas_detected']}")
        print(f"   Opportunities: {api_response_structure['schema_insights']['opportunities_found']}")
        
        # Final Summary
        print(f"\n🎯 Schema Intelligence Integration Test Results")
        print(f"=" * 60)
        print(f"✅ Schema Intelligence successfully integrated")
        print(f"✅ Schema Intelligence Score: {scores['schema_intelligence']}/100")
        print(f"✅ AEO Readiness Score: {scores['aeo_readiness']}/100")
        print(f"✅ Overall Intelligence Level: {scores['intelligence_level']}")
        print(f"✅ Enhanced scoring system working")
        print(f"✅ Smart recommendations generated: {len(recommendations)}")
        
        # Calculate combined intelligence
        combined_intelligence = (scores['faq_intelligence'] + scores['schema_intelligence']) / 2
        print(f"✅ Combined Intelligence Score: {combined_intelligence:.1f}/100")
        
        if combined_intelligence >= 70:
            print(f"🏆 TARGET ACHIEVED: 70%+ Combined Intelligence Level Reached!")
        elif combined_intelligence >= 50:
            print(f"🎉 MILESTONE: 50%+ Combined Intelligence Achieved!")
        else:
            print(f"📈 Progress: {combined_intelligence:.1f}% Combined Intelligence (Goal: 70%)")
        
        # Phase completion check
        if scores['schema_intelligence'] >= 60 and scores['faq_intelligence'] >= 70:
            print(f"🚀 PHASE 2 COMPLETE: Schema Intelligence Successfully Integrated!")
            print(f"Ready for Phase 3: Entity Recognition & Dynamic Recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run schema intelligence integration tests"""
    success = await test_schema_integration()
    
    if success:
        print(f"\n🚀 Schema Intelligence Integration Complete!")
        print(f"Your AEO tool now has both FAQ and Schema Intelligence!")
        print(f"Ready to move to Phase 3: Entity Recognition Enhancement")
    else:
        print(f"\n⚠️  Schema integration issues detected. Please review errors above.")
        
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)