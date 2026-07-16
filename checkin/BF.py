import os
import logging
import cloudscraper
from dotenv import load_dotenv

# 设置日志文件
logging.basicConfig(filename='checkin.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg):
    print(msg)
    logging.info(msg)

def load_env():
    log("🔄 正在加载 .env 文件...")
    load_dotenv()
    if not os.getenv('COOKIE_1_logged_in'):
        log("⚠️ 警告：未成功加载 .env 文件或部分变量缺失，请检查")

def build_cookie(index):
    return {
        'logged_in': os.getenv(f'COOKIE_{index}_logged_in'),
        'cf_clearance': os.getenv(f'COOKIE_{index}_cf_clearance'),
        'c_secure_uid': os.getenv(f'COOKIE_{index}_c_secure_uid'),
        'c_secure_tracker_ssl': os.getenv(f'COOKIE_{index}_c_secure_tracker_ssl'),
        'c_secure_ssl': os.getenv(f'COOKIE_{index}_c_secure_ssl'),
        'c_secure_pass': os.getenv(f'COOKIE_{index}_c_secure_pass'),
        'c_secure_login': os.getenv(f'COOKIE_{index}_c_secure_login'),
        'c_lang_folder': os.getenv(f'COOKIE_{index}_c_lang_folder')
    }

def print_cookie_info(name, cookie_dict):
    log(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        log(f"  {k} = {v if v else '❌ 缺失'}")

def is_cookie_valid(cookie_dict):
    return all(cookie_dict.values())

# 签到请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.pttime.org/',
    'Connection': 'keep-alive'
}

# 创建可以绕过Cloudflare的scraper实例
scraper = cloudscraper.create_scraper()

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
    load_env()

    # 构建两个账号的 cookie
    cookies_1 = build_cookie(1)
    cookies_2 = build_cookie(2)

    print_cookie_info("账号 1", cookies_1)
    print_cookie_info("账号 2", cookies_2)

    if is_cookie_valid(cookies_1):
        check_in('https://www.pttime.org/attendance.php?type=sign&uid=2785', cookies_1, "账号 1")
    else:
        log("⚠️ 账号 1 的 Cookie 信息不完整，跳过签到")

    if is_cookie_valid(cookies_2):
        check_in('https://www.pttime.org/attendance.php?type=sign&uid=20801', cookies_2, "账号 2")
    else:
        log("⚠️ 账号 2 的 Cookie 信息不完整，跳过签到")

if __name__ == "__main__":
    main()
