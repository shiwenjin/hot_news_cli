from typing import Type
from .protocol import FetcherProtocol


class FetcherRegistry:
    """爬虫插件注册中心"""

    _fetchers: dict[str, Type[FetcherProtocol]] = {}

    @classmethod
    def register(cls, platform_id: str = None):
        """装饰器：注册爬虫插件"""
        def decorator(fetcher_cls: Type[FetcherProtocol]) -> Type[FetcherProtocol]:
            pid = platform_id or fetcher_cls.__name__.replace("Fetcher", "").lower()
            cls._fetchers[pid] = fetcher_cls
            return fetcher_cls
        return decorator

    @classmethod
    def get(cls, platform_id: str) -> Type[FetcherProtocol]:
        """获取爬虫类"""
        if platform_id not in cls._fetchers:
            raise ValueError(f"Unknown platform: {platform_id}")
        return cls._fetchers[platform_id]

    @classmethod
    def all(cls) -> dict[str, Type[FetcherProtocol]]:
        """获取所有已注册的爬虫"""
        return cls._fetchers.copy()

    @classmethod
    def list_platforms(cls) -> list[str]:
        """列出所有平台ID"""
        return list(cls._fetchers.keys())
