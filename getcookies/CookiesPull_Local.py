import os
from dotenv import dotenv_values
from github import Github

# ==== 配置 ====
REPO_NAME = "nihil7/GetPtCookies"  # 替换为你的 GitHub 仓库路径

# ==== 加载 .env 文件变量 ====
env_vars = dotenv_values(".env")

# ==== 从系统环境变量中读取 GitHub Token ====
TOKEN = os.getenv("TOKEN") or env_vars.get("TOKEN")

if not TOKEN:
    print("❌ TOKEN 未配置，请设置为系统变量或放入 .env 文件中")
    exit(1)

# ==== 初始化 GitHub 客户端 ====
g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

# ==== 上传 Secrets ====
success = 0
failed = 0

print("🚀 开始上传 Secrets 到 GitHub...")

for key, value in env_vars.items():
    if not value:
        print(f"⚠️ 忽略空值变量：{key}")
        continue
    if key.upper().startswith("GITHUB_"):
        print(f"⚠️ 忽略保留前缀变量：{key}")
        continue
    try:
        repo.create_secret(key, value)
        print(f"✅ 成功设置 GitHub Secret：{key}")
        success += 1
    except Exception as e:
        print(f"❌ 设置 {key} 失败：{e}")
        failed += 1

# ==== 总结 ====
print(f"\n🌟 上传完成：{success} 个成功，{failed} 个失败。")
