# AEO Assessment Tool - Backend

**Current Status**: Basic FastAPI-based backend service with Google PageSpeed integration  
**Goal**: Intelligent Answer Engine Optimization (AEO) analysis engine

> ⚠️ **Note**: This backend currently provides **basic website analysis** with excellent performance measurement. See roadmap below for planned intelligent AEO features.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Add your Google PageSpeed API key to .env
   ```

3. **Start the server:**
   ```bash
   python app.py
   ```

4. **Access the API:**
   - Server: http://localhost:8001
   - Health check: http://localhost:8001/health
   - API docs: http://localhost:8001/docs

## API Endpoints

### Health Check
- **GET** `/health` - Server health and API key status

### Website Analysis
- **POST** `/api/analyze` - Start website analysis
- **GET** `/api/analysis/{id}` - Get analysis results

## Environment Variables

Required:
- `GOOGLE_PAGESPEED_API_KEY` - Google PageSpeed Insights API key

Optional:
- `ENVIRONMENT` - development/production (default: development)

## Project Structure

```
backend/
├── app.py              # Main FastAPI application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── models/            # Data models
├── services/          # Analysis services
└── utils/             # Utility functions
```

## Current Analysis Process (Basic Implementation)

1. **✅ Performance Analysis** - Google PageSpeed Insights API (Advanced)
   - Real Core Web Vitals measurement
   - Mobile-first performance scoring
   
2. **🟡 Schema Markup Detection** - Basic presence detection (Needs Enhancement)
   - JSON-LD script tag detection (+15 points)
   - Microdata attribute detection (+10 points)
   - *Missing: Schema validation, AEO-specific schemas, completeness check*

3. **🔴 Content Structure Analysis** - Minimal implementation (Needs Major Enhancement)
   - Simple heading count (3+ headings = 10 points, else 5 points)
   - *Missing: FAQ detection, Q&A patterns, content quality, conversational analysis*

4. **🔴 Technical SEO Check** - Minimal implementation (Needs Enhancement)
   - HTTPS detection only (+10 points)
   - *Missing: Meta tags, mobile optimization, site structure, accessibility*

## Current Scoring System (Basic - 175 max points)

- **✅ Performance**: 0-100 (Real Google PageSpeed score - Advanced)
- **🟡 Schema Markup**: 0-25 (Basic presence detection - Needs Enhancement)
- **🔴 Content Structure**: 0-25 (Heading count only - Needs Major Enhancement)  
- **🔴 Technical SEO**: 0-25 (HTTPS only - Needs Enhancement)
- **Current Overall Score**: Sum of all categories (max 175 points)

## Target Intelligent Scoring System (500 max points)

- **Performance Intelligence**: 0-100 (Core Web Vitals + Mobile + Speed)
- **Answer Engine Readiness**: 0-100 (FAQ + Conversational + Completeness + Entities)
- **Schema Intelligence**: 0-100 (AEO Schemas + Knowledge Graph + Rich Snippets)
- **Content Structure Intelligence**: 0-100 (Questions + Answers + Depth + Readability)
- **Technical AEO Foundation**: 0-100 (Mobile + Architecture + Speed + Accessibility)

## Intelligence Roadmap

### Phase 1: Enhanced Content Analysis
```python
# TODO: Implement FAQ detection
def detect_faq_patterns(content):
    # Identify question-answer structures
    # Extract Q&A pairs  
    # Analyze conversational tone
    pass
```

### Phase 2: Schema Intelligence  
```python
# TODO: AEO-specific schema validation
def analyze_aeo_schemas(page):
    # Validate FAQ schema
    # Check HowTo schema
    # Assess Q&A schema completeness
    pass
```

### Phase 3: Voice Search Optimization
```python
# TODO: Voice search readiness analysis
def analyze_voice_search_potential(content):
    # Natural language query detection
    # Featured snippet format analysis
    # Local intent optimization
    pass
``` 