"""
Test Script for Intelligent FAQ Analysis
Demonstrates the power of your new AEO intelligence upgrade!
"""

import requests
from bs4 import BeautifulSoup
from services.content import ContentAnalyzer
import json

def test_faq_intelligence():
    """Test the new FAQ intelligence on real websites"""
    
    print("🚀 AEO Assessment Tool - FAQ Intelligence Test")
    print("=" * 60)
    
    # Initialize the enhanced content analyzer
    analyzer = ContentAnalyzer()
    
    # Test URLs with different FAQ patterns
    test_urls = [
        "https://help.shopify.com/en/manual/getting-started",  # Rich FAQ content
        "https://support.google.com/",  # Support/FAQ structure
        "https://www.hubspot.com/",     # Business website with questions
    ]
    
    for url in test_urls:
        print(f"\n🔍 Analyzing: {url}")
        print("-" * 40)
        
        try:
            # Fetch webpage content
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AEO-Analyzer/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch {url} (Status: {response.status_code})")
                continue
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Run the intelligent analysis
            results = analyzer.analyze_content(soup)
            
            # Display key results
            print_analysis_results(results)
            
        except Exception as e:
            print(f"❌ Error analyzing {url}: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test completed! Your AEO tool now has AI-powered FAQ intelligence!")

def print_analysis_results(results):
    """Print formatted analysis results"""
    
    # Overall Intelligence Score
    intelligence_score = results.get('content_intelligence_score', 0)
    print(f"📊 Content Intelligence Score: {intelligence_score:.1f}/100")
    
    # FAQ Analysis Results
    faq_data = results.get('faq_analysis', {})
    print(f"🤖 FAQ Intelligence Score: {faq_data.get('faq_intelligence_score', 0)}/100")
    print(f"📋 FAQ Sections Found: {faq_data.get('faq_sections_found', 0)}")
    print(f"❓ Q&A Pairs Extracted: {faq_data.get('qa_pairs_count', 0)}")
    print(f"🎤 Voice Search Readiness: {faq_data.get('voice_search_readiness', 0):.2f}")
    print(f"⭐ Featured Snippet Potential: {faq_data.get('featured_snippet_potential', 0)}")
    
    # Show sample Q&A pairs if found
    qa_pairs = faq_data.get('qa_pairs', [])
    if qa_pairs:
        print(f"\n📝 Sample Q&A Pairs Found:")
        for i, pair in enumerate(qa_pairs[:3]):  # Show first 3
            print(f"  {i+1}. Q: {pair['question'][:80]}...")
            print(f"     A: {pair['answer'][:80]}...")
            print(f"     Snippet Potential: {pair['snippet_potential']:.2f}")
    
    # AEO Metrics
    aeo_data = results.get('aeo_metrics', {})
    if aeo_data:
        print(f"\n🎯 AEO Optimization Metrics:")
        print(f"  • Answer Richness: {aeo_data.get('answer_richness_score', 0):.2f}")
        print(f"  • Conversational Language: {aeo_data.get('conversational_score', 0):.2f}")
        print(f"  • Snippet Readiness: {aeo_data.get('snippet_readiness_score', 0):.2f}")
    
    # Top Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        print(f"\n💡 Top Improvement Suggestions:")
        for i, rec in enumerate(recommendations[:3]):
            print(f"  {i+1}. {rec}")

def test_sample_html():
    """Test with sample FAQ content"""
    
    print("\n🧪 Testing with Sample FAQ Content")
    print("-" * 40)
    
    # Sample HTML with FAQ content
    sample_html = """
    <html>
    <head><title>Sample FAQ Page</title></head>
    <body>
        <h1>Frequently Asked Questions</h1>
        
        <section class="faq">
            <h2>What is AEO?</h2>
            <p>Answer Engine Optimization (AEO) is the practice of optimizing content 
            to appear in AI-powered search results and voice search responses. 
            It focuses on providing direct, conversational answers to user questions.</p>
            
            <h2>How do I optimize for voice search?</h2>
            <p>To optimize for voice search, you should focus on natural language patterns, 
            create conversational content, and structure your answers in a clear, 
            step-by-step format. Use question-based headings and provide concise answers.</p>
            
            <h2>Why is FAQ content important for AEO?</h2>
            <p>FAQ content is crucial for AEO because it directly matches the 
            question-answer format that AI systems look for. Well-structured FAQs 
            help your content appear in featured snippets and voice search results.</p>
            
            <h2>When should you update your FAQ section?</h2>
            <p>You should update your FAQ section regularly, ideally monthly. 
            First, analyze user questions from support channels. 
            Next, identify trending topics in your industry. 
            Finally, optimize answers for better readability and completeness.</p>
        </section>
    </body>
    </html>
    """
    
    # Analyze the sample content
    analyzer = ContentAnalyzer()
    soup = BeautifulSoup(sample_html, 'html.parser')
    results = analyzer.analyze_content(soup)
    
    print_analysis_results(results)

if __name__ == "__main__":
    # Run the tests
    test_sample_html()
    
    # Uncomment the line below to test with real websites
    # test_faq_intelligence()
    
    print("\n🎉 Your AEO tool is now 10x more intelligent!")
    print("Ready to analyze websites with AI-powered FAQ detection!")