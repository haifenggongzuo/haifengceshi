from flask import Flask, render_template, request, jsonify
from supabase import create_client
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz
import hashlib
import json

app = Flask(__name__)

# Supabase配置
url = "https://rwlziuinlbazgoajkcme.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3bHppdWlubGJhemdvYWprY21lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUxODAwNjIsImV4cCI6MjA2MDc1NjA2Mn0.Y1KiIiUXmDiDSFYFQLHmyd1Oe86SxSfvHJcKrJmz2gI"
supabase = create_client(url, key)

# 股票图片映射
STOCK_IMAGES = {
    'AAPL': 'https://logo.clearbit.com/apple.com',
    'MSFT': 'https://logo.clearbit.com/microsoft.com',
    'GOOGL': 'https://logo.clearbit.com/google.com',
    'AMZN': 'https://logo.clearbit.com/amazon.com',
    'META': 'https://logo.clearbit.com/meta.com',
    'TSLA': 'https://logo.clearbit.com/tesla.com',
    'NVDA': 'https://logo.clearbit.com/nvidia.com',
    'JPM': 'https://logo.clearbit.com/jpmorgan.com',
    'V': 'https://logo.clearbit.com/visa.com',
    'WMT': 'https://logo.clearbit.com/walmart.com'
}

def get_real_time_price(symbol):
    """获取实时股票价格"""
    try:
        stock = yf.Ticker(f"{symbol}")
        current_price = stock.info.get('regularMarketPrice')
        if current_price is None:
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
        return float(current_price) if current_price else None
    except Exception as e:
        print(f"Error getting price for {symbol}: {str(e)}")
        return None

def get_device_fingerprint():
    """生成设备指纹"""
    user_agent = request.headers.get('User-Agent', '')
    ip = request.remote_addr
    # 可以添加更多设备特征
    fingerprint_data = f"{ip}:{user_agent}"
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()

def get_next_whatsapp_agent(device_fingerprint):
    """获取下一个可用的WhatsApp客服"""
    try:
        print("开始获取WhatsApp客服")
        print(f"使用设备指纹: {device_fingerprint}")
        
        # 测试数据库连接
        try:
            test_query = supabase.table('whatsapp_agents').select('count').execute()
            print(f"数据库连接测试: {test_query.data}")
        except Exception as db_error:
            print(f"数据库连接测试失败: {str(db_error)}")
            return None
        
        # 检查是否已有分配记录
        try:
            existing_record = supabase.table('contact_records').select('*').eq('device_fingerprint', device_fingerprint).execute()
            print(f"现有记录查询结果: {existing_record.data}")
        except Exception as e:
            print(f"查询现有记录失败: {str(e)}")
            return None
        
        if existing_record.data:
            # 如果已有分配，返回之前分配的客服
            agent_id = existing_record.data[0]['agent_id']
            print(f"找到现有分配的客服ID: {agent_id}")
            try:
                agent = supabase.table('whatsapp_agents').select('*').eq('id', agent_id).execute()
                print(f"获取到现有客服信息: {agent.data}")
                return agent.data[0] if agent.data else None
            except Exception as e:
                print(f"获取现有客服信息失败: {str(e)}")
                return None
        
        # 获取所有客服
        try:
            agents = supabase.table('whatsapp_agents').select('*').eq('is_active', True).execute()
            print(f"可用客服列表查询结果: {agents.data}")
            if not agents.data:
                print("没有找到可用的客服")
                return None
        except Exception as e:
            print(f"获取客服列表失败: {str(e)}")
            return None
            
        # 获取每个客服的当前分配数量
        try:
            assignments = supabase.table('contact_records').select('agent_id, count').execute()
            print(f"客服分配记录查询结果: {assignments.data}")
            assignment_counts = {}
            for record in assignments.data:
                agent_id = record['agent_id']
                assignment_counts[agent_id] = assignment_counts.get(agent_id, 0) + 1
            print(f"客服分配数量统计: {assignment_counts}")
        except Exception as e:
            print(f"获取分配记录失败: {str(e)}")
            assignment_counts = {}
            
        # 选择分配数量最少的客服
        min_assignments = float('inf')
        selected_agent = None
        
        for agent in agents.data:
            count = assignment_counts.get(agent['id'], 0)
            if count < min_assignments:
                min_assignments = count
                selected_agent = agent
        
        print(f"选择的客服: {selected_agent}")
        
        if selected_agent:
            # 记录新的分配
            try:
                insert_data = {
                    'device_fingerprint': device_fingerprint,
                    'agent_id': selected_agent['id'],
                    'ip_address': request.remote_addr,
                    'user_agent': request.headers.get('User-Agent', ''),
                    'timestamp': datetime.now(pytz.UTC).isoformat()
                }
                print(f"准备插入新记录: {insert_data}")
                insert_result = supabase.table('contact_records').insert(insert_data).execute()
                print(f"插入记录结果: {insert_result.data}")
            except Exception as e:
                print(f"插入分配记录失败: {str(e)}")
                # 即使插入失败也返回选中的客服
                
        return selected_agent
        
    except Exception as e:
        print(f"获取WhatsApp客服时发生错误: {str(e)}")
        return None

@app.route('/api/get-whatsapp-link', methods=['GET', 'POST'])
def get_whatsapp_link():
    """获取WhatsApp链接API"""
    try:
        print("\n=== 开始处理WhatsApp链接请求 ===")
        device_fingerprint = get_device_fingerprint()
        print(f"生成的设备指纹: {device_fingerprint}")
        
        # 获取点击时间
        click_time = None
        if request.method == 'POST':
            data = request.get_json()
            click_time = data.get('click_time')
            print(f"记录点击时间: {click_time}")
        
        agent = get_next_whatsapp_agent(device_fingerprint)
        print(f"获取到的客服信息: {agent}")
        
        if agent:
            # 更新点击时间
            if click_time:
                try:
                    update_data = {
                        'click_time': click_time
                    }
                    update_result = supabase.table('contact_records').update(update_data).eq('device_fingerprint', device_fingerprint).execute()
                    print(f"更新点击时间结果: {update_result.data}")
                except Exception as e:
                    print(f"更新点击时间失败: {str(e)}")
            
            app_link = f"whatsapp://send?phone={agent['phone_number']}"
            print(f"生成的WhatsApp链接: {app_link}")
            return {
                'success': True,
                'app_link': app_link
            }
        else:
            print("未能获取到可用的客服")
            return {
                'success': False,
                'message': "暂时无法连接客服，请稍后再试"
            }
            
    except Exception as e:
        print(f"处理WhatsApp链接请求时发生错误: {str(e)}")
        return {
            'success': False,
            'message': "系统错误，请稍后再试"
        }

@app.route('/')
def index():
    try:
        # 获取交易数据
        response = supabase.table('trades').select("*").execute()
        trades = response.data
        
        if not trades:
            print("No trades found in database")
            trades = []
        
        # 为每个交易添加图片URL
        for trade in trades:
            trade['image_url'] = STOCK_IMAGES.get(trade['symbol'], '')
            
            # 如果没有current_price，获取实时价格
            if 'current_price' not in trade or not trade['current_price']:
                current_price = get_real_time_price(trade['symbol'])
                if current_price:
                    trade['current_price'] = current_price
                    trade['current_amount'] = current_price * trade['size']
                    trade['profit_amount'] = trade['current_amount'] - trade['entry_amount']
                    trade['profit_ratio'] = (trade['profit_amount'] / trade['entry_amount']) * 100
        
        # 计算总览数据
        total_trades = len(trades)
        
        # 获取当前持仓
        positions = [t for t in trades if t['status'] == '持有中']
        
        # 计算当月平仓盈亏
        current_month = datetime.now().strftime('%Y-%m')
        monthly_closed_trades = [t for t in trades 
                               if t['status'] in ['以止盈', '以止损'] 
                               and 'exit_date' in t 
                               and t['exit_date'] 
                               and t['exit_date'].startswith(current_month)]
        monthly_profit = sum(t.get('profit_amount', 0) for t in monthly_closed_trades)
        
        # 获取交易员信息
        profile_response = supabase.table('trader_profiles').select("*").limit(1).execute()
        trader_info = profile_response.data[0] if profile_response.data else {
            'trader_name': '专业交易员',
            'professional_title': '股票交易专家 | 技术分析大师',
            'bio': '专注于美股市场的技术分析和量化交易',
            'profile_image_url': 'https://via.placeholder.com/100'
        }
        
        # 添加新的收益指标
        trader_info.update({
            'positions': positions,
            'monthly_profit': round(monthly_profit, 2),  # 本月平仓盈亏
            'active_trades': len(positions),
            'total_profit': round(sum(t.get('profit_amount', 0) for t in trades), 2)  # 总盈亏
        })
        
        return render_template('index.html', 
                            trades=trades,
                            trader_info=trader_info)
    except Exception as e:
        print(f"Error in index route: {e}")
        return render_template('index.html', 
                            trades=[],
                            trader_info={'trader_name': '系统错误', 
                                       'monthly_profit': 0, 
                                       'active_trades': 0})

@app.route('/api/trader-profile', methods=['GET'])
def trader_profile():
    try:
        # 获取个人资料
        response = supabase.table('trader_profiles').select('*').limit(1).execute()
        
        # 获取trades表中的记录数
        trades_response = supabase.table('trades').select('id').execute()
        trades_count = len(trades_response.data) if trades_response.data else 0
        
        if response.data:
            profile = response.data[0]
            # 更新总交易次数 = trader_profiles表中的total_trades + trades表中的记录数
            profile['total_trades'] = profile.get('total_trades', 0) + trades_count
            return jsonify({
                'success': True,
                'data': profile
            })
        else:
            # 如果没有数据，返回默认值，但使用动态计算的总交易次数
            return jsonify({
                'success': True,
                'data': {
                    'trader_name': '专业交易员',
                    'professional_title': '股票交易专家 | 技术分析大师',
                    'years_of_experience': 5,
                    'total_trades': trades_count,  # 使用动态计算的值
                    'win_rate': 85.0
                }
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 