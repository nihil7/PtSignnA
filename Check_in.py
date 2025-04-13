import os
from dotenv import load_dotenv
import cloudscraper
import logging

# 加载 .env 文件
load_dotenv()

# 设置日志输出
logging.basicConfig(filename='checkin.log', level=logging.INFO, format='%(asctime)s - %(message)s')
def log(msg):
    print(msg)
    logging.info(msg)

# 通用头信息
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.pttime.org/',
    'Connection': 'keep-alive'
}

scraper = cloudscraper.create_scraper()

def build_cookie(prefix):
    return {
        'logged_in': os.getenv(f'{prefix}_logged_in'),
        'cf_clearance': os.getenv(f'{prefix}_cf_clearance'),
        'c_secure_uid': os.getenv(f'{prefix}_c_secure_uid'),
        'c_secure_tracker_ssl': os.getenv(f'{prefix}_c_secure_tracker_ssl'),
        'c_secure_ssl': os.getenv(f'{prefix}_c_secure_ssl'),
        'c_secure_pass': os.getenv(f'{prefix}_c_secure_pass'),
        'c_secure_login': os.getenv(f'{prefix}_c_secure_login'),
        'c_lang_folder': os.getenv(f'{prefix}_c_lang_folder'),
    }

def print_cookie_info(name, cookie_dict):
    log(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        log(f"  {k} = {v if v else '❌ 缺失'}")

def is_cookie_valid(cookie_dict):
    return all(cookie_dict.values())

def check_in(url, cookies, account_name):
    log(f"🚀 正在发送签到请求: {url}")
    try:
        response = scraper.get(url, cookies=cookies, headers=headers, timeout=10)
        log(f"✅ 响应状态码: {response.status_code}")
        log(f"📝 响应内容（前200字）：{response.text[:200]}...")
        if response.status_code == 200:
            log(f"🎉 {account_name} 签到成功")
        else:
            log(f"❌ {account_name} 签到失败")
    except Exception as e:
        log(f"🚨 {account_name} 请求异常: {str(e)}")

def main():
    cookies_1 = build_cookie("COOKIE_1")
    cookies_2 = build_cookie("COOKIE_2")

    print_cookie_info("账号 1", cookies_1)
    print_cookie_info("账号 2", cookies_2)

    if is_cookie_valid(cookies_1):
        check_in("https://www.pttime.org/index.php", cookies_1, "账号 1")
    else:
        log("⚠️ 账号 1 的 Cookie 信息不完整，跳过签到")

    if is_cookie_valid(cookies_2):
        check_in("https://www.pttime.org/index.php", cookies_2, "账号 2")
    else:
        log("⚠️ 账号 2 的 Cookie 信息不完整，跳过签到")

if __name__ == "__main__":
    main()
