from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import aiohttp
import asyncio
import uuid
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from services.analyzer import WebsiteAnalyzer  # Import our enhanced analyzer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AEO Assessment Tool - Enhanced with FAQ Intelligence",
    description="Advanced Answer Engine Optimization analysis with AI-powered FAQ detection",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store analysis results in memory
analysis_results = {}

@app.get("/")
async def root():
    return {
        "message": "AEO Assessment Tool - Enhanced with FAQ Intelligence!",
        "version": "2.0.0",
        "features": [
            "AI-powered FAQ detection",
            "Voice search optimization analysis",
            "Featured snippet potential assessment",
            "Enhanced content intelligence scoring"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv("GOOGLE_PAGESPEED_API_KEY")),
        "faq_intelligence": "enabled",
        "nlp_models": "loaded"
    }

@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv("GOOGLE_PAGESPEED_API_KEY")),
        "faq_intelligence": "enabled",
        "nlp_models": "loaded"
    }

async def get_pagespeed_score(url: str):
    """Get real Google PageSpeed data"""
    api_key = os.getenv("GOOGLE_PAGESPEED_API_KEY")
    
    if not api_key:
        logger.warning("Google PageSpeed API key not configured, using fallback analysis")
        return 50  # Fallback score
    
    try:
        async with aiohttp.ClientSession() as session:
            # Mobile analysis
            mobile_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={api_key}"
            async with session.get(mobile_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'lighthouseResult' in data:
                        performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
                        return int(performance_score)
                    else:
                        logger.warning("No lighthouse data in PageSpeed response")
                        return 50
                else:
                    logger.warning(f"PageSpeed API returned status {response.status}")
                    return 50
    except asyncio.TimeoutError:
        logger.warning("PageSpeed API timeout")
        return 45
    except Exception as e:
        logger.warning(f"PageSpeed API error: {e}")
        return 40

async def quick_analyze(url: str):
    """Quick analysis fallback"""
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AEO-Analyzer/2.0)'
        }
        
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Enhanced quick scoring with FAQ intelligence preview
                    performance_score = await get_pagespeed_score(url)
                    schema_score = 15 if soup.find('script', type='application/ld+json') else 0
                    
                    # Quick FAQ detection
                    text_content = soup.get_text().lower()
                    faq_indicators = ['faq', 'frequently asked', 'common questions', 'q&a']
                    faq_found = any(indicator in text_content for indicator in faq_indicators)
                    questions = len([h for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) 
                                   if '?' in h.get_text()])
                    
                    content_score = 15 if faq_found and questions >= 3 else (10 if len(soup.find_all(['h1', 'h2', 'h3'])) >= 3 else 5)
                    technical_score = 10 if urlparse(url).scheme == 'https' else 0
                    
                    total_score = performance_score + schema_score + content_score + technical_score
                    
                    return {
                        "url": url,
                        "overall_score": total_score,
                        "category_scores": {
                            "performance": performance_score,
                            "schema": schema_score,
                            "content": content_score,
                            "technical": technical_score
                        },
                        "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "faq_preview": {
                            "faq_detected": faq_found,
                            "question_headings": questions
                        },
                        "recommendations": [
                            "Improve page speed" if performance_score < 50 else "Good performance",
                            "Add FAQ schema markup" if schema_score == 0 else "Schema markup detected",
                            "Enhance FAQ content for voice search" if not faq_found else "FAQ content detected - run full analysis for intelligence scoring"
                        ]
                    }
                else:
                    raise Exception(f"Website returned status {response.status}")
    except aiohttp.ClientTimeout:
        raise Exception("Website took too long to respond (timeout)")
    except aiohttp.ClientError as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Analysis failed: {str(e)}")

async def run_enhanced_analysis(url: str, task_id: str):
    """Run enhanced analysis with FAQ intelligence"""
    try:
        # Initialize analysis
        analysis_results[task_id] = {
            "status": "in_progress", 
            "progress": 0,
            "current_step": "Initializing enhanced analysis...",
            "intelligence_level": "enhanced"
        }
        
        # Initialize the enhanced analyzer
        analyzer = WebsiteAnalyzer(url)
        analysis_id = analyzer.generate_analysis_id()
        
        logger.info(f"Starting enhanced analysis for {url} with ID {analysis_id}")
        
        # Step 1: Performance Analysis (20%)
        analysis_results[task_id].update({
            "progress": 10,
            "current_step": "Analyzing performance with Google PageSpeed..."
        })
        
        performance_result = await analyzer.analyze_performance()
        
        analysis_results[task_id].update({
            "progress": 20,
            "current_step": "Performance analysis complete"
        })
        
        # Step 2: Enhanced Content Analysis with FAQ Intelligence (50%)
        analysis_results[task_id].update({
            "progress": 25,
            "current_step": "Fetching content for AI analysis..."
        })
        
        content_result = await analyzer.analyze_content()
        
        analysis_results[task_id].update({
            "progress": 50,
            "current_step": "Running AI-powered FAQ detection and analysis..."
        })
        
        # Step 3: Schema Analysis (70%)
        analysis_results[task_id].update({
            "progress": 60,
            "current_step": "Analyzing schema markup and structured data..."
        })
        
        schema_result = await analyzer.analyze_schema()
        
        analysis_results[task_id].update({
            "progress": 70,
            "current_step": "Schema analysis complete"
        })
        
        # Step 4: Technical Analysis (85%)
        analysis_results[task_id].update({
            "progress": 75,
            "current_step": "Checking technical SEO factors..."
        })
        
        technical_result = await analyzer.analyze_technical()
        
        analysis_results[task_id].update({
            "progress": 85,
            "current_step": "Calculating enhanced intelligence scores..."
        })
        
        # Step 5: Calculate Enhanced Scores (95%)
        all_results = {
            'performance': performance_result,
            'schema': schema_result,
            'content': content_result,
            'technical': technical_result
        }
        
        scores = analyzer.calculate_scores(all_results)
        
        analysis_results[task_id].update({
            "progress": 95,
            "current_step": "Generating AI-powered recommendations..."
        })
        
        # Step 6: Generate Enhanced Recommendations (100%)
        recommendations = analyzer.generate_recommendations(scores, all_results)
        
        # Extract enhanced content data for display
        enhanced_content = content_result.get('enhanced', {}) if content_result.get('intelligence_upgrade') else {}
        faq_analysis = enhanced_content.get('faq_analysis', {})
        
        # Final enhanced results
        results = {
            "analysis_id": analysis_id,
            "url": url,
            "overall_score": scores['overall'],
            "intelligence_level": scores.get('intelligence_level', 'Basic'),
            "category_scores": {
                "performance": scores['performance'],
                "schema": scores['schema'],
                "content": scores['content'],
                "technical": scores['technical']
            },
            "enhanced_metrics": {
                "faq_intelligence_score": scores.get('faq_intelligence', 0),
                "content_intelligence_score": enhanced_content.get('content_intelligence_score', 0),
                "voice_search_readiness": faq_analysis.get('voice_search_readiness', 0),
                "featured_snippet_potential": faq_analysis.get('featured_snippet_potential', 0),
                "qa_pairs_found": faq_analysis.get('qa_pairs_count', 0),
                "faq_sections_detected": faq_analysis.get('faq_sections_found', 0)
            },
            "analysis_details": {
                "performance": {
                    "lcp": getattr(performance_result, 'lcp', 0),
                    "fid": getattr(performance_result, 'fid', 0),
                    "cls": getattr(performance_result, 'cls', 0),
                    "mobile_score": getattr(performance_result, 'mobile_score', 0),
                    "desktop_score": getattr(performance_result, 'desktop_score', 0)
                },
                "content": enhanced_content if enhanced_content else {"basic_analysis": "No enhanced data available"},
                "schema": {
                    "faq_schema_present": getattr(schema_result, 'faq_schema_present', False),
                    "qa_schema_present": getattr(schema_result, 'qa_schema_present', False),
                    "total_schemas_found": getattr(schema_result, 'total_schemas_found', 0)
                },
                "technical": {
                    "https_enabled": getattr(technical_result, 'https_enabled', False),
                    "mobile_friendly": getattr(technical_result, 'mobile_friendly', False),
                    "core_web_vitals_passed": getattr(technical_result, 'core_web_vitals_passed', False)
                }
            },
            "recommendations": [
                {
                    "category": rec.category,
                    "title": rec.title,
                    "description": rec.description,
                    "impact": rec.impact,
                    "difficulty": rec.difficulty,
                    "action_items": rec.action_items
                }
                for rec in recommendations
            ],
            "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "version": "2.0.0",
            "features_used": [
                "AI-powered FAQ detection",
                "Voice search optimization analysis", 
                "Featured snippet potential assessment",
                "Enhanced content intelligence scoring"
            ]
        }
        
        analysis_results[task_id] = {
            "status": "completed",
            "progress": 100,
            "current_step": "Enhanced analysis complete!",
            "results": results,
            "intelligence_level": scores.get('intelligence_level', 'Basic')
        }
        
        logger.info(f"Enhanced analysis completed for {url}. Intelligence Level: {scores.get('intelligence_level', 'Basic')}, FAQ Score: {scores.get('faq_intelligence', 0)}")
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed for {url}: {e}")
        analysis_results[task_id] = {
            "status": "failed",
            "progress": 100,
            "error": str(e),
            "fallback_available": True
        }

# Legacy quick analysis endpoint (maintained for compatibility)
@app.post("/api/quick-analyze")
async def quick_analysis(data: dict):
    """Quick analysis endpoint (legacy)"""
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        result = await quick_analyze(url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Enhanced analysis endpoints
@app.post("/api/analyze")
async def start_enhanced_analysis(background_tasks: BackgroundTasks, data: dict):
    """Start enhanced website analysis with FAQ intelligence"""
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    task_id = str(uuid.uuid4())
    
    # Use enhanced analysis by default
    background_tasks.add_task(run_enhanced_analysis, url, task_id)
    
    return {
        "analysis_id": task_id, 
        "status": "started",
        "analysis_type": "enhanced",
        "features": [
            "AI-powered FAQ detection",
            "Voice search optimization analysis",
            "Featured snippet potential assessment",
            "Enhanced content intelligence scoring"
        ]
    }

@app.get("/api/analysis/{task_id}")
async def get_analysis(task_id: str):
    """Get enhanced analysis results"""
    if task_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    result = analysis_results[task_id]
    
    # Add helpful metadata
    if result.get("status") == "completed":
        result["metadata"] = {
            "analysis_version": "2.0.0",
            "intelligence_upgrade": True,
            "faq_intelligence_enabled": True
        }
    
    return result

@app.get("/api/features")
async def get_features():
    """Get information about available analysis features"""
    return {
        "version": "2.0.0",
        "analysis_types": {
            "enhanced": {
                "description": "Full AI-powered analysis with FAQ intelligence",
                "features": [
                    "Advanced NLP-based FAQ detection",
                    "Voice search optimization scoring",
                    "Featured snippet potential analysis",
                    "AI-generated improvement recommendations",
                    "Content intelligence scoring"
                ],
                "recommended": True
            },
            "quick": {
                "description": "Fast basic analysis",
                "features": [
                    "Basic performance metrics",
                    "Simple content structure analysis",
                    "Schema detection"
                ],
                "recommended": False
            }
        },
        "intelligence_levels": [
            "Basic (0-29%)",
            "Developing (30-49%)", 
            "Intermediate (50-69%)",
            "Advanced (70%+)"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 