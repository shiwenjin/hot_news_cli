import pkgutil
import importlib
from pathlib import Path


def load_fetchers() -> None:
    """自动加载所有爬虫插件"""
    # 获取 fetchers 包路径
    fetchers_dir = Path(__file__).parent.parent / "fetchers"
    
    if not fetchers_dir.exists():
        return
    
    # 遍历模块
    for module_info in pkgutil.iter_modules([str(fetchers_dir)]):
        module_name = module_info.name
        
        # 跳过 __init__ 和私有模块
        if module_name.startswith("_"):
            continue
        
        # 导入模块，触发注册
        importlib.import_module(f"hot_news.fetchers.{module_name}")
