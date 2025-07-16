"""
Configuration management for AEO Assessment Tool
"""

import os
from functools import lru_cache
from typing import List


class Settings:
    """Application settings"""
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # API Keys
    GOOGLE_PAGESPEED_API_KEY: str = os.getenv("GOOGLE_PAGESPEED_API_KEY", "")
    GOOGLE_SEARCH_CONSOLE_API_KEY: str = os.getenv("GOOGLE_SEARCH_CONSOLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "admin-secret-key")
    
    # Database & Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aeo_tool.db")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://yourdomain.com"  # Replace with actual domain
    ]
    
    # Feature Flags
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    ENABLE_EMAIL_NOTIFICATIONS: bool = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    
    # Email Configuration (if enabled)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")
    
    # Analysis Settings
    ANALYSIS_TIMEOUT: int = int(os.getenv("ANALYSIS_TIMEOUT", "180"))  # 3 minutes
    MAX_CONCURRENT_ANALYSES: int = int(os.getenv("MAX_CONCURRENT_ANALYSES", "10"))
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def __init__(self):
        """Validate required settings"""
        if self.ENVIRONMENT == "production":
            required_vars = [
                "GOOGLE_PAGESPEED_API_KEY",
                "SECRET_KEY",
                "REDIS_URL"
            ]
            
            missing_vars = [var for var in required_vars if not getattr(self, var)]
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {missing_vars}")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings() 