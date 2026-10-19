# loon-rules

自用 Loon 插件。订阅地址用 raw 链接。

| 插件 | 订阅地址 | 说明 |
|---|---|---|
| 微博净化[墨鱼版] | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/WeiboEnhanced.plugin` | 由 `Scripts/convert_weibo.py` 从墨鱼原版 QX 配置自动转换，GitHub Actions 每 6 小时同步；脚本直接用原作者地址 `ddgksf2013.top/scripts/weibo_json.js`。需开启 MITM。 |
| Leisu Splash AdBlock | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/Leisu-Splash-AdBlock.plugin` | 雷速开屏广告，无需 MITM。 |

转换来源顺序：先取原作者 `ddgksf2013.top/rewrite/WeiboEnhanced.conf`，取不到时用逐字镜像。上游出现无法转换的行时任务失败、不覆盖现有插件。
