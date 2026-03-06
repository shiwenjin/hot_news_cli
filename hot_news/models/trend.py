from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, List


@dataclass
class HotTrend:
    """单条热榜数据"""
    platform: str  # 平台ID
    rank: int  # 排名
    title: str  # 标题
    url: str  # 链接
    hot: Optional[int] = None  # 热度值
    description: Optional[str] = None  # 描述/摘要
    extra: Optional[dict] = None  # 平台特有字段
    timestamp: datetime = field(default_factory=datetime.utcnow)  # 时间戳


@dataclass
class PlatformMetadata:
    """平台元信息"""
    id: str  # 唯一标识
    name: str  # 显示名称
    icon: str  # Emoji 图标


@dataclass
class FetchResult:
    """单个平台的获取结果"""
    platform: str
    success: bool
    data: Optional[List[HotTrend]] = None
    error: Optional[str] = None
