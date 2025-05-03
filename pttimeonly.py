import os
import time
import random
# from dotenv import load_dotenv
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
    多网站、多账号统一签到入口
    """
    # 统一签到配置：网站名、签到URL、环境变量Cookie前缀
    sites = [
        {
            "name": "PTTime-账号1",
            "url": "https://www.pttime.org/attendance.php?type=sign&uid=2785",
            "cookie_prefix": "COOKIE_1"
        },
        {
            "name": "PTTime-账号2",
            "url": "https://www.pttime.org/attendance.php?type=sign&uid=20801",
            "cookie_prefix": "COOKIE_2"
        },
        # 示例如何添加额外网站
        {
            "name": "OtherSite-账号1",
            "url": "https://www.othersite.com/signin",
            "cookie_prefix": "OTHERSITE_COOKIE_1"
        },
    ]

    for site in sites:
        cookies = build_cookie(site["cookie_prefix"])
        print_cookie_info(site["name"], cookies)

        if is_cookie_valid(cookies):
            check_in(site["url"], cookies, site["name"])
        else:
            print(f"⚠️ {site['name']} 的 Cookie 信息不完整，跳过签到")

        # 每个签到之间加入 0~5 秒的随机等待时间
        delay = random.uniform(0, 5)
        print(f"⏳ 等待 {delay:.2f} 秒后进行下一个签到...")
        time.sleep(delay)


if __name__ == "__main__":
    main()
