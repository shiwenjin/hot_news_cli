"""CLI 入口"""
import typer
import asyncio
import json
from datetime import datetime
from typing import Optional, List

from hot_news.core.loader import load_fetchers
from hot_news.core.registry import FetcherRegistry
from hot_news.core.runner import FetchRunner
from hot_news.models import FetchResult

app = typer.Typer(help="多平台热榜命令行工具")


def format_output(results: dict[str, FetchResult], pretty: bool = False) -> str:
    """格式化输出为 JSON"""
    platforms = []
    
    for platform_id, result in results.items():
        fetcher_cls = FetcherRegistry.get(platform_id)
        fetcher = fetcher_cls()
        metadata = fetcher.metadata
        
        if result.success and result.data:
            trends = [
                {
                    "rank": t.rank,
                    "title": t.title,
                    "description": t.description,
                    "hot": t.hot,
                    "url": t.url,
                    "extra": t.extra,
                }
                for t in result.data
            ]
            count = len(trends)
            success = True
        else:
            trends = []
            count = 0
            success = False
        
        platforms.append({
            "id": metadata.id,
            "name": metadata.name,
            "icon": metadata.icon,
            "success": success,
            "count": count,
            "trends": trends,
            "error": result.error if not success else None,
        })
    
    output = {
        "version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_platforms": len(platforms),
        "platforms": platforms,
    }
    
    if pretty:
        return json.dumps(output, ensure_ascii=False, indent=2)
    return json.dumps(output, ensure_ascii=False)


@app.command("list")
def list_platforms():
    """列出所有可用平台"""
    load_fetchers()
    platforms = FetcherRegistry.list_platforms()
    
    result = {
        "platforms": platforms,
        "total": len(platforms),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("get")
def get_trends(
    platforms: Optional[List[str]] = typer.Argument(None, help="平台 ID，不指定则获取所有平台"),
    limit: int = typer.Option(20, "-n", "--limit", help="每平台返回条数"),
    pretty: bool = typer.Option(False, "--pretty", help="美化 JSON 输出"),
    timeout: float = typer.Option(10.0, "--timeout", help="请求超时时间(秒)"),
):
    """获取热榜数据"""
    # 加载所有爬虫
    load_fetchers()
    
    # 确定要获取的平台
    if platforms:
        # 验证平台是否存在
        all_platforms = FetcherRegistry.list_platforms()
        for p in platforms:
            if p not in all_platforms:
                typer.echo(f"错误: 未知平台 '{p}'", err=True)
                typer.echo(f"可用平台: {', '.join(all_platforms)}", err=True)
                raise typer.Exit(1)
        target_platforms = platforms
    else:
        target_platforms = FetcherRegistry.list_platforms()
    
    if not target_platforms:
        typer.echo("错误: 没有可用的平台", err=True)
        raise typer.Exit(1)
    
    # 异步获取数据
    runner = FetchRunner(timeout=timeout)
    results = asyncio.run(runner.run(target_platforms, limit))
    
    # 输出结果
    output = format_output(results, pretty)
    print(output)


if __name__ == "__main__":
    app()
