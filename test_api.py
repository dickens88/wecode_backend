#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
"""

import requests
import json
import time

# 测试配置
BASE_URL = 'http://localhost:5000'
TEST_EVENT_ID = 'test_event_123'
TEST_APP_ID = 'test_app_456'

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_index():
    """测试根路径接口"""
    print("=== 测试根路径接口 ===")
    
    url = f"{BASE_URL}/"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_get_tickets():
    """测试获取工单列表接口"""
    print("=== 测试获取工单列表接口 ===")
    
    url = f"{BASE_URL}/tickets/events"
    params = {
        'offset': 1,
        'size': 10,
        'status': 'open',
        'time': '24h',
        'keyword': 'test'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_get_ticket_detail():
    """测试获取工单详情接口"""
    print("=== 测试获取工单详情接口 ===")
    
    url = f"{BASE_URL}/tickets/events/{TEST_EVENT_ID}"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_create_ai_task():
    """测试创建AI任务接口"""
    print("=== 测试创建AI任务接口 ===")
    
    url = f"{BASE_URL}/tickets/events/{TEST_EVENT_ID}/activities"
    data = {
        'app_id': TEST_APP_ID,
        'task_content': '这是一个测试AI任务，用于验证接口功能'
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_get_activities():
    """测试获取AI任务列表接口"""
    print("=== 测试获取AI任务列表接口 ===")
    
    url = f"{BASE_URL}/tickets/events/{TEST_EVENT_ID}/activities"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def test_get_artifacts():
    """测试获取AI任务结果接口"""
    print("=== 测试获取AI任务结果接口 ===")
    
    url = f"{BASE_URL}/tickets/events/{TEST_EVENT_ID}/artifacts"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {str(e)}")
    
    print()

def main():
    """主测试函数"""
    print("开始API接口测试...")
    print(f"测试目标: {BASE_URL}")
    print()
    
    # 等待应用启动
    print("等待应用启动...")
    time.sleep(2)
    
    # 执行测试
    test_health_check()
    test_index()
    test_get_tickets()
    test_get_ticket_detail()
    test_create_ai_task()
    test_get_activities()
    test_get_artifacts()
    
    print("API接口测试完成！")

if __name__ == '__main__':
    main()
