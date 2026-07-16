# PtSuite（PT 站自动签到套件）

原 `PtSignnA`、`GetPtCookies`、`Schedulerupdater` 三个项目的合并仓库。

## 目录结构

| 目录 | 来源 | 作用 |
|------|------|------|
| `checkin/` | PtSignnA | 每日自动签到脚本（PTTIME A/B、1PTBA、PTZONE、BTSCHOOL） |
| `getcookies/` | GetPtCookies | 用 Selenium / cloudscraper 抓取 PT 站 cookie，并上传到本仓库 Secrets |
| `scheduler/` | Schedulerupdater | 【已退役】原用于每天改写 cron 给仓库"保活"，现由 RunDaily 工作流内置保活步骤取代 |

## 工作流

- `.github/workflows/RunDaily.yml` — 每天北京时间约 6 点自动签到；
  末步"保活提交"会在仓库超过 25 天无提交时自动空提交，防止 GitHub 因
  60 天无活动禁用定时任务（`disabled_inactivity`）。
- `.github/workflows/GetCookies.yml` — 手动触发的 cookie 抓取（原 GetPtCookies 的 Run_monthly）。
  注意：`cf_clearance` 与出口 IP / User-Agent 绑定，在本地抓取的值不一定能在 Actions 上通过。

## 密钥

- GitHub Secrets：`PTTIME_A_*`、`PTTIME_B_*`、`PTBA_X1_*`、`PTZONE_X1_*`、`BTSCHOOL_X1_*`（签到用），
  `COOKIE_1_*`、`COOKIE_2_*`、`TOKEN`（抓 cookie / 写 Secrets 用）。
- 本地：各目录下的 `.env` / `.ennv` / `*.pkl`（均已 gitignore，勿提交）。

## Cookie 过期处理

签到返回 403（Cloudflare 拦截）说明对应站点的 `cf_clearance` 过期：
浏览器重新登录该站点，从 DevTools 复制新的 `cf_clearance`，
用 `gh secret set <站点>_CF_CLEARANCE -R nihil7/PtSignnA` 更新。
