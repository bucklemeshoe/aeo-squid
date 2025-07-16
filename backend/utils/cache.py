"""
Redis cache management utilities
"""

import redis.asyncio as redis
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class CacheManager:
    """Redis cache management"""
    
    def __init__(self, redis_url: str):
        """
        Initialize cache manager
        
        Args:
            redis_url: Redis connection URL
        """
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            logger.info(f"Initialized Redis cache manager")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            # Fallback to in-memory cache
            self.redis_client = None
            self._memory_cache = {}
    
    async def get_cached_result(self, cache_key: str) -> Optional[Dict[Any, Any]]:
        """
        Get cached result
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached result or None
        """
        try:
            if self.redis_client:
                cached = await self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            else:
                # Fallback to memory cache
                return self._memory_cache.get(cache_key)
        except Exception as e:
            logger.error(f"Cache get error for key {cache_key}: {e}")
        
        return None
    
    async def cache_result(self, cache_key: str, data: Dict[Any, Any], ttl: int = 3600):
        """
        Cache result
        
        Args:
            cache_key: Cache key
            data: Data to cache
            ttl: Time to live in seconds
        """
        try:
            if self.redis_client:
                await self.redis_client.setex(
                    cache_key, 
                    ttl, 
                    json.dumps(data, default=str)
                )
            else:
                # Fallback to memory cache with basic TTL
                expiry = datetime.utcnow() + timedelta(seconds=ttl)
                self._memory_cache[cache_key] = {
                    'data': data,
                    'expiry': expiry
                }
                
        except Exception as e:
            logger.error(f"Cache set error for key {cache_key}: {e}")
    
    async def delete_cached_result(self, cache_key: str):
        """
        Delete cached result
        
        Args:
            cache_key: Cache key to delete
        """
        try:
            if self.redis_client:
                await self.redis_client.delete(cache_key)
            else:
                self._memory_cache.pop(cache_key, None)
        except Exception as e:
            logger.error(f"Cache delete error for key {cache_key}: {e}")
    
    async def clear_expired_cache(self):
        """Clear expired entries from memory cache"""
        if not self.redis_client and hasattr(self, '_memory_cache'):
            now = datetime.utcnow()
            expired_keys = [
                key for key, value in self._memory_cache.items()
                if isinstance(value, dict) and value.get('expiry', now) < now
            ]
            for key in expired_keys:
                del self._memory_cache[key]
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Cache statistics
        """
        stats = {
            'type': 'redis' if self.redis_client else 'memory',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            if self.redis_client:
                info = await self.redis_client.info()
                stats.update({
                    'connected_clients': info.get('connected_clients', 0),
                    'used_memory': info.get('used_memory', 0),
                    'total_commands_processed': info.get('total_commands_processed', 0)
                })
            else:
                stats.update({
                    'memory_cache_size': len(self._memory_cache),
                    'memory_cache_keys': list(self._memory_cache.keys())
                })
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            stats['error'] = str(e)
        
        return stats
    
    async def close(self):
        """Close cache connections"""
        try:
            if self.redis_client:
                await self.redis_client.close()
        except Exception as e:
            logger.error(f"Error closing cache connection: {e}")
    
    def _serialize_for_cache(self, data: Any) -> str:
        """
        Serialize data for caching
        
        Args:
            data: Data to serialize
            
        Returns:
            Serialized string
        """
        try:
            return json.dumps(data, default=str)
        except Exception as e:
            logger.error(f"Serialization error: {e}")
            return "{}"
    
    def _deserialize_from_cache(self, data: str) -> Optional[Dict]:
        """
        Deserialize data from cache
        
        Args:
            data: Serialized data
            
        Returns:
            Deserialized data or None
        """
        try:
            return json.loads(data)
        except Exception as e:
            logger.error(f"Deserialization error: {e}")
            return None 