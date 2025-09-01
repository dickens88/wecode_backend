#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import os
import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """加载YAML配置文件"""
        config_path = Path(__file__).parent.parent / 'resources' / 'config.yml'
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
                self._parse_config(config_data)
        else:
            # 如果配置文件不存在，使用默认配置
            self._set_defaults()
    
    def _parse_config(self, config_data):
        """解析配置文件数据"""
        # Flask配置
        flask_config = config_data.get('flask', {})
        self.SECRET_KEY = self._get_env_value('SECRET_KEY', flask_config.get('secret_key', 'dev-secret-key'))
        self.FLASK_HOST = flask_config.get('host', '0.0.0.0')
        self.FLASK_PORT = flask_config.get('port', 5000)
        self.FLASK_DEBUG = flask_config.get('debug', False)
        
        # 数据库配置
        db_config = config_data.get('database', {})
        mysql_config = db_config.get('mysql', {})
        self.MYSQL_HOST = self._get_env_value('MYSQL_HOST', mysql_config.get('host', 'localhost'))
        self.MYSQL_PORT = int(self._get_env_value('MYSQL_PORT', mysql_config.get('port', 3306)))
        self.MYSQL_USER = self._get_env_value('MYSQL_USER', mysql_config.get('user', 'root'))
        self.MYSQL_PASSWORD = self._get_env_value('MYSQL_PASSWORD', mysql_config.get('password', 'password'))
        self.MYSQL_DATABASE = self._get_env_value('MYSQL_DATABASE', mysql_config.get('database', 'wecode_sec_tools'))
        
        # SQLAlchemy配置
        self.SQLALCHEMY_TRACK_MODIFICATIONS = db_config.get('sqlalchemy', {}).get('track_modifications', False)
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}'
        
        # 第三方API配置
        api_config = config_data.get('third_party_api', {})
        self.THIRD_PARTY_API_BASE_URL = self._get_env_value('THIRD_PARTY_API_BASE_URL', api_config.get('base_url', 'https://api.example.com'))
        self.THIRD_PARTY_API_KEY = self._get_env_value('THIRD_PARTY_API_KEY', api_config.get('api_key', 'your-api-key'))
        
        # 定时任务配置
        scheduler_config = config_data.get('scheduler', {})
        self.SCHEDULER_INTERVAL = scheduler_config.get('interval', 10)
        
        # 日志配置
        logging_config = config_data.get('logging', {})
        self.LOG_LEVEL = self._get_env_value('LOG_LEVEL', logging_config.get('level', 'INFO'))
        self.LOG_DIR = self._get_env_value('LOG_DIR', logging_config.get('dir', 'logs'))
        self.LOG_FILE = self._get_env_value('LOG_FILE', logging_config.get('file', 'wecode_sec_tools.log'))
        self.LOG_MAX_BYTES = self._get_env_value('LOG_MAX_BYTES', logging_config.get('max_bytes', 10*1024*1024))  # 10MB
        self.LOG_BACKUP_COUNT = self._get_env_value('LOG_BACKUP_COUNT', logging_config.get('backup_count', 5))
    
    def _set_defaults(self):
        """设置默认配置"""
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
        self.FLASK_HOST = '0.0.0.0'
        self.FLASK_PORT = 5000
        self.FLASK_DEBUG = False
        
        self.MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        self.MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
        self.MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        self.MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
        self.MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'wecode_sec_tools')
        
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}'
        
        self.THIRD_PARTY_API_BASE_URL = os.environ.get('THIRD_PARTY_API_BASE_URL', 'https://api.example.com')
        self.THIRD_PARTY_API_KEY = os.environ.get('THIRD_PARTY_API_KEY', 'your-api-key')
        
        self.SCHEDULER_INTERVAL = 10
        
        # 日志默认配置
        self.LOG_LEVEL = 'INFO'
        self.LOG_DIR = 'logs'
        self.LOG_FILE = 'wecode_sec_tools.log'
        self.LOG_MAX_BYTES = 10*1024*1024  # 10MB
        self.LOG_BACKUP_COUNT = 5
    
    def _get_env_value(self, env_key, default_value):
        """获取环境变量值，支持${ENV_VAR:-default}格式"""
        if isinstance(default_value, str) and default_value.startswith('${') and ':-' in default_value:
            # 解析 ${ENV_VAR:-default} 格式
            env_var = default_value[2:].split(':-')[0]
            fallback = default_value.split(':-')[1].rstrip('}')
            return os.environ.get(env_var, fallback)
        elif isinstance(default_value, str) and default_value.startswith('${') and default_value.endswith('}'):
            # 解析 ${ENV_VAR} 格式
            env_var = default_value[2:-1]
            return os.environ.get(env_var, default_value)
        else:
            return default_value
