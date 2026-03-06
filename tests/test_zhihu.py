"""知乎爬虫测试"""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from hot_news.fetchers.zhihu import ZhihuFetcher
from hot_news.models import HotTrend, PlatformMetadata


class TestZhihuFetcher:
    """知乎爬虫测试"""

    @pytest.fixture
    def fetcher(self):
        """创建爬虫实例"""
        return ZhihuFetcher()

    def test_metadata(self, fetcher):
        """测试元数据"""
        metadata = fetcher.metadata
        
        assert isinstance(metadata, PlatformMetadata)
        assert metadata.id == "zhihu"
        assert metadata.name == "知乎"
        assert metadata.icon == "💬"

    @pytest.mark.asyncio
    async def test_fetch_success(self, fetcher):
        """测试成功获取数据 - 使用真实 API 响应格式"""
        # 模拟真实 API 响应
        mock_response_data = {
            "data": [
                {
                    "target": {
                        "id": 2012997512626136587,
                        "title": "人大建议短视频凌晨 1 点至 5 点深夜强制未成年下线",
                        "excerpt": "这是一个测试摘要内容",
                        "answer_count": 843,
                        "follower_count": 1211
                    },
                    "detail_text": "593 万热度"  # 实际是字符串，不是字典
                },
                {
                    "target": {
                        "id": 2013179466591987479,
                        "title": "建议最低法定年假从5天提至10天",
                        "excerpt": "另一个摘要内容",
                        "answer_count": 249,
                        "follower_count": 340
                    },
                    "detail_text": "300 万热度"
                }
            ]
        }

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_client.request = AsyncMock(return_value=mock_response)

        # 执行 fetch
        trends = await fetcher.fetch(mock_client, limit=10)

        # 验证结果
        assert len(trends) == 2
        
        # 验证第一条
        assert trends[0].platform == "zhihu"
        assert trends[0].rank == 1
        assert trends[0].title == "人大建议短视频凌晨 1 点至 5 点深夜强制未成年下线"
        assert trends[0].url == "https://www.zhihu.com/question/2012997512626136587"
        assert trends[0].hot == "593 万热度"  # 验证是字符串
        assert trends[0].description == "这是一个测试摘要内容"  # 验证描述字段
        assert trends[0].extra["answer_count"] == 843
        
        # 验证第二条
        assert trends[1].rank == 2
        assert trends[1].hot == "300 万热度"
        assert trends[1].description == "另一个摘要内容"

    @pytest.mark.asyncio
    async def test_fetch_limit(self, fetcher):
        """测试 limit 参数"""
        mock_response_data = {
            "data": [
                {"target": {"id": i, "title": f"问题{i}"}, "detail_text": f"{i}万热度"}
                for i in range(1, 51)
            ]
        }

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_client.request = AsyncMock(return_value=mock_response)

        # 请求 10 条
        trends = await fetcher.fetch(mock_client, limit=10)

        assert len(trends) == 10

    @pytest.mark.asyncio
    async def test_fetch_empty(self, fetcher):
        """测试空数据"""
        mock_response_data = {"data": []}

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_client.request = AsyncMock(return_value=mock_response)

        trends = await fetcher.fetch(mock_client, limit=10)

        assert len(trends) == 0

    @pytest.mark.asyncio
    async def test_fetch_url_format(self, fetcher):
        """测试 URL 格式正确转换"""
        mock_response_data = {
            "data": [
                {
                    "target": {
                        "id": 1234567890123456789,
                        "title": "测试问题",
                        "excerpt": "这是描述内容",
                        "answer_count": 10,
                        "follower_count": 100
                    },
                    "detail_text": "100 万热度"
                }
            ]
        }

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_client.request = AsyncMock(return_value=mock_response)

        trends = await fetcher.fetch(mock_client, limit=10)

        # 验证 URL 格式正确
        assert trends[0].url == "https://www.zhihu.com/question/1234567890123456789"
        # 验证描述字段
        assert trends[0].description == "这是描述内容"
