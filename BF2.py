import logging
import cloudscraper

# 设置日志文件
logging.basicConfig(filename='checkin.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg):
    print(msg)
    logging.info(msg)

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
    # 手动写入两个账号 Cookie 信息
    cookies_1 = {
        'logged_in': 'true',
        'cf_clearance': 'evwwjBi0zHtg4phQ20mY5AtHRJeGwksYU8XN80L.inY-1744452269-1.2.1.1-YSnP6oAnIFfeHNrzDdAn6DySIc5YTT767dPXccN3p5l1SYzyensRnmkOCLPHr58KEhjtMmGSrXtlL6lGi3GorDSvAj_30eSvgAgmfoRweEIfJpDzAz.qyz33c_Ex39S2aycDZgVr8TZZU0WLHDRKXdkQHF_klDwAFE3M2Bcj1BQW2Uwt06Hr3ORcD9402XGT6DiMk86lB0Hptn9fzOgGk1_Aa7flO2E4cCSzvMr6Y0Ixhe65IMJttwKvE6B6_76xDpn9b7SMDScxgj7umrXEhGtH7FPXWMIziqZd4q_LzurhV4YZz8fyGWUiIAeRT9lhMKHSmPY22g_5Tqg5wFb_2EMZSDYiZkdvodTPpSgOT3c',
        'c_secure_uid': 'Mjc4NQ%3D%3D',
        'c_secure_tracker_ssl': 'eWVhaA%3D%3D',
        'c_secure_ssl': 'eWVhaA%3D%3D',
        'c_secure_pass': '3b2e7d0a2eefd5e6cd30b2abd289a329',
        'c_secure_login': 'bm9wZQ%3D%3D',
        'c_lang_folder': 'chs'
    }

    cookies_2 = {
        'logged_in': 'true',
        'cf_clearance': 'AoyfbPNEGoMjNSbUnOwsDz5_VA1Xhht8q8tlW4PPCJA-1744453098-1.2.1.1-LMIpRVTdR0QycD0Vm9bX8OhHVG.Oytx7hyoejdF0b5ujnUdxDn2BU9kYB_aHqhBSWkj0YN1Gr9h7wsWujLkIPB9gRmwjR4Q4OmlJPqvMCq4uKrFUcCHwV_NY.PzUN24.t0Y1vmEpU_3HaVxSfJapIatUey4Feok_IrG0ZmQO3ePrbL5DurvbwVedCPlzx7xhJfLrtqYUnQ76bH8CLDnHlY_mxD1p7j8_Zh2lnNa36epUiF76.Gfs2Fh12HfM0BJIlxOrJ..8v56TYAde1uS1dRDCedFmx7ESDVYEbjqGD1sMiNzlPs8t7ZX5ojbighUWKLpjaZVXEBR5e3_K9bORJmXH01oBmtCYOUZbwSMQVnQ',
        'c_secure_uid': 'MjA4MDE%3D',
        'c_secure_tracker_ssl': 'eWVhaA%3D%3D',
        'c_secure_ssl': 'eWVhaA%3D%3D',
        'c_secure_pass': '81d8e46b8765e7a42b7e75aa3be24af4',
        'c_secure_login': 'bm9wZQ%3D%3D',
        'c_lang_folder': 'chs'
    }

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
