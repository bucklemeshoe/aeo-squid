"""
Rate limiting utilities
"""

import logging
from typing import Optional
import time
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, redis_client):
        """
        Initialize rate limiter
        
        Args:
            redis_client: Redis client instance
        """
        self.redis = redis_client
        self._memory_store = {}  # Fallback for when Redis is unavailable
    
    async def check_rate_limit(
        self, 
        identifier: str, 
        limit: int = 10, 
        window: int = 3600
    ) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            True if within limit, False if exceeded
        """
        try:
            if self.redis:
                return await self._check_redis_rate_limit(identifier, limit, window)
            else:
                return await self._check_memory_rate_limit(identifier, limit, window)
        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            # Fail open - allow request if rate limiting fails
            return True
    
    async def _check_redis_rate_limit(
        self, 
        identifier: str, 
        limit: int, 
        window: int
    ) -> bool:
        """
        Check rate limit using Redis
        
        Args:
            identifier: Unique identifier
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            True if within limit
        """
        key = f"rate_limit:{identifier}"
        
        try:
            # Use Redis pipeline for atomic operations
            pipe = self.redis.pipeline()
            
            # Increment counter
            pipe.incr(key)
            
            # Set expiry if this is the first request
            pipe.expire(key, window)
            
            # Execute pipeline
            results = await pipe.execute()
            current_count = results[0]
            
            if current_count <= limit:
                logger.debug(f"Rate limit OK for {identifier}: {current_count}/{limit}")
                return True
            else:
                logger.warning(f"Rate limit exceeded for {identifier}: {current_count}/{limit}")
                return False
                
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            return True  # Fail open
    
    async def _check_memory_rate_limit(
        self, 
        identifier: str, 
        limit: int, 
        window: int
    ) -> bool:
        """
        Check rate limit using memory store (fallback)
        
        Args:
            identifier: Unique identifier
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            True if within limit
        """
        now = time.time()
        window_start = now - window
        
        # Clean up old entries
        if identifier in self._memory_store:
            self._memory_store[identifier] = [
                timestamp for timestamp in self._memory_store[identifier]
                if timestamp > window_start
            ]
        else:
            self._memory_store[identifier] = []
        
        # Check current count
        current_count = len(self._memory_store[identifier])
        
        if current_count < limit:
            # Add current request
            self._memory_store[identifier].append(now)
            logger.debug(f"Memory rate limit OK for {identifier}: {current_count + 1}/{limit}")
            return True
        else:
            logger.warning(f"Memory rate limit exceeded for {identifier}: {current_count}/{limit}")
            return False
    
    async def get_rate_limit_info(self, identifier: str, window: int = 3600) -> dict:
        """
        Get rate limit information for identifier
        
        Args:
            identifier: Unique identifier
            window: Time window in seconds
            
        Returns:
            Rate limit information
        """
        try:
            if self.redis:
                key = f"rate_limit:{identifier}"
                current_count = await self.redis.get(key)
                ttl = await self.redis.ttl(key)
                
                return {
                    'current_count': int(current_count) if current_count else 0,
                    'time_remaining': ttl if ttl > 0 else window,
                    'window': window
                }
            else:
                now = time.time()
                window_start = now - window
                
                if identifier in self._memory_store:
                    requests = [
                        ts for ts in self._memory_store[identifier]
                        if ts > window_start
                    ]
                    current_count = len(requests)
                    oldest_request = min(requests) if requests else now
                    time_remaining = window - (now - oldest_request)
                else:
                    current_count = 0
                    time_remaining = window
                
                return {
                    'current_count': current_count,
                    'time_remaining': max(0, int(time_remaining)),
                    'window': window
                }
                
        except Exception as e:
            logger.error(f"Error getting rate limit info: {e}")
            return {
                'current_count': 0,
                'time_remaining': window,
                'window': window,
                'error': str(e)
            }
    
    async def reset_rate_limit(self, identifier: str):
        """
        Reset rate limit for identifier
        
        Args:
            identifier: Unique identifier to reset
        """
        try:
            if self.redis:
                key = f"rate_limit:{identifier}"
                await self.redis.delete(key)
            else:
                self._memory_store.pop(identifier, None)
                
            logger.info(f"Rate limit reset for {identifier}")
            
        except Exception as e:
            logger.error(f"Error resetting rate limit: {e}")
    
    async def cleanup_expired_entries(self):
        """Clean up expired entries from memory store"""
        if not self.redis:
            now = time.time()
            window = 3600  # Use default window for cleanup
            
            for identifier in list(self._memory_store.keys()):
                window_start = now - window
                self._memory_store[identifier] = [
                    timestamp for timestamp in self._memory_store[identifier]
                    if timestamp > window_start
                ]
                
                # Remove empty entries
                if not self._memory_store[identifier]:
                    del self._memory_store[identifier] 