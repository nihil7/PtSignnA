import os
from dotenv import load_dotenv
import requests

print("🔄 正在加载 .env 文件...")
load_dotenv()

def print_cookie_info(name, cookie_dict):
    print(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        print(f"  {k} = {v if v else '❌ 缺失'}")

# 构建 cookie
cookies_1 = {
    'logged_in': os.getenv('COOKIE_1_logged_in'),
    'cf_clearance': os.getenv('COOKIE_1_cf_clearance'),
    'c_secure_uid': os.getenv('COOKIE_1_c_secure_uid'),
    'c_secure_tracker_ssl': os.getenv('COOKIE_1_c_secure_tracker_ssl'),
    'c_secure_ssl': os.getenv('COOKIE_1_c_secure_ssl'),
    'c_secure_pass': os.getenv('COOKIE_1_c_secure_pass'),
    'c_secure_login': os.getenv('COOKIE_1_c_secure_login'),
    'c_lang_folder': os.getenv('COOKIE_1_c_lang_folder')
}

cookies_2 = {
    'logged_in': os.getenv('COOKIE_2_logged_in'),
    'cf_clearance': os.getenv('COOKIE_2_cf_clearance'),
    'c_secure_uid': os.getenv('COOKIE_2_c_secure_uid'),
    'c_secure_tracker_ssl': os.getenv('COOKIE_2_c_secure_tracker_ssl'),
    'c_secure_ssl': os.getenv('COOKIE_2_c_secure_ssl'),
    'c_secure_pass': os.getenv('COOKIE_2_c_secure_pass'),
    'c_secure_login': os.getenv('COOKIE_2_c_secure_login'),
    'c_lang_folder': os.getenv('COOKIE_2_c_lang_folder')
}

# 模拟浏览器请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.pttime.org/',
    'Connection': 'keep-alive'
}

# 打印 cookie 信息
print_cookie_info("账号1", cookies_1)
print_cookie_info("账号2", cookies_2)

# 封装签到请求函数
def check_in(url, cookies, account_name):
    print(f"🚀 发送请求到: {url}")
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        print(f"✅ 响应状态码: {response.status_code}")
        print(f"📝 响应内容（前200字）：{response.text[:200]}...")
        if response.status_code == 200:
            print(f"🎉 {account_name} 签到成功")
        else:
            print(f"❌ {account_name} 签到失败")
    except Exception as e:
        print(f"🚨 {account_name} 请求异常: {str(e)}")

# 签到
check_in('https://www.pttime.org/attendance.php?type=sign&uid=2785', cookies_1, "账号 1")
check_in('https://www.pttime.org/attendance.php?type=sign&uid=20801', cookies_2, "账号 2")
