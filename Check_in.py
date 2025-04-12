import os
from dotenv import load_dotenv
import requests

print("🔄 正在加载 .env 文件...")
load_dotenv()

def print_cookie_info(name, cookie_dict):
    print(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        print(f"  {k} = {v}")

# 从环境变量中获取 cookies
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

print_cookie_info("账号1", cookies_1)
print_cookie_info("账号2", cookies_2)

# 签到页面 URL
url_1 = 'https://www.pttime.org/attendance.php?type=sign&uid=2785'
url_2 = 'https://www.pttime.org/attendance.php?type=sign&uid=20801'

# 发起签到请求
print(f"🚀 发送请求到: {url_1}")
response_1 = requests.get(url_1, cookies=cookies_1)
print(f"✅ 响应状态码: {response_1.status_code}")
print(f"📝 响应内容（前200字）：{response_1.text[:200]}")

print(f"🚀 发送请求到: {url_2}")
response_2 = requests.get(url_2, cookies=cookies_2)
print(f"✅ 响应状态码: {response_2.status_code}")
print(f"📝 响应内容（前200字）：{response_2.text[:200]}")

# 检查是否签到成功
if response_1.status_code == 200:
    print("🎉 账号 1 签到成功")
else:
    print("❌ 账号 1 签到失败")

if response_2.status_code == 200:
    print("🎉 账号 2 签到成功")
else:
    print("❌ 账号 2 签到失败")
