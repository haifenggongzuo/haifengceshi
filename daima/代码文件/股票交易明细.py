import pandas as pd
from supabase import create_client
import os
import sys

print("程序开始运行...")
sys.stdout.flush()

try:
    # 直接设置环境变量
    url = "https://rwlziuinlbazgoajkcme.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3bHppdWlubGJhemdvYWprY21lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUxODAwNjIsImV4cCI6MjA2MDc1NjA2Mn0.Y1KiIiUXmDiDSFYFQLHmyd1Oe86SxSfvHJcKrJmz2gI"
    
    print(f"配置信息:")
    print(f"URL: {url}")
    print(f"KEY: {key}")
    sys.stdout.flush()
    
    # 连接到 Supabase
    print("正在连接到Supabase...")
    sys.stdout.flush()
    supabase = create_client(url, key)
    print("连接成功！")
    sys.stdout.flush()
    
    # 获取所有交易记录
    print("正在获取交易记录...")
    sys.stdout.flush()
    response = supabase.table('trades').select("*").execute()
    print(f"获取到响应: {response}")
    sys.stdout.flush()
    
    # 转换为DataFrame并显示
    df = pd.DataFrame(response.data)
    print(f"DataFrame信息: {len(df)} 行")
    sys.stdout.flush()
    
    if len(df) > 0:
        print("\n所有交易记录：")
        print(df)
        sys.stdout.flush()
    else:
        print("没有找到任何交易记录")
        sys.stdout.flush()
        
except Exception as e:
    print(f"发生错误: {str(e)}")
    print("错误详情:")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()

print("程序运行结束")
sys.stdout.flush()
