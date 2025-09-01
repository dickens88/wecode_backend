#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的数据库创建脚本
"""

import pymysql
import sys

def create_database(password):
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        print("正在连接MySQL服务器...")
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        database_name = 'wecode_sec_tools'
        print(f"正在创建数据库 {database_name}...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"数据库 {database_name} 创建成功！")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"创建数据库失败: {str(e)}")
        print("\n可能的解决方案：")
        print("1. 检查MySQL服务是否正在运行")
        print("2. 检查root用户密码是否正确")
        print("3. 检查root用户是否有创建数据库的权限")
        return False

if __name__ == '__main__':
    print("=== WeCodeSecTools 数据库初始化 ===")
    
    # 询问用户MySQL root密码
    password = input("请输入MySQL root用户密码（如果没有密码请直接回车）: ").strip()
    
    if password:
        # 如果用户输入了密码，先验证密码
        try:
            connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password=password,
                charset='utf8mb4'
            )
            connection.close()
            print("密码验证成功！")
        except Exception as e:
            print(f"密码验证失败: {str(e)}")
            sys.exit(1)
    else:
        password = ''  # 空密码
    
    # 创建数据库
    if create_database(password):
        print("\n数据库初始化完成！")
        print("接下来您可以运行 'python init_db.py' 来创建数据表")
    else:
        print("\n数据库初始化失败，请检查错误信息")
        sys.exit(1)
