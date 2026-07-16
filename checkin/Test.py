import os
from dotenv import load_dotenv
import requests

# 加载 .env 文件
load_dotenv()

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


# 页面 URL
url_1 = 'https://www.pttime.org/index.php'


# 发起请求
response_1 = requests.get(url_1, cookies=cookies_1)


# 检查请求的响应状态
if response_1.status_code == 200:
    print("页面加载成功！")
    # 打印页面内容
    print(response_1.text)  # 打印 HTML 内容
else:
    print(f"页面加载失败，状态码: {response_1.status_code}")
