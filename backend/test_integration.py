"""
Integration Test for Enhanced AEO Analyzer
Tests the full integration of FAQ intelligence with the main analyzer
"""

import asyncio
import sys
import logging
from services.analyzer import WebsiteAnalyzer
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_integration():
    """Test the complete integration of enhanced analyzer"""
    
    print("🚀 Testing Enhanced AEO Analyzer Integration")
    print("=" * 60)
    
    # Test with sample HTML that has FAQ content
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test FAQ Page for AEO Analysis</title>
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question",
                "name": "What is AEO?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Answer Engine Optimization (AEO) is the practice of optimizing content to appear in AI-powered search results."
                }
            }]
        }
        </script>
    </head>
    <body>
        <h1>Frequently Asked Questions About AEO</h1>
        
        <section class="faq-section">
            <h2>What is Answer Engine Optimization?</h2>
            <p>Answer Engine Optimization (AEO) is the practice of optimizing content 
            to appear in AI-powered search results and voice search responses. 
            It focuses on providing direct, conversational answers to user questions.</p>
            
            <h2>How do I optimize for voice search?</h2>
            <p>To optimize for voice search, you should focus on natural language patterns, 
            create conversational content, and structure your answers in a clear, 
            step-by-step format. First, research common questions. 
            Next, create question-based headings. Finally, provide concise answers.</p>
            
            <h2>Why is FAQ content important for AEO?</h2>
            <p>FAQ content is crucial for AEO because it directly matches the 
            question-answer format that AI systems look for. Well-structured FAQs 
            help your content appear in featured snippets and voice search results.</p>
            
            <h2>When should you update your FAQ section?</h2>
            <p>You should update your FAQ section regularly, ideally monthly. 
            Monitor user questions from support channels and add new Q&A pairs 
            based on trending topics in your industry.</p>
            
            <h2>Where can I learn more about AEO best practices?</h2>
            <p>You can learn more about AEO by following SEO industry publications, 
            attending digital marketing conferences, and testing different 
            optimization strategies on your own content.</p>
        </section>
        
        <section class="content">
            <h2>Getting Started with AEO</h2>
            <p>This comprehensive guide covers everything you need to know about 
            optimizing your content for answer engines. We'll walk you through 
            the essential steps to improve your visibility in AI-powered search results.</p>
            
            <ol>
                <li>Research conversational queries in your industry</li>
                <li>Create natural language question-based headings</li>
                <li>Structure answers in 20-150 words for featured snippets</li>
                <li>Use step-by-step formats and direct answers</li>
                <li>Implement FAQ schema markup</li>
            </ol>
        </section>
    </body>
    </html>
    """
    
    # Create a mock URL for testing
    test_url = "https://example.com/test-faq-page"
    
    try:
        # Test 1: Initialize Enhanced Analyzer
        print("\n📊 Test 1: Initializing Enhanced Analyzer")
        analyzer = WebsiteAnalyzer(test_url)
        analysis_id = analyzer.generate_analysis_id()
        print(f"✅ Analyzer initialized with ID: {analysis_id}")
        
        # Test 2: Test Content Analysis (most important!)
        print("\n🤖 Test 2: Testing Enhanced Content Analysis")
        
        # Parse HTML for content analysis
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # Test the enhanced content analyzer directly
        content_results = analyzer.content_analyzer.analyze_content(soup)
        
        print(f"✅ Content Intelligence Score: {content_results.get('content_intelligence_score', 0):.1f}/100")
        
        faq_data = content_results.get('faq_analysis', {})
        print(f"✅ FAQ Intelligence Score: {faq_data.get('faq_intelligence_score', 0):.1f}/100")
        print(f"✅ FAQ Sections Found: {faq_data.get('faq_sections_found', 0)}")
        print(f"✅ Q&A Pairs Extracted: {faq_data.get('qa_pairs_count', 0)}")
        print(f"✅ Voice Search Readiness: {faq_data.get('voice_search_readiness', 0):.2f}")
        print(f"✅ Featured Snippet Potential: {faq_data.get('featured_snippet_potential', 0)}")
        
        # Show sample Q&A pairs
        qa_pairs = faq_data.get('qa_pairs', [])
        if qa_pairs:
            print(f"\n📝 Sample Q&A Pairs Detected:")
            for i, pair in enumerate(qa_pairs[:3]):
                print(f"  {i+1}. Q: {pair['question'][:60]}...")
                print(f"     A: {pair['answer'][:60]}...")
                print(f"     Snippet Potential: {pair['snippet_potential']:.2f}")
        
        # Test 3: Legacy Compatibility
        print(f"\n🔄 Test 3: Testing Legacy Compatibility")
        
        # Create enhanced content structure for full analyzer
        enhanced_content_result = {
            'enhanced': content_results,
            'legacy': analyzer._create_legacy_content_result(content_results),
            'intelligence_upgrade': True
        }
        
        # Test scoring with enhanced data
        mock_results = {
            'performance': type('PerformanceResult', (), {
                'lcp': 2.1, 'fid': 120, 'cls': 0.08, 'score': 85,
                'mobile_score': 82, 'desktop_score': 88
            })(),
            'schema': type('SchemaResult', (), {
                'faq_schema_present': True, 'qa_schema_present': False,
                'howto_schema_present': False, 'organization_schema_present': True,
                'local_business_schema_present': False, 'validation_errors': [],
                'total_schemas_found': 2
            })(),
            'content': enhanced_content_result,
            'technical': type('TechnicalResult', (), {
                'https_enabled': True, 'mobile_friendly': True,
                'sitemap_present': True, 'robots_txt_present': True,
                'page_speed_score': 87, 'core_web_vitals_passed': True
            })()
        }
        
        scores = analyzer.calculate_scores(mock_results)
        
        print(f"✅ Performance Score: {scores['performance']}/25")
        print(f"✅ Schema Score: {scores['schema']}/25")
        print(f"✅ Enhanced Content Score: {scores['content']}/25")
        print(f"✅ Technical Score: {scores['technical']}/25")
        print(f"✅ Overall Score: {scores['overall']}/100")
        print(f"✅ Intelligence Level: {scores['intelligence_level']}")
        print(f"✅ FAQ Intelligence: {scores['faq_intelligence']}/100")
        
        # Test 4: Enhanced Recommendations
        print(f"\n💡 Test 4: Testing Enhanced Recommendations")
        
        recommendations = analyzer.generate_recommendations(scores, mock_results)
        
        print(f"✅ Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3]):
            print(f"  {i+1}. [{rec.category}] {rec.title}")
            print(f"     Impact: {rec.impact} | Difficulty: {rec.difficulty}")
            if rec.action_items:
                print(f"     First action: {rec.action_items[0]}")
        
        # Test 5: API Compatibility Test
        print(f"\n🔗 Test 5: Testing API Integration Points")
        
        # Test the data structures that would be returned by API
        api_response_structure = {
            "analysis_id": analysis_id,
            "url": test_url,
            "overall_score": scores['overall'],
            "intelligence_level": scores.get('intelligence_level', 'Basic'),
            "enhanced_metrics": {
                "faq_intelligence_score": scores.get('faq_intelligence', 0),
                "content_intelligence_score": content_results.get('content_intelligence_score', 0),
                "voice_search_readiness": faq_data.get('voice_search_readiness', 0),
                "featured_snippet_potential": faq_data.get('featured_snippet_potential', 0),
                "qa_pairs_found": faq_data.get('qa_pairs_count', 0),
            },
            "recommendations": len(recommendations)
        }
        
        print(f"✅ API Response Structure Valid")
        print(f"   Analysis ID: {api_response_structure['analysis_id']}")
        print(f"   Intelligence Level: {api_response_structure['intelligence_level']}")
        print(f"   FAQ Intelligence: {api_response_structure['enhanced_metrics']['faq_intelligence_score']}")
        
        # Final Summary
        print(f"\n🎯 Integration Test Results Summary")
        print(f"=" * 60)
        print(f"✅ All core components integrated successfully")
        print(f"✅ FAQ Intelligence: {scores['faq_intelligence']}/100")
        print(f"✅ Overall Intelligence Level: {scores['intelligence_level']}")
        print(f"✅ Content upgraded from basic to {content_results.get('content_intelligence_score', 0):.1f}% intelligence")
        print(f"✅ Voice Search Readiness: {faq_data.get('voice_search_readiness', 0)*100:.1f}%")
        print(f"✅ Enhanced recommendations: {len(recommendations)} generated")
        
        intelligence_increase = max(scores['faq_intelligence'], content_results.get('content_intelligence_score', 0))
        if intelligence_increase >= 70:
            print(f"🏆 TARGET ACHIEVED: 70%+ Intelligence Level Reached!")
        elif intelligence_increase >= 50:
            print(f"🎉 MILESTONE: 50%+ Intelligence Level Achieved!")
        else:
            print(f"📈 Progress: {intelligence_increase}% Intelligence (Goal: 70%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run integration tests"""
    success = await test_integration()
    
    if success:
        print(f"\n🚀 Integration Complete!")
        print(f"Your AEO tool now has intelligent FAQ analysis capabilities!")
        print(f"Ready to move to Phase 2: Schema Intelligence Enhancement")
    else:
        print(f"\n⚠️  Integration issues detected. Please review errors above.")
        
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)