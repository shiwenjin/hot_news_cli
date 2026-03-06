import httpx
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from hot_news.models import HotTrend, PlatformMetadata


class FetcherProtocol(ABC):
    """爬虫插件协议"""

    @property
    @abstractmethod
    def metadata(self) -> "PlatformMetadata":
        """平台元信息"""
        ...

    @abstractmethod
    async def fetch(
        self,
        client: httpx.AsyncClient,
        limit: int = 50
    ) -> List["HotTrend"]:
        """获取热榜数据"""
        ...
