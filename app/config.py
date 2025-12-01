import toml
from pathlib import Path
from typing import Any, Dict
from threading import Lock

# 全局配置文件路径
CONFIG_PATH = "app/data/config.toml"
VERSION = "1.0.0"

class Config:
    _instance = None
    _lock = Lock()

    def __new__(cls, config_path: str = CONFIG_PATH):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._config_path = Path(config_path)
                    cls._instance._config = {}
                    cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """从文件加载配置到内存"""
        if self._config_path.exists():
            with open(self._config_path, 'r', encoding='utf-8') as f:
                self._config = toml.load(f)
        else:
            self._config = {}

    def get(self, key: str, default=None) -> Any:
        """支持点分隔的嵌套键，如 'database.host'"""
        keys = key.split('.')
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """设置配置值（支持嵌套）"""
        keys = key.split('.')
        target = self._config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def save(self):
        """将内存中的配置写回文件"""
        with open(self._config_path, 'w', encoding='utf-8') as f:
            toml.dump(self._config, f)

    def reload(self):
        """重新从文件加载配置（用于外部修改后刷新）"""
        self._load_config()

    @property
    def config(self) -> Dict:
        return self._config.copy()  # 返回副本，避免外部直接修改

# 全局实例（懒加载，线程安全）
config = Config()