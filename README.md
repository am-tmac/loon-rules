# loon-rules

自用 Loon 插件。订阅地址用 raw 链接。

| 插件 | 订阅地址 | 说明 |
|---|---|---|
| 微博净化[墨鱼版] | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/WeiboEnhanced.plugin` | 由 `Scripts/convert_weibo.py` 从墨鱼原版 QX 配置自动转换，GitHub Actions 每 6 小时同步；脚本直接用原作者地址 `ddgksf2013.top/scripts/weibo_json.js`。需开启 MITM。 |
| Leisu Splash AdBlock | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/Leisu-Splash-AdBlock.plugin` | 雷速开屏广告，无需 MITM。 |
| Swipt Loopback | `https://raw.githubusercontent.com/am-tmac/loon-rules/main/SwiptLoopback.plugin` | 替代 LocalDevVPN：`include-tun 10.7.0.1/32` + `[IP Rewrite] 10.7.0.1 = reflect`，给 Swipt / StikDebug / SideStore 用。需 Loon Build 1007+，启用后断开重连 VPN。无需 MITM。 |

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

## B站 PCDN 拦截

订阅：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/Bili-PCDN-Block.plugin`

拦截 B 站 PCDN/P2P 边缘节点（`*pcdn*.biliapi.net`、`mcdn.bilivideo.cn/.com`、`szbdyd.com`、`mountaintoys.cn`），让播放回落到官方 CDN。规则来源为 X 用户分享，按用户要求封装成独立插件；无脚本、无需 MitM。

注意：PCDN 对部分网络反而更快，拦截后是否变流畅取决于你的线路，建议开启前后各测一段再决定是否保留。

### 两种用法（二选一）

**插件（推荐，含名称/说明）**
```
https://raw.githubusercontent.com/am-tmac/loon-rules/main/Bili-PCDN-Block.plugin
```
Loon → 配置 → 插件 → 添加 → 粘贴上面的 URL。

**远程规则（只要规则本体）**
```
https://raw.githubusercontent.com/am-tmac/loon-rules/main/Bili-PCDN-Block.list
```
Loon → 配置 → 规则 → 添加远程规则 → 粘贴 URL。

## Apple Intelligence / Siri AI 分流

订阅：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/Apple-Intelligence-AI.plugin`

把 Apple Intelligence（Private Cloud Compute：`apple-relay.apple.com`）、Siri（`guzzoni.apple.com`）和 ChatGPT 延伸功能（`chatgpt.com`/`openai.com` 等）的流量强制走代理。只接管这些域名，不碰 iCloud、App Store 等普通 Apple 流量。

**用法**：插件里的策略名 `Proxy` 需换成你自己的节点组名（如「手动切换」「自动选择」），否则规则可能不命中。

**前提**：iOS 的地区限制主要看 **Apple ID 国家/地区**，仅靠网络分流不保证解锁；分流是必要条件之一。若设置里仍提示「此地区无法使用」，需要把 Apple ID 地区切到支持区。

## Quantumult X：Apple 智能分流（国行改 LL/A 方案）

来源：@RZ7Vc 的 Erosion 中文修复版教程第四节。Siri 语音必须直连，PCC、资格校验和 ChatGPT 走美国节点。

- Siri 直连：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/QuantumultX/AppleAI_Direct.list`
- 美国节点：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/QuantumultX/AppleAI_US.list`（强制策略选美国节点）

两条都要拖到所有 Apple 分流规则之前；同时关掉 iRingo/NSRingo 的定位服务和 Siri 模块。

### Quantumult X：Siri AI 全走美国节点（英语 Siri AI / 美版设备）

`https://raw.githubusercontent.com/am-tmac/loon-rules/main/QuantumultX/AppleAI_SiriAI_US.list`

Siri（guzzoni/smoot 等）也走代理。和上面的「Siri 直连」二选一，不要同时启用。

## Loon：Siri AI 全走代理（远程规则）

`https://raw.githubusercontent.com/am-tmac/loon-rules/main/SiriAI-US.list`

Loon → 配置 → 规则 → 添加远程规则，策略选你的节点组，拖到所有 Apple 规则之前。与 Apple-Intelligence-AI / Apple-AI-Full 内容重叠，只开一个。

## 拒绝 QUIC（Loon 插件）

订阅：`https://raw.githubusercontent.com/am-tmac/loon-rules/main/No-QUIC.plugin`

规则只有一条 `PROTOCOL,QUIC,REJECT`。作用是让 UDP/443 的 QUIC 回落 TCP：

- 避免 QUIC 绕过分流规则（有些客户端对 QUIC 的规则匹配不完整，容易出现「明明设了规则却直连」）
- 避免 UDP 443 被运营商 QoS 时出现卡顿、测速异常
- 代价：极少数纯 QUIC 服务会稍慢，浏览器会自动回落，一般无感

需不需要取决于你的线路：UDP 稳定的话收益有限；UDP 被限速或经常卡顿时收益明显。
