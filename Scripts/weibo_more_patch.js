// 微博「我」页面：隐藏「更多功能」模块（免流量服务 / 我的钱包 / 经常访问 …）。
// 补丁：墨鱼微博助手只按 itemId "100505_-_manage" 隐藏，新版微博该卡片为 "100505_-_manage2"
// 或其它 itemId，开关不生效。本脚本在墨鱼脚本之后运行，只删这一个模块，其他内容不动。
// 规则：http-response ^https?://api\.weibo\.cn/2/profile/me(?=[?#]|$) requires-body=true
const MORE_IDS = new Set(["100505_-_manage", "100505_-_manage2"]);

function titleOf(item) {
  const h = item && item.header;
  const t = h && (h.title || (h.data && h.data.title));
  if (!t) return "";
  return typeof t === "string" ? t : (t.content || t.text || "");
}

function isMore(item) {
  if (!item || typeof item !== "object") return false;
  if (MORE_IDS.has(item.itemId)) return true;
  return titleOf(item).trim() === "更多功能";
}

function clean(body) {
  let obj;
  try { obj = JSON.parse(body); } catch (e) { return null; }
  if (!obj || !Array.isArray(obj.items)) return null;
  const before = obj.items.length;
  obj.items = obj.items.filter((item) => !isMore(item));
  return obj.items.length === before ? null : JSON.stringify(obj);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { clean, isMore };
} else {
  const out = clean($response.body);
  $done(out ? { body: out } : {});
}
