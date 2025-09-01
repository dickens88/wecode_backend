#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接创建数据表的脚本
"""

import pymysql
from utils.config import Config
from utils.logging_config import setup_logging

# 设置日志
logger = setup_logging(log_level='INFO')

def create_tables():
    """创建数据表"""
    try:
        config = Config()
        
        # 连接数据库
        connection = pymysql.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DATABASE,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建AI任务表（修改后的结构）
        create_activities_table = """
        CREATE TABLE IF NOT EXISTS t_event_activities (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
            event_id VARCHAR(100) NOT NULL COMMENT '工单ID',
            task_id VARCHAR(36) NOT NULL UNIQUE COMMENT '任务UUID',
            app_id VARCHAR(100) NOT NULL COMMENT '应用ID',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            task_content TEXT NOT NULL COMMENT '任务内容',
            status VARCHAR(20) DEFAULT 'init' COMMENT '任务状态: init, running, complete',
            title VARCHAR(500) DEFAULT NULL COMMENT '任务标题（由AI返回结果填充）',
            description TEXT DEFAULT NULL COMMENT '任务描述（由AI返回结果填充）',
            result TEXT DEFAULT NULL COMMENT '任务结果（由AI返回结果填充）',
            INDEX idx_event_id (event_id),
            INDEX idx_task_id (task_id),
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI任务表'
        """
        
        # 创建新的AI代理任务异步表
        create_agent_task_table = """
        CREATE TABLE IF NOT EXISTS t_ai_agent_task_async (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
            task_id VARCHAR(36) NOT NULL UNIQUE COMMENT '任务UUID',
            app_id VARCHAR(100) NOT NULL COMMENT '应用ID',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            task_content TEXT NOT NULL COMMENT '任务内容',
            status VARCHAR(20) DEFAULT 'init' COMMENT '任务状态: init, running, complete',
            result TEXT DEFAULT NULL COMMENT '任务结果（由AI返回结果填充）',
            INDEX idx_task_id (task_id),
            INDEX idx_app_id (app_id),
            INDEX idx_status (status),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI代理任务异步表'
        """
        
        # 创建AI任务结果表
        create_artifacts_table = """
        CREATE TABLE IF NOT EXISTS t_event_artifacts (
            id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
            activity_id INT NOT NULL COMMENT '关联的AI任务ID',
            artifact_data JSON NOT NULL COMMENT 'AI任务返回结果',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
            INDEX idx_activity_id (activity_id),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI任务结果表'
        """
        
        # 执行创建表的SQL
        logger.info("正在创建AI任务表...")
        cursor.execute(create_activities_table)
        
        logger.info("正在创建AI代理任务异步表...")
        cursor.execute(create_agent_task_table)
        
        logger.info("正在创建AI任务结果表...")
        cursor.execute(create_artifacts_table)
        
        # 添加外键约束
        add_foreign_key = """
        ALTER TABLE t_event_artifacts 
        ADD CONSTRAINT fk_artifacts_activity 
        FOREIGN KEY (activity_id) REFERENCES t_event_activities(id) ON DELETE CASCADE
        """
        
        try:
            cursor.execute(add_foreign_key)
            logger.info("外键约束添加成功")
        except Exception as e:
            logger.warning(f"外键约束可能已存在: {str(e)}")
        
        # 提交事务
        connection.commit()
        
        logger.info("数据表创建成功！")
        
        # 显示表结构
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        logger.info(f"当前数据库中的表: {[table[0] for table in tables]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        logger.error(f"创建数据表失败: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        logger.info("开始创建数据表...")
        
        if create_tables():
            logger.info("数据表创建完成！")
            logger.info("现在您可以运行 'python app.py' 来启动应用")
        else:
            logger.error("数据表创建失败")
            exit(1)
            
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
