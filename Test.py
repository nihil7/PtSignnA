import requests

# 提取的 cookies 字典1
cookies = {
    'logged_in': 'true',
    'cf_clearance': 'evwwjBi0zHtg4phQ20mY5AtHRJeGwksYU8XN80L.inY-1744452269-1.2.1.1-YSnP6oAnIFfeHNrzDdAn6DySIc5YTT767dPXccN3p5l1SYzyensRnmkOCLPHr58KEhjtMmGSrXtlL6lGi3GorDSvAj_30eSvgAgmfoRweEIfJpDzAz.qyz33c_Ex39S2aycDZgVr8TZZU0WLHDRKXdkQHF_klDwAFE3M2Bcj1BQW2Uwt06Hr3ORcD9402XGT6DiMk86lB0Hptn9fzOgGk1_Aa7flO2E4cCSzvMr6Y0Ixhe65IMJttwKvE6B6_76xDpn9b7SMDScxgj7umrXEhGtH7FPXWMIziqZd4q_LzurhV4YZz8fyGWUiIAeRT9lhMKHSmPY22g_5Tqg5wFb_2EMZSDYiZkdvodTPpSgOT3c',
    'c_secure_uid': 'Mjc4NQ%3D%3D',
    'c_secure_tracker_ssl': 'eWVhaA%3D%3D',
    'c_secure_ssl': 'eWVhaA%3D%3D',
    'c_secure_pass': '3b2e7d0a2eefd5e6cd30b2abd289a329',
    'c_secure_login': 'bm9wZQ%3D%3D',
    'c_lang_folder': 'chs'
}

# 访问签到页面1
url = 'https://www.pttime.org/attendance.php?type=sign&uid=2785'


# 提取的 cookies 字典2
cookies = {
    'logged_in': 'true',
    'cf_clearance': 'AoyfbPNEGoMjNSbUnOwsDz5_VA1Xhht8q8tlW4PPCJA-1744453098-1.2.1.1-LMIpRVTdR0QycD0Vm9bX8OhHVG.Oytx7hyoejdF0b5ujnUdxDn2BU9kYB_aHqhBSWkj0YN1Gr9h7wsWujLkIPB9gRmwjR4Q4OmlJPqvMCq4uKrFUcCHwV_NY.PzUN24.t0Y1vmEpU_3HaVxSfJapIatUey4Feok_IrG0ZmQO3ePrbL5DurvbwVedCPlzx7xhJfLrtqYUnQ76bH8CLDnHlY_mxD1p7j8_Zh2lnNa36epUiF76.Gfs2Fh12HfM0BJIlxOrJ..8v56TYAde1uS1dRDCedFmx7ESDVYEbjqGD1sMiNzlPs8t7ZX5ojbighUWKLpjaZVXEBR5e3_K9bORJmXH01oBmtCYOUZbwSMQVnQ',
    'c_secure_uid': 'MjA4MDE%3D',
    'c_secure_tracker_ssl': 'eWVhaA%3D%3D',
    'c_secure_ssl': 'eWVhaA%3D%3D',
    'c_secure_pass': '81d8e46b8765e7a42b7e75aa3be24af4',
    'c_secure_login': 'bm9wZQ%3D%3D',
    'c_lang_folder': 'chs'
}

# 访问签到页面2
url = 'https://www.pttime.org/attendance.php?type=sign&uid=20801'

# 发送 GET 请求
response = requests.get(url, cookies=cookies)

# 检查请求的响应状态
if response.status_code == 200:
    print("页面加载成功！")
    # 打印页面内容
    # print(response.text)  # 打印 HTML 内容
else:
    print(f"页面加载失败，状态码: {response.status_code}")
