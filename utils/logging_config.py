#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置文件
"""

import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging(log_level='INFO', log_file=None, max_bytes=10*1024*1024, backup_count=5):
    """
    设置日志配置
    
    Args:
        log_level: 日志级别，默认INFO
        log_file: 日志文件路径，如果为None则只输出到控制台
        max_bytes: 单个日志文件最大大小，默认10MB
        backup_count: 保留的日志文件数量，默认5个
    """
    # 创建logs目录
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('apscheduler').setLevel(logging.INFO)
    
    return root_logger

def get_logger(name):
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)

def setup_app_logging(app_name='WeCodeSecTools', log_dir='logs'):
    """
    为应用设置日志配置
    
    Args:
        app_name: 应用名称
        log_dir: 日志目录
        
    Returns:
        logging.Logger: 应用日志记录器
    """
    # 创建日志目录
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # 设置日志文件路径
    log_file = log_path / f"{app_name.lower()}.log"
    
    # 设置日志配置
    setup_logging(
        log_level='INFO',
        log_file=str(log_file),
        max_bytes=10*1024*1024,  # 10MB
        backup_count=5
    )
    
    # 获取应用日志记录器
    app_logger = get_logger(app_name)
    app_logger.info(f"应用日志系统初始化完成，日志文件：{log_file}")
    
    return app_logger
