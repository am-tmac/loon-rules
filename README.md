# loon-rules

自用 Loon 插件。订阅地址用 raw 链接。

| 插件 | 订阅地址 | 说明 |
|---|---|---|
| 微博净化[墨鱼版] | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/WeiboEnhanced.plugin` | 由 `Scripts/convert_weibo.py` 从墨鱼原版 QX 配置自动转换，GitHub Actions 每 6 小时同步；脚本直接用原作者地址 `ddgksf2013.top/scripts/weibo_json.js`。需开启 MITM。 |
| Leisu Splash AdBlock | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/Leisu-Splash-AdBlock.plugin` | 雷速开屏广告，无需 MITM。 |

转换来源顺序：先取原作者 `ddgksf2013.top/rewrite/WeiboEnhanced.conf`，取不到时用逐字镜像。上游出现无法转换的行时任务失败、不覆盖现有插件。


## 腾讯 App 净化（原作 @ZenmoFeiShi）

- 腾讯体育：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/txsports-ad-clean.plugin`

来源：https://github.com/ZenmoFeiShi/Qx （对应同名 snippet 与 JS）。保留原作逻辑，适配 QX bodyBytes 到 Loon binary-body-mode / Uint8Array，并解码文本分支；体育共享域名仍由脚本检查 QQSportsV3 User-Agent。
需要启用脚本、MitM 并安装信任证书。不要同时启用同接口的其他净化插件。脚本为本仓库快照，不自动跟随上游；源仓库未确认授权许可，不添加其他许可证声明。
已进行 Node 语法、模拟二进制文本响应、UA隔离及异常数据透传测试；未在真实 iOS Loon / 腾讯 App 上验证广告效果。不承诺去除所有播放广告或解锁会员。


## 雷速广告拦截（扩展版）

订阅：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/Leisu-AdBlock-Extended.plugin`

依据用户提供清单封装，包含33条域名规则与1条 `https://cdn.leisu.com/app-ad/` 路径拦截。共享广告SDK域名规则是全局的，可能影响其他App广告、激励视频和相关功能；不是精确的雷速专属策略。原 `Leisu-Splash-AdBlock.plugin` 精简版保留，建议择一使用。

域名拦截无需解密；路径拦截需要打开MitM、安装并信任证书，仅添加 `cdn.leisu.com`，不封整个CDN。未添加无请求证据的业务网关路径。无脚本、无IPA修改、无会员解锁。配置是静态快照，无自动更新上游。已进行结构/规则计数/路径正反例检查与远端字节验证，未进行真实iOS Loon或雷速App测试；来源清单的Android分析及iOS覆盖声明未独立验证。
