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

# Load environment variables
load_dotenv()

app = FastAPI(title="AEO Lite Assessment")

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
    return {"message": "AEO Lite Assessment - Ready for Analysis!"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv("GOOGLE_PAGESPEED_API_KEY"))
    }

@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv("GOOGLE_PAGESPEED_API_KEY"))
    }

async def get_pagespeed_score(url: str):
    """Get real Google PageSpeed data"""
    api_key = os.getenv("GOOGLE_PAGESPEED_API_KEY")
    if not api_key:
        print(f"ERROR: Google PageSpeed API key not configured")
        return 0
    
    try:
        pagespeed_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": url,
            "key": api_key,
            "strategy": "mobile"
        }
        
        print(f"Making PageSpeed API call for {url}...")
        async with aiohttp.ClientSession() as session:
            async with session.get(pagespeed_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    score = data["lighthouseResult"]["categories"]["performance"]["score"]
                    print(f"PageSpeed API success: {int(score * 100)}")
                    return int(score * 100)
                else:
                    error_text = await response.text()
                    print(f"ERROR: PageSpeed API returned {response.status}: {error_text}")
                    return 0
    except Exception as e:
        print(f"ERROR: PageSpeed API exception: {str(e)}")
        return 0

async def analyze_website_simple(url: str):
    """Simple website analysis"""
    try:
        # Get performance score
        performance_score = await get_pagespeed_score(url)
        
        # Get basic page content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Basic scoring
                    schema_score = 15 if soup.find('script', type='application/ld+json') else 0
                    content_score = 10 if len(soup.find_all(['h1', 'h2', 'h3'])) >= 3 else 5
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
                        "recommendations": [
                            "Improve page speed" if performance_score < 50 else "Good performance",
                            "Add structured data" if schema_score == 0 else "Schema markup detected",
                            "Optimize for answer engines"
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

async def run_background_analysis(url: str, task_id: str):
    """Run analysis in background with real progress tracking"""
    try:
        # Initialize analysis
        analysis_results[task_id] = {
            "status": "in_progress", 
            "progress": 0,
            "current_step": "Starting analysis..."
        }
        
        # Step 1: Performance Analysis (25%)
        analysis_results[task_id].update({
            "progress": 10,
            "current_step": "Analyzing performance with Google PageSpeed..."
        })
        performance_score = await get_pagespeed_score(url)
        
        analysis_results[task_id].update({
            "progress": 25,
            "current_step": "Performance analysis complete"
        })
        
        # Step 2: Fetch website content (50%)
        analysis_results[task_id].update({
            "progress": 30,
            "current_step": "Fetching website content..."
        })
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                else:
                    raise Exception(f"Website returned status {response.status}")
        
        analysis_results[task_id].update({
            "progress": 50,
            "current_step": "Analyzing schema markup..."
        })
        
        # Step 3: Schema Analysis (75%)
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        microdata = soup.find_all(attrs={"itemscope": True})
        schema_score = 0
        if json_ld_scripts:
            schema_score += 15
        if microdata:
            schema_score += 10
        schema_score = min(schema_score, 25)
        
        analysis_results[task_id].update({
            "progress": 75,
            "current_step": "Analyzing content structure..."
        })
        
        # Step 4: Content Analysis (90%)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        content_score = 10 if len(headings) >= 3 else 5
        
        analysis_results[task_id].update({
            "progress": 90,
            "current_step": "Checking technical SEO..."
        })
        
        # Step 5: Technical Analysis (100%)
        from urllib.parse import urlparse
        technical_score = 10 if urlparse(url).scheme == 'https' else 0
        
        # Calculate total score
        total_score = performance_score + schema_score + content_score + technical_score
        
        # Final results
        results = {
            "url": url,
            "overall_score": total_score,
            "category_scores": {
                "performance": performance_score,
                "schema": schema_score,
                "content": content_score,
                "technical": technical_score
            },
            "analysis_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": [
                "Improve page speed" if performance_score < 50 else "Good performance",
                "Add structured data" if schema_score == 0 else "Schema markup detected",
                "Optimize for answer engines"
            ]
        }
        
        analysis_results[task_id] = {
            "status": "completed",
            "progress": 100,
            "current_step": "Analysis complete!",
            "results": results
        }
    except Exception as e:
        analysis_results[task_id] = {
            "status": "failed",
            "progress": 100,
            "error": str(e)
        }

@app.post("/api/analyze")
async def start_analysis(background_tasks: BackgroundTasks, data: dict):
    """Start website analysis"""
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    task_id = str(uuid.uuid4())
    background_tasks.add_task(run_background_analysis, url, task_id)
    
    return {"analysis_id": task_id, "status": "started"}

@app.get("/api/analysis/{task_id}")
async def get_analysis(task_id: str):
    """Get analysis results"""
    if task_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_results[task_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 