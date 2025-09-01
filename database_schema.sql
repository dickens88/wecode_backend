-- WeCodeSecTools 数据库表结构
-- 创建数据库
CREATE DATABASE IF NOT EXISTS wecode_sec_tools CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE wecode_sec_tools;

-- AI任务表
CREATE TABLE IF NOT EXISTS t_event_activities (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    event_id VARCHAR(100) NOT NULL COMMENT '工单ID',
    task_id VARCHAR(36) NOT NULL UNIQUE COMMENT '任务UUID',
    app_id VARCHAR(100) NOT NULL COMMENT '应用ID',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    task_content TEXT NOT NULL COMMENT '任务内容',
    status VARCHAR(20) DEFAULT 'init' COMMENT '任务状态: init, running, complete',
    INDEX idx_event_id (event_id),
    INDEX idx_task_id (task_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI任务表';

-- AI任务结果表
CREATE TABLE IF NOT EXISTS t_event_artifacts (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    activity_id INT NOT NULL COMMENT '关联的AI任务ID',
    artifact_data JSON NOT NULL COMMENT 'AI任务返回结果',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (activity_id) REFERENCES t_event_activities(id) ON DELETE CASCADE,
    INDEX idx_activity_id (activity_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI任务结果表';

-- 插入测试数据
INSERT INTO t_event_activities (event_id, task_id, app_id, task_content, status) VALUES
('test_event_123', '550e8400-e29b-41d4-a716-446655440000', 'test_app_456', '测试AI任务1', 'init'),
('test_event_124', '550e8400-e29b-41d4-a716-446655440001', 'test_app_457', '测试AI任务2', 'running'),
('test_event_125', '550e8400-e29b-41d4-a716-446655440002', 'test_app_458', '测试AI任务3', 'complete');

-- 插入测试结果数据
INSERT INTO t_event_artifacts (activity_id, artifact_data) VALUES
(3, '{"result": "测试结果", "status": "success", "data": {"key": "value"}}');
