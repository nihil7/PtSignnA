import os
import time
import random
import cloudscraper
from datetime import datetime
# from dotenv import load_dotenv

# === 加载本地 .env（GitHub Actions 中跳过）===
if not os.getenv("GITHUB_ACTIONS", "").lower() == "true":
    load_dotenv()

# === 通用请求头 ===
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0",
    "Referer": "https://pt.btschool.club/index.php",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
}


# === 创建 Cloudscraper 请求对象 ===
scraper = cloudscraper.create_scraper()

# === 每个账号一条配置 ===
ACCOUNTS = [
    {
        "site": "PTTIME",
        "account": "A",
        "url": "https://www.pttime.org/attendance.php?type=sign&uid=2785"
    },
    {
        "site": "PTTIME",
        "account": "B",
        "url": "https://www.pttime.org/attendance.php?type=sign&uid=20801"
    },
    {
        "site": "PTBA",
        "account": "X1",
        "url": "https://1ptba.com/attendance.php"
    },
    {
        "site": "PTZONE",
        "account": "X1",
        "url": "https://ptzone.xyz/attendance.php"
    },
    {
        "site": "BTSCHOOL",
        "account": "X1",
        "url": "https://pt.btschool.club/index.php?action=addbonus"
    }
]

# === 构造 Cookie ===
def build_cookie(site, account):
    prefix = f"{site}_{account}".upper()
    return {
        'logged_in': os.getenv(f'{prefix}_LOGGED_IN'),
        'cf_clearance': os.getenv(f'{prefix}_CF_CLEARANCE'),
        'c_secure_uid': os.getenv(f'{prefix}_C_SECURE_UID'),
        'c_secure_tracker_ssl': os.getenv(f'{prefix}_C_SECURE_TRACKER_SSL'),
        'c_secure_ssl': os.getenv(f'{prefix}_C_SECURE_SSL'),
        'c_secure_pass': os.getenv(f'{prefix}_C_SECURE_PASS'),
        'c_secure_login': os.getenv(f'{prefix}_C_SECURE_LOGIN'),
        'c_lang_folder': os.getenv(f'{prefix}_C_LANG_FOLDER'),
    }

# === 校验 Cookie ===
def is_cookie_valid(cookie_dict):
    """
    只验证关键字段，不强制要求 cf_clearance
    """
    required = [
        'logged_in',
        'c_secure_uid',
        'c_secure_pass',
        'c_secure_ssl',
        'c_secure_tracker_ssl',
        'c_secure_login'
    ]
    return all(cookie_dict.get(k) for k in required)



# === 打印 Cookie（调试用）===
def print_cookie_info(name, cookie_dict):
    print(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        print(f"  {k} = {v if v else '❌ 缺失'}")

# === 执行签到 ===
def check_in(url, cookies, site, account):
    print(f"🚀 正在签到 [{site} - {account}]: {url}")
    try:
        response = scraper.get(url, cookies=cookies, headers=headers, timeout=10)
        print(f"✅ 状态码: {response.status_code}")
        print(f"📄 内容（前200字）: {response.text[:200]}...")
        if response.status_code == 200:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🎉 成功签到：{site} - {account} @ {now}")
        else:
            print(f"❌ 签到失败：{site} - {account}")
    except Exception as e:
        print(f"🚨 异常：{site} - {account} - {str(e)}")

# === 主函数 ===
def main():
    for conf in ACCOUNTS:
        site = conf["site"]
        account = conf["account"]
        url = conf["url"]

        cookie = build_cookie(site, account)
        print_cookie_info(f"{site}-{account}", cookie)

        if not is_cookie_valid(cookie):
            print(f"⚠️ 跳过：{site} - {account}，Cookie 信息不完整")
            continue

        check_in(url, cookie, site, account)

        delay = random.uniform(0, 5)
        print(f"⏳ 等待 {delay:.2f} 秒...\n")
        time.sleep(delay)

if __name__ == "__main__":
    main()
