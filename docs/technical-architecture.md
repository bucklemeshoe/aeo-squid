# AEO Quick Assessment Tool - Technical Architecture

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │  External APIs  │
│                 │    │                 │    │                 │
│  React/HTML     │◄──►│  Flask/FastAPI  │◄──►│  PageSpeed API  │
│  Dashboard      │    │  Analysis       │    │  Rich Results   │
│  Export Tools   │    │  Engine         │    │  Custom Checks  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Static Files  │    │   File Storage  │    │   Rate Limiting │
│   CSS/JS        │    │   Reports/Cache │    │   & Monitoring  │
│   Images        │    │   Templates     │    │   (Redis)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

**Frontend**
- **Framework**: Vanilla HTML/CSS/JavaScript (for speed and simplicity)
- **UI Library**: Bootstrap 5 (responsive, professional styling)
- **Charts**: Chart.js (for score visualizations)
- **PDF Generation**: jsPDF (client-side PDF creation)

**Backend**
- **Framework**: FastAPI (Python - fast, modern, well-documented)
- **Web Server**: Uvicorn (ASGI server)
- **Task Queue**: Celery with Redis (for background analysis)
- **Caching**: Redis (API response caching, rate limiting)

**External Services**
- **Performance**: Google PageSpeed Insights API
- **Schema Testing**: Google Rich Results Test API
- **Analytics**: Google Analytics 4
- **Monitoring**: Uptime Robot + custom health checks

**Deployment**
- **Hosting**: DigitalOcean Droplet or AWS EC2
- **Reverse Proxy**: Nginx
- **SSL**: Let's Encrypt (Certbot)
- **Domain**: Custom domain with professional branding

---

## Detailed Component Design

### 1. Frontend Application

**File Structure:**
```
frontend/
├── index.html              # Landing page
├── analysis.html           # Loading/progress page
├── results.html            # Dashboard template
├── assets/
│   ├── css/
│   │   ├── main.css       # Custom styles
│   │   └── dashboard.css  # Results styling
│   ├── js/
│   │   ├── main.js        # Core functionality
│   │   ├── analysis.js    # Analysis handling
│   │   └── dashboard.js   # Results display
│   └── images/
│       ├── logo.png
│       └── icons/
└── templates/
    └── report.html        # PDF export template
```

**Key Components:**

1. **URL Input Form**
   ```html
   <form id="analysis-form">
     <input type="url" placeholder="Enter website URL" required>
     <input type="email" placeholder="Email for results" required>
     <button type="submit">Analyze Website</button>
   </form>
   ```

2. **Progress Tracker**
   ```javascript
   const analysisSteps = [
     "Fetching website content",
     "Checking performance metrics", 
     "Analyzing schema markup",
     "Testing mobile optimization",
     "Generating recommendations"
   ];
   ```

3. **Results Dashboard**
   ```javascript
   const dashboard = {
     overallScore: 0-100,
     categories: {
       performance: { score: 0-25, details: [...] },
       schema: { score: 0-25, details: [...] },
       content: { score: 0-25, details: [...] },
       technical: { score: 0-25, details: [...] }
     }
   };
   ```

### 2. Backend API

**File Structure:**
```
backend/
├── main.py                 # FastAPI application entry
├── models/
│   ├── __init__.py
│   ├── analysis.py        # Data models
│   └── report.py          # Report structures
├── services/
│   ├── __init__.py
│   ├── analyzer.py        # Main analysis orchestrator
│   ├── performance.py     # PageSpeed integration
│   ├── schema.py          # Schema detection/validation
│   ├── content.py         # Content structure analysis
│   └── technical.py       # Technical SEO checks
├── utils/
│   ├── __init__.py
│   ├── validators.py      # URL/input validation
│   ├── cache.py           # Redis caching
│   └── rate_limiter.py    # Rate limiting logic
├── templates/
│   └── pdf_report.html    # PDF template
├── config.py              # Configuration management
└── requirements.txt       # Python dependencies
```

**API Endpoints:**

```python
# Main analysis endpoint
POST /api/analyze
{
  "url": "https://example.com",
  "email": "user@example.com",
  "callback_url": "optional"
}

# Get analysis results
GET /api/results/{analysis_id}

# Generate PDF report
GET /api/report/{analysis_id}/pdf

# Health check
GET /api/health

# Analytics data
GET /api/stats (admin only)
```

### 3. Analysis Engine

**Core Analysis Workflow:**

```python
class WebsiteAnalyzer:
    def __init__(self, url: str):
        self.url = url
        self.results = AnalysisResults()
    
    async def analyze(self) -> AnalysisResults:
        # 1. Validate and normalize URL
        validated_url = await self.validate_url()
        
        # 2. Run parallel analysis modules
        tasks = [
            self.analyze_performance(),
            self.analyze_schema(),
            self.analyze_content(),
            self.analyze_technical()
        ]
        results = await asyncio.gather(*tasks)
        
        # 3. Calculate scores and generate recommendations
        self.calculate_scores(results)
        self.generate_recommendations()
        
        return self.results
```

**Analysis Modules:**

1. **Performance Analysis** (`services/performance.py`)
   ```python
   async def analyze_performance(self, url: str) -> PerformanceResult:
       # PageSpeed Insights API integration
       api_response = await self.call_pagespeed_api(url)
       return PerformanceResult(
           lcp=api_response['lcp'],
           cls=api_response['cls'], 
           fid=api_response['fid'],
           score=api_response['score']
       )
   ```

2. **Schema Detection** (`services/schema.py`)
   ```python
   async def analyze_schema(self, url: str) -> SchemaResult:
       # Fetch page content
       content = await self.fetch_page_content(url)
       
       # Extract JSON-LD and microdata
       jsonld_schemas = self.extract_jsonld(content)
       microdata = self.extract_microdata(content)
       
       # Validate against schema.org
       validation_results = await self.validate_schemas(jsonld_schemas)
       
       return SchemaResult(
           faq_schema_present=self.has_faq_schema(jsonld_schemas),
           qa_schema_present=self.has_qa_schema(jsonld_schemas),
           validation_errors=validation_results
       )
   ```

3. **Content Analysis** (`services/content.py`)
   ```python
   async def analyze_content(self, url: str) -> ContentResult:
       content = await self.fetch_page_content(url)
       
       return ContentResult(
           heading_structure=self.analyze_headings(content),
           faq_patterns=self.detect_faq_patterns(content),
           qa_content=self.detect_qa_content(content),
           word_count=self.calculate_word_count(content)
       )
   ```

4. **Technical Analysis** (`services/technical.py`)
   ```python
   async def analyze_technical(self, url: str) -> TechnicalResult:
       return TechnicalResult(
           mobile_friendly=await self.check_mobile_friendly(url),
           https_enabled=self.check_https(url),
           sitemap_present=await self.check_sitemap(url),
           robots_txt=await self.check_robots_txt(url)
       )
   ```

---

## Data Models

### Analysis Results Structure

```python
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class AnalysisResults(BaseModel):
    analysis_id: str
    url: str
    timestamp: datetime
    overall_score: int  # 0-100
    
    # Category scores (0-25 each)
    performance_score: int
    schema_score: int
    content_score: int
    technical_score: int
    
    # Detailed results
    performance_details: PerformanceResult
    schema_details: SchemaResult
    content_details: ContentResult
    technical_details: TechnicalResult
    
    # Recommendations
    recommendations: List[Recommendation]
    priority_issues: List[Issue]

class Recommendation(BaseModel):
    category: str
    title: str
    description: str
    impact: str  # "High", "Medium", "Low"
    difficulty: str  # "Easy", "Medium", "Hard"
    action_items: List[str]

class Issue(BaseModel):
    category: str
    title: str
    description: str
    severity: str  # "Critical", "Important", "Minor"
    fix_guidance: str
```

---

## API Integration Specifications

### Google PageSpeed Insights API

**Endpoint:** `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`

**Integration:**
```python
import aiohttp
from typing import Dict

class PageSpeedAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    async def analyze_url(self, url: str) -> Dict:
        params = {
            'url': url,
            'key': self.api_key,
            'category': ['PERFORMANCE', 'SEO', 'BEST_PRACTICES'],
            'strategy': 'MOBILE'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise APIException(f"PageSpeed API error: {response.status}")
```

### Google Rich Results Test API

**Integration:**
```python
class RichResultsAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://searchconsole.googleapis.com/v1/urlTestingTools/richResults:run"
    
    async def test_url(self, url: str) -> Dict:
        payload = {
            'url': url,
            'inspectionUrl': url
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, json=payload, headers=headers) as response:
                return await response.json()
```

---

## Performance Optimization

### Caching Strategy

**Redis Cache Structure:**
```python
# Cache PageSpeed results for 24 hours
cache_key = f"pagespeed:{url_hash}"
ttl = 86400  # 24 hours

# Cache analysis results for 1 hour
analysis_cache_key = f"analysis:{url_hash}:{timestamp}"
analysis_ttl = 3600  # 1 hour

# Rate limiting
rate_limit_key = f"rate_limit:{ip_address}"
rate_limit_window = 3600  # 1 hour window
rate_limit_max = 10  # 10 requests per hour
```

**Implementation:**
```python
import redis
import json
from typing import Optional

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
    
    async def get_cached_result(self, cache_key: str) -> Optional[Dict]:
        cached = self.redis_client.get(cache_key)
        return json.loads(cached) if cached else None
    
    async def cache_result(self, cache_key: str, data: Dict, ttl: int):
        self.redis_client.setex(cache_key, ttl, json.dumps(data))
```

### Rate Limiting

```python
class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def check_rate_limit(self, identifier: str, limit: int = 10, window: int = 3600) -> bool:
        current_count = self.redis.incr(f"rate:{identifier}")
        if current_count == 1:
            self.redis.expire(f"rate:{identifier}", window)
        
        return current_count <= limit
```

---

## Security Considerations

### Input Validation

```python
from urllib.parse import urlparse
import re

class URLValidator:
    ALLOWED_SCHEMES = ['http', 'https']
    BLOCKED_DOMAINS = ['localhost', '127.0.0.1', '10.', '192.168.', '172.']
    
    @staticmethod
    def validate_url(url: str) -> bool:
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in URLValidator.ALLOWED_SCHEMES:
                return False
            
            # Check for blocked domains (prevent SSRF)
            for blocked in URLValidator.BLOCKED_DOMAINS:
                if blocked in parsed.netloc:
                    return False
            
            # Basic domain validation
            domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-_.]*[a-zA-Z0-9]$'
            if not re.match(domain_pattern, parsed.netloc):
                return False
            
            return True
            
        except Exception:
            return False
```

### API Security

```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

security = HTTPBearer()

async def verify_api_key(token: str = Depends(security)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

---

## Deployment Architecture

### Server Setup (DigitalOcean/AWS)

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Static files
    location /static/ {
        alias /var/www/aeo-tool/frontend/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Frontend
    location / {
        root /var/www/aeo-tool/frontend;
        try_files $uri $uri/ /index.html;
    }
}
```

**Docker Configuration:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=sqlite:///./test.db
    depends_on:
      - redis
    volumes:
      - ./reports:/app/reports

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./frontend:/var/www/aeo-tool/frontend
    depends_on:
      - web
```

---

## Monitoring & Analytics

### Application Monitoring

```python
import logging
from datetime import datetime
import json

class AnalyticsLogger:
    def __init__(self):
        self.logger = logging.getLogger('analytics')
    
    def log_analysis_start(self, url: str, user_ip: str):
        self.logger.info(json.dumps({
            'event': 'analysis_started',
            'url': url,
            'ip': user_ip,
            'timestamp': datetime.utcnow().isoformat()
        }))
    
    def log_analysis_complete(self, url: str, duration: float, score: int):
        self.logger.info(json.dumps({
            'event': 'analysis_completed',
            'url': url,
            'duration_seconds': duration,
            'overall_score': score,
            'timestamp': datetime.utcnow().isoformat()
        }))
```

### Health Checks

```python
from fastapi import FastAPI
import aiohttp
import redis

app = FastAPI()

@app.get("/api/health")
async def health_check():
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow(),
        'services': {}
    }
    
    # Check Redis
    try:
        redis_client.ping()
        health_status['services']['redis'] = 'healthy'
    except:
        health_status['services']['redis'] = 'unhealthy'
        health_status['status'] = 'degraded'
    
    # Check PageSpeed API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://google.com&key=YOUR_KEY') as response:
                if response.status == 200:
                    health_status['services']['pagespeed_api'] = 'healthy'
                else:
                    health_status['services']['pagespeed_api'] = 'unhealthy'
    except:
        health_status['services']['pagespeed_api'] = 'unreachable'
        health_status['status'] = 'degraded'
    
    return health_status
```

---

## Development Setup

### Local Development Environment

**Requirements:**
- Python 3.11+
- Node.js 16+ (for frontend tooling)
- Redis (local or Docker)
- Google API keys (PageSpeed Insights)

**Setup Instructions:**

1. **Clone and Setup Backend:**
   ```bash
   git clone <repository>
   cd aeo-assessment-tool/backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**
   ```bash
   # .env file
   GOOGLE_PAGESPEED_API_KEY=your_api_key_here
   REDIS_URL=redis://localhost:6379
   SECRET_KEY=your_secret_key_here
   ENVIRONMENT=development
   ```

3. **Start Services:**
   ```bash
   # Terminal 1: Redis
   redis-server
   
   # Terminal 2: Backend API
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 3: Frontend (if using live server)
   cd ../frontend
   python -m http.server 3000
   ```

4. **Testing:**
   ```bash
   # Run backend tests
   pytest
   
   # Test API endpoint
   curl -X POST "http://localhost:8000/api/analyze" \
        -H "Content-Type: application/json" \
        -d '{"url": "https://example.com", "email": "test@example.com"}'
   ```

---

## API Documentation

### Complete API Reference

**Base URL:** `https://yourdomain.com/api`

**Authentication:** API key in header (for premium features)

**Rate Limits:** 10 requests per hour per IP address

#### POST /analyze
Initiate website analysis

**Request:**
```json
{
  "url": "https://example.com",
  "email": "user@example.com",
  "callback_url": "https://yoursite.com/webhook" // optional
}
```

**Response:**
```json
{
  "analysis_id": "uuid-string",
  "status": "processing",
  "estimated_completion": "2024-01-01T12:05:00Z",
  "message": "Analysis started. Check results in 2-3 minutes."
}
```

#### GET /results/{analysis_id}
Get analysis results

**Response:**
```json
{
  "analysis_id": "uuid-string",
  "url": "https://example.com",
  "timestamp": "2024-01-01T12:03:00Z",
  "status": "completed",
  "overall_score": 75,
  "category_scores": {
    "performance": 18,
    "schema": 15,
    "content": 20,
    "technical": 22
  },
  "detailed_results": { /* full analysis data */ },
  "recommendations": [ /* prioritized recommendations */ ],
  "report_url": "/api/report/uuid-string/pdf"
}
```

This technical architecture provides a solid foundation for building the AEO Quick Assessment Tool with scalability, security, and maintainability in mind. The modular design allows for easy testing and future enhancements.

---

## Next Implementation Steps

1. **Setup Development Environment** (Day 1)
2. **Implement Core Analysis Engine** (Days 2-3)
3. **Build Frontend Interface** (Days 4-5)
4. **Integrate External APIs** (Days 6-7)
5. **Testing & Refinement** (Days 8-10)
6. **Deployment & Launch** (Days 11-14) 