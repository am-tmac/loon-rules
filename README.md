# loon-rules

自用 Loon 插件。订阅地址用 raw 链接。

| 插件 | 订阅地址 | 说明 |
|---|---|---|
| 微博净化[墨鱼版] | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/WeiboEnhanced.plugin` | 由 `Scripts/convert_weibo.py` 从墨鱼原版 QX 配置自动转换，GitHub Actions 每 6 小时同步；脚本直接用原作者地址 `ddgksf2013.top/scripts/weibo_json.js`。需开启 MITM。 |
| Leisu Splash AdBlock | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/Leisu-Splash-AdBlock.plugin` | 雷速开屏广告，无需 MITM。 |

转换来源顺序：先取原作者 `ddgksf2013.top/rewrite/WeiboEnhanced.conf`，取不到时用逐字镜像。上游出现无法转换的行时任务失败、不覆盖现有插件。


## 腾讯 App 净化（原作 @ZenmoFeiShi）

- 腾讯体育：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/txsports-ad-clean.plugin`
- 腾讯视频：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/TxvideoAD.plugin`

来源：https://github.com/ZenmoFeiShi/Qx （对应同名 snippet 与 JS）。保留原作逻辑，适配 QX bodyBytes 到 Loon binary-body-mode / Uint8Array，并解码文本分支；体育共享域名仍由脚本检查 QQSportsV3 User-Agent。
需要启用脚本、MitM 并安装信任证书。不要同时启用同接口的其他净化插件。脚本为本仓库快照，不自动跟随上游；源仓库未确认授权许可，不添加其他许可证声明。
已进行 Node 语法、模拟二进制文本响应、UA隔离及异常数据透传测试；未在真实 iOS Loon / 腾讯 App 上验证广告效果。不承诺去除所有播放广告或解锁会员。
