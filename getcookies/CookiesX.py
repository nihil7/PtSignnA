import pickle
import os

# ==== 配置 ====
COOKIES_PATH_1 = "cookies_1.pkl"  # 第一个 cookies 文件路径
COOKIES_PATH_2 = "cookies_2.pkl"  # 第二个 cookies 文件路径


# ==== 读取 cookies 并格式化 ====
def load_cookies_from_file(cookies_path):
    """从文件加载 cookies"""
    if os.path.exists(cookies_path):
        with open(cookies_path, "rb") as cookiesfile:
            cookies = pickle.load(cookiesfile)
            return cookies
    else:
        print(f"❌ 未找到 {cookies_path} 文件")
        return None

def format_cookies(cookies, prefix):
    """格式化 cookies 为指定格式"""
    formatted_cookies = {}
    if isinstance(cookies, list):  # 检查是否为列表类型
        for cookie in cookies:
            if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:  # 确保每个元素是字典并含有 name 和 value
                name = cookie['name']
                value = cookie['value']
                formatted_cookies[f"{prefix}_{name}"] = value
    return formatted_cookies

# 加载 cookies
cookies_1 = load_cookies_from_file(COOKIES_PATH_1)
cookies_2 = load_cookies_from_file(COOKIES_PATH_2)

if cookies_1 is None or cookies_2 is None:
    exit(1)

# 格式化 cookies
formatted_cookies_1 = format_cookies(cookies_1, "COOKIE_1")
formatted_cookies_2 = format_cookies(cookies_2, "COOKIE_2")

# 保存到 .env 文件
env_file_path = ".ennv"
with open(env_file_path, "a") as env_file:
    for key, value in formatted_cookies_1.items():
        env_file.write(f"{key}={value}\n")
    for key, value in formatted_cookies_2.items():
        env_file.write(f"{key}={value}\n")

print(f"✅ Cookies 已保存到 {env_file_path} 文件")

