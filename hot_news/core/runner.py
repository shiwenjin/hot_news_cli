import asyncio

import httpx

from .registry import FetcherRegistry
from hot_news.models import FetchResult


class FetchRunner:
    """统一调度层 - 控制并发、统一错误处理"""

    def __init__(
        self,
        timeout: float = 10.0,
        max_concurrency: int = 10
    ):
        self.timeout = timeout
        self.max_concurrency = max_concurrency

    async def run(
        self,
        platforms: list[str],
        limit: int = 20
    ) -> dict[str, FetchResult]:
        """获取多个平台的热榜数据"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            semaphore = asyncio.Semaphore(self.max_concurrency)

            async def fetch_one(p: str) -> tuple[str, FetchResult]:
                async with semaphore:
                    try:
                        fetcher = FetcherRegistry.get(p)()
                        data = await fetcher.fetch(client, limit)
                        return p, FetchResult(platform=p, success=True, data=data)
                    except Exception as e:
                        return p, FetchResult(platform=p, success=False, error=str(e))

            tasks = [fetch_one(p) for p in platforms]
            results = await asyncio.gather(*tasks)
            return dict(results)
