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

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# Supabase配置
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

@app.route('/')
def index():
    try:
        # 获取交易数据
        response = supabase.table('trades').select("*").execute()
        trades = response.data
        
        if not trades:
            print("No trades found in database")
            trades = []
            
        return render_template('index.html', 
                             trades=trades,
                             trader_info={
                                 'trader_name': '专业交易员',
                                 'professional_title': '股票交易专家',
                                 'monthly_profit': 50000,
                                 'active_trades': 5,
                                 'total_profit': 3000000
                             })
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', 
                             trades=[],
                             trader_info={'trader_name': '系统错误'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 