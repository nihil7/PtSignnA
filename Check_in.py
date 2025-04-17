import os
import time
import random
from dotenv import load_dotenv
import cloudscraper
from datetime import datetime

# 仅在本地加载 .env 文件，GitHub Actions 中跳过
if not os.getenv("GITHUB_ACTIONS", "").lower() == "true":
    load_dotenv()

# 通用请求头信息
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://www.pttime.org/',
    'Connection': 'keep-alive'
}

# 创建一个 Cloudscraper 对象，用于发送绕过 Cloudflare 的请求
scraper = cloudscraper.create_scraper()

# 构建单个账号的 Cookie 字典
def build_cookie(prefix):
    """
    从环境变量中读取以 prefix 开头的 Cookie 键值对
    """
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

# 打印某账号的 Cookie 信息（用于调试）
def print_cookie_info(name, cookie_dict):
    """
    打印账号名及其对应的 Cookie 信息，缺失项会提示 ❌
    """
    print(f"🍪 {name} cookies:")
    for k, v in cookie_dict.items():
        print(f"  {k} = {v if v else '❌ 缺失'}")

# 校验 Cookie 是否完整
def is_cookie_valid(cookie_dict):
    """
    判断所有 Cookie 是否都存在，如果有缺失则返回 False
    """
    return all(cookie_dict.values())

# 执行签到请求
def check_in(url, cookies, account_name):
    """
    向指定 URL 发送签到请求，打印请求结果和签到时间
    """
    print(f"🚀 正在发送签到请求: {url}")
    try:
        response = scraper.get(url, cookies=cookies, headers=headers, timeout=10)
        print(f"✅ 响应状态码: {response.status_code}")
        print(f"📝 响应内容（前200字）：{response.text[:200]}...")
        if response.status_code == 200:
            print(f"🎉 {account_name} 签到成功")
            # 打印当前签到时间（北京时间）
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"⏰ {account_name} 签到时间: {now}")
        else:
            print(f"❌ {account_name} 签到失败")
    except Exception as e:
        print(f"🚨 {account_name} 请求异常: {str(e)}")

# 主函数
def main():
    """
    程序入口：读取 Cookie，判断有效性，依次对两个账号执行签到
    中间随机等待 0~5 秒，模拟人为操作
    """
    cookies_1 = build_cookie("COOKIE_1")
    cookies_2 = build_cookie("COOKIE_2")

    print_cookie_info("账号 1", cookies_1)
    print_cookie_info("账号 2", cookies_2)

    if is_cookie_valid(cookies_1):
        check_in("https://www.pttime.org/attendance.php?type=sign&uid=2785", cookies_1, "账号 1")
    else:
        print("⚠️ 账号 1 的 Cookie 信息不完整，跳过签到")

    # 在两个签到之间加入 0~5 秒的随机等待时间
    delay = random.uniform(0, 5)
    print(f"⏳ 等待 {delay:.2f} 秒后进行下一个账号签到...")
    time.sleep(delay)

    if is_cookie_valid(cookies_2):
        check_in("https://www.pttime.org/attendance.php?type=sign&uid=20801", cookies_2, "账号 2")
    else:
        print("⚠️ 账号 2 的 Cookie 信息不完整，跳过签到")

if __name__ == "__main__":
    main()
