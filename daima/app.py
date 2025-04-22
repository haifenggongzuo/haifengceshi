from flask import Flask, render_template, request, jsonify
from supabase import create_client
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz
import hashlib
import json
import os
from dotenv import load_dotenv
from config import config

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config.from_object(config['default'])

# Supabase配置
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

# 初始化后台管理
from admin import init_admin
app = init_admin(app)

# ... existing code ...

if __name__ == '__main__':
    # 生产环境配置
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 