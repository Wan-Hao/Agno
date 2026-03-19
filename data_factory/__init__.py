"""
Data Factory Module
负责原始数据的摄入、清洗、辩论和图谱构建。
"""

from pathlib import Path

# 原始数据目录
RAW_DATA_DIR = Path(__file__).parent.parent / "dataset" / "raw_data"
TEXT_DATA_DIR = RAW_DATA_DIR / "texts"
IMAGE_DATA_DIR = RAW_DATA_DIR / "images"


