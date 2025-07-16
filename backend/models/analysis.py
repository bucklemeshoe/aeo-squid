"""
Data models for AEO analysis requests and responses
"""

from pydantic import BaseModel, EmailStr, HttpUrl, validator
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class AnalysisStatus(str, Enum):
    """Analysis status enumeration"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRequest(BaseModel):
    """Request model for initiating website analysis"""
    url: str
    email: EmailStr
    callback_url: Optional[str] = None
    
    @validator('url')
    def validate_url(cls, v):
        """Validate URL format"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com",
                "email": "user@example.com",
                "callback_url": "https://yoursite.com/webhook"
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis initiation"""
    analysis_id: str
    status: AnalysisStatus
    estimated_completion: datetime
    message: str
    cached: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "uuid-string-here",
                "status": "processing",
                "estimated_completion": "2024-01-01T12:05:00Z",
                "message": "Analysis started. Results will be available in 2-3 minutes.",
                "cached": False
            }
        }


class ProgressInfo(BaseModel):
    """Progress information for ongoing analysis"""
    percentage: int
    current_step: str
    steps_completed: List[str]


class PerformanceResult(BaseModel):
    """Performance analysis results"""
    lcp: float  # Largest Contentful Paint
    fid: float  # First Input Delay
    cls: float  # Cumulative Layout Shift
    score: int  # Overall performance score (0-100)
    mobile_score: Optional[int] = None
    desktop_score: Optional[int] = None
    
    class Config:
        schema_extra = {
            "example": {
                "lcp": 2.1,
                "fid": 120,
                "cls": 0.08,
                "score": 85,
                "mobile_score": 82,
                "desktop_score": 88
            }
        }


class SchemaResult(BaseModel):
    """Schema markup analysis results"""
    faq_schema_present: bool
    qa_schema_present: bool
    howto_schema_present: bool
    organization_schema_present: bool
    local_business_schema_present: bool
    validation_errors: List[str]
    total_schemas_found: int
    
    class Config:
        schema_extra = {
            "example": {
                "faq_schema_present": True,
                "qa_schema_present": False,
                "howto_schema_present": True,
                "organization_schema_present": True,
                "local_business_schema_present": False,
                "validation_errors": [],
                "total_schemas_found": 3
            }
        }


class ContentResult(BaseModel):
    """Content structure analysis results"""
    heading_structure_score: int
    faq_patterns_found: int
    qa_content_detected: bool
    word_count: int
    readability_score: Optional[float] = None
    conversational_queries_optimized: int
    
    class Config:
        schema_extra = {
            "example": {
                "heading_structure_score": 8,
                "faq_patterns_found": 5,
                "qa_content_detected": True,
                "word_count": 1250,
                "readability_score": 7.8,
                "conversational_queries_optimized": 12
            }
        }


class TechnicalResult(BaseModel):
    """Technical SEO analysis results"""
    https_enabled: bool
    mobile_friendly: bool
    sitemap_present: bool
    robots_txt_present: bool
    page_speed_score: int
    core_web_vitals_passed: bool
    
    class Config:
        schema_extra = {
            "example": {
                "https_enabled": True,
                "mobile_friendly": True,
                "sitemap_present": True,
                "robots_txt_present": True,
                "page_speed_score": 87,
                "core_web_vitals_passed": True
            }
        }


class Recommendation(BaseModel):
    """Individual recommendation"""
    category: str
    title: str
    description: str
    impact: str  # "High", "Medium", "Low"
    difficulty: str  # "Easy", "Medium", "Hard"
    action_items: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "category": "Schema",
                "title": "Add FAQ Schema Markup",
                "description": "Implement JSON-LD FAQ schema to help AI engines understand your Q&A content.",
                "impact": "High",
                "difficulty": "Medium",
                "action_items": [
                    "Identify top 5 FAQ pages",
                    "Add JSON-LD FAQ schema markup",
                    "Validate with Google's Rich Results Test"
                ]
            }
        }


class Issue(BaseModel):
    """Critical issue found during analysis"""
    category: str
    title: str
    description: str
    severity: str  # "Critical", "Important", "Minor"
    fix_guidance: str


class CategoryScores(BaseModel):
    """Scores for each analysis category"""
    performance: int  # 0-25
    schema: int      # 0-25
    content: int     # 0-25
    technical: int   # 0-25


class DetailedResults(BaseModel):
    """Detailed analysis results for each category"""
    performance_details: PerformanceResult
    schema_details: SchemaResult
    content_details: ContentResult
    technical_details: TechnicalResult


class AnalysisResults(BaseModel):
    """Complete analysis results"""
    analysis_id: str
    url: str
    timestamp: datetime
    status: AnalysisStatus
    overall_score: int  # 0-100
    
    # Category scores
    category_scores: Optional[CategoryScores] = None
    
    # Detailed results
    detailed_results: Optional[DetailedResults] = None
    
    # Recommendations and issues
    recommendations: Optional[List[Recommendation]] = None
    priority_issues: Optional[List[Issue]] = None
    
    # Progress information (for ongoing analyses)
    progress: Optional[ProgressInfo] = None
    
    # Report URL
    report_url: Optional[str] = None
    
    # Error information (for failed analyses)
    error: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "analysis_id": "uuid-string-here",
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
                "report_url": "/api/report/uuid-string-here/pdf"
            }
        }


class AnalyticsSummary(BaseModel):
    """Analytics summary for admin dashboard"""
    total_analyses: int
    completed_analyses: int
    failed_analyses: int
    success_rate: float
    avg_score: float
    popular_domains: List[str]
    timestamp: datetime 