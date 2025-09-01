#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

import pymysql
from utils.config import Config
from utils.logging_config import setup_logging

# 设置日志
logger = setup_logging(log_level='INFO')

def create_database():
    """
    创建数据库
    """
    try:
        config = Config()
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        logger.info(f"数据库 {config.MYSQL_DATABASE} 创建成功")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        logger.error(f"创建数据库失败: {str(e)}")
        raise

def create_tables():
    """
    创建数据表
    """
    try:
        from app import create_app
        from models.database import db
        
        app = create_app()
        
        with app.app_context():
            # 创建所有表
            db.create_all()
            logger.info("数据表创建成功")
            
    except Exception as e:
        logger.error(f"创建数据表失败: {str(e)}")
        raise

def main():
    """
    主函数
    """
    try:
        logger.info("开始初始化数据库...")
        
        # 创建数据库
        create_database()
        
        # 创建表
        create_tables()
        
        logger.info("数据库初始化完成！")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
