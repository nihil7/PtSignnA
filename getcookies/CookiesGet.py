import os
import time
import random
import re
import platform
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import cloudscraper  # 引入 cloudscraper 库

# 尝试加载 .env 文件（如果存在）
load_dotenv()  # 无论 .env 是否存在，都会尝试加载

# 从环境变量中获取 cookies 信息（如果有）
cookies = {
    'c_secure_ssl': os.getenv('COOKIE_1_c_secure_ssl'),
    'c_secure_pass': os.getenv('COOKIE_1_c_secure_pass'),
    'logged_in': os.getenv('COOKIE_1_logged_in'),
    'c_secure_uid': os.getenv('COOKIE_1_c_secure_uid'),
    'c_secure_login': os.getenv('COOKIE_1_c_secure_login'),
    'c_secure_tracker_ssl': os.getenv('COOKIE_1_c_secure_tracker_ssl'),
    'cf_clearance': os.getenv('COOKIE_1_cf_clearance'),
    'c_lang_folder': os.getenv('COOKIE_1_c_lang_folder')
}

# 打印 cookies（确认加载），每个 cookie 的值只显示前一半内容
print("📦 当前加载的 cookies：")
for name, value in cookies.items():
    print(f"{name}: {value[:len(value) // 3]}")  # 打印每个 cookie 的前一半字符

# 设置 Chrome 浏览器选项
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 启用无头模式（不显示浏览器界面）
options.add_argument("--no-sandbox")  # 解决部分 Linux 系统的权限问题
options.add_argument("--disable-dev-shm-usage")  # 解决内存共享问题
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.52-1 Safari/537.36")  # 设置用户代理

# 判断操作系统类型
IS_LINUX = platform.system() == "Linux"
if IS_LINUX:
    print("当前操作系统：Linux")
    service = Service(ChromeDriverManager().install())
else:
    print("当前操作系统：Windows")
    LOCAL_CHROMEDRIVER_PATH = r"C:\Users\ishel\Desktop\编程总库\chrome\chromedriver-win64\chromedriver.exe"
    service = Service(LOCAL_CHROMEDRIVER_PATH)

# 启动浏览器
try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"❌ 无法启动 Chrome WebDriver: {e}")
    exit(1)


# 函数：模拟用户操作
def simulate_user_actions(driver):
    """
    模拟用户滚动页面，增加页面的活跃度
    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))  # 随机延时，模拟人类操作


# 函数：加载 Cookies
def load_cookies(driver, cookies_dict):
    """
    将从 .env 文件读取的 Cookies 加载到浏览器会话中
    """
    for name, value in cookies_dict.items():
        driver.add_cookie({'name': name, 'value': value, 'domain': '.pttime.org'})  # 注意添加正确的域名


# 函数：获取页面内容并打印中文信息
def fetch_page_content(driver, url):
    """
    访问指定的 URL，获取页面内容，并打印前 200 个汉字
    """
    print(f"正在访问 URL: {url}")
    try:
        # 访问目标 URL
        driver.get(url)
        print("🔄 页面加载开始...")
        time.sleep(5)  # 等待页面加载完成

        # 获取页面源码
        page_source = driver.page_source

        # 打印页面的一部分源码，检查是否正确加载
        print("🔍 页面源码加载完成，开始分析页面内容...")
        print("页面源码的一部分：")
        print(page_source[:2000])  # 打印前500个字符的源码，防止页面过长

        # 提取中文内容
        chinese_content = "".join(re.findall(r'[\u4e00-\u9fff]+', page_source))
        print(f"📄 页面前200个汉字内容：{chinese_content[:200]}")

        # 检查是否包含“收藏”字样
        if "收藏" in chinese_content:
            print("✅ 登录成功 - 页面包含 '收藏' 关键词")
        else:
            print("⚠️ 登录失败 - 页面不包含 '收藏' 关键词")

        # 获取当前页面的 cookies
        cookies = driver.get_cookies()

        # 打印 cookies 信息，帮助分析 cookies 是否正确加载
        print("📦 当前页面 cookies：")
        if not cookies:
            print("⚠️ 没有获取到 cookies，请检查是否被拦截或者是否登录成功。")
        else:
            for i, cookie in enumerate(cookies, start=1):
                cookie_name = cookie['name']
                cookie_value = cookie['value']
                print(f"COOKIE_{i}_{cookie_name}: {cookie_value[:100]}")  # 只显示前100个字符

        # 打印页面标题和 URL，进一步确认页面是否加载正确
        print(f"📑 页面标题：{driver.title}")
        print(f"🌐 当前页面 URL：{driver.current_url}")

    except Exception as e:
        print(f"❌ 访问 URL 时发生错误: {e}")


# 使用 cloudscraper 获取有效的 cookies
def get_valid_cookies(url):
    """
    使用 cloudscraper 获取有效的 cookies，并用 .env 中的 cookies 登录
    """
    scraper = cloudscraper.create_scraper()

    # 通过 cloudscraper 获取页面，并携带 .env 中的 cookies
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.52-1 Safari/537.36"
    }

    # 设置 cookies（从 .env 加载的）
    cookies = {
        'c_secure_ssl': os.getenv('COOKIE_1_c_secure_ssl'),
        'c_secure_pass': os.getenv('COOKIE_1_c_secure_pass'),
        'logged_in': os.getenv('COOKIE_1_logged_in'),
        'c_secure_uid': os.getenv('COOKIE_1_c_secure_uid'),
        'c_secure_login': os.getenv('COOKIE_1_c_secure_login'),
        'c_secure_tracker_ssl': os.getenv('COOKIE_1_c_secure_tracker_ssl'),
        'cf_clearance': os.getenv('COOKIE_1_cf_clearance'),
        'c_lang_folder': os.getenv('COOKIE_1_c_lang_folder')
    }

    # 发起请求，带上 cookies
    response = scraper.get(url, headers=headers, cookies=cookies)

    # 返回 cookies 字典
    return response.cookies.get_dict()


if __name__ == "__main__":
    target_url = "https://www.pttime.org/index.php"

    # 使用 cloudscraper 获取有效的 cookies（用 .env 中的 cookies 登录）
    valid_cookies = get_valid_cookies(target_url)

    # 打印获取到的 cookies（方便调试）
    print("📦 获取到的有效 cookies：")
    for name, value in valid_cookies.items():
        print(f"{name}: {value[:len(value) // 3]}")  # 打印每个 cookie 的前一半字符

    # 启动浏览器并加载 cookies
    driver.get(target_url)  # 首先打开页面
    load_cookies(driver, valid_cookies)  # 加载有效 cookies
    driver.refresh()  # 刷新页面，模拟登录状态

    # 访问目标页面并打印反馈内容
    fetch_page_content(driver, target_url)

    driver.quit()
