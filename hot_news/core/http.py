import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


# 可重试的异常类型
RETRYABLE_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.NetworkError,
)


@retry(
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_exponential(multiplier=1, min=1, max=10),  # 指数退避: 1s, 2s, 4s
    reraise=True,
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
)
async def request(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    **kwargs
) -> httpx.Response:
    """统一 HTTP 请求封装 - 带重试机制"""
    response = await client.request(method, url, **kwargs)
    response.raise_for_status()
    return response


async def get(client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response:
    """GET 请求"""
    return await request(client, "GET", url, **kwargs)


async def post(client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response:
    """POST 请求"""
    return await request(client, "POST", url, **kwargs)
