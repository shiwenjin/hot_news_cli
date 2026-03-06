"""知乎热榜爬虫"""
import httpx
from typing import Optional, List
from hot_news.core.protocol import FetcherProtocol
from hot_news.core.registry import FetcherRegistry
from hot_news.core.http import get
from hot_news.models import HotTrend, PlatformMetadata


@FetcherRegistry.register()
class ZhihuFetcher(FetcherProtocol):
    """知乎热榜爬虫"""

    BASE_URL = "https://api.zhihu.com/topstory/hot-lists/total"

    @property
    def metadata(self) -> PlatformMetadata:
        return PlatformMetadata(
            id="zhihu",
            name="知乎",
            icon="💬"
        )

    async def fetch(
        self,
        client: httpx.AsyncClient,
        limit: int = 50
    ) -> List[HotTrend]:
        """获取知乎热榜数据"""
        params = {"limit": limit}

        response = await get(client, self.BASE_URL, params=params)
        data = response.json()

        trends = []
        for i, item in enumerate(data.get("data", [])[:limit]):
            target = item.get("target", {})
            # detail_text 是字符串，如 "593 万热度"
            detail_text = item.get("detail_text", "")
            trends.append(HotTrend(
                platform=self.metadata.id,
                rank=i + 1,
                title=target.get("title", ""),
                # 将 API URL 转换为网页 URL
                url=f"https://www.zhihu.com/question/{target.get('id', '')}",
                hot=detail_text,  # 热度值（字符串格式）
                description=target.get("excerpt", ""),  # 描述/摘要
                extra={
                    "answer_count": target.get("answer_count"),
                    "follower_count": target.get("follower_count"),
                }
            ))

        return trends
