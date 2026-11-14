#!/usr/bin/env python3
"""Sync ZenmoFeiShi's QX txsports-ad-clean (snippet + JS) into a Loon plugin.

- Fetches the author's snippet and JS from GitHub.
- Drops the live-match rules (m/match/liveSum, match/multiUpdate): they blank live
  score/state data and make live streams stall.
- Applies the Loon body adapter to the JS (QX bodyBytes -> Loon binary-body-mode).
  Every adapter replacement must match exactly once; otherwise exit 1 and leave the
  existing files untouched, so an upstream rewrite never ships a half-adapted script.
"""
import re
import sys
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/ZenmoFeiShi/Qx/refs/heads/main/"
SNIPPET = BASE + "txsports-ad-clean.snippet"
SCRIPT = BASE + "txsports-ad-clean.js"
ROOT = Path(__file__).resolve().parents[1]
OUT_PLUGIN = ROOT / "txsports-ad-clean.plugin"
OUT_JS = ROOT / "Scripts" / "txsports-ad-clean.js"
JS_URL = "https://raw.githubusercontent.com/am-tmac/loon-rules/main/Scripts/txsports-ad-clean.js"

# Rules removed on purpose (match on the path part of the pattern).
DROP = ("m\\/match\\/liveSum", "match\\/multiUpdate")

HEADER_JS = r'''// Original: @ZenmoFeiShi; Loon body adapter: am-tmac.
// Upstream: https://github.com/ZenmoFeiShi/Qx (auto-synced)
function loonText(x) {
  if (typeof x === "string") return x;
  if (!x) return "";
  var b = x instanceof ArrayBuffer ? new Uint8Array(x) : x;
  var s=""; for(var i=0;i<b.length;i++) s+=String.fromCharCode(b[i]);
  try { return decodeURIComponent(escape(s)); } catch(e) { return s; }
}
var loonDone = $done;
$done = function(o) {
  if(o && o.body instanceof ArrayBuffer) o.body = new Uint8Array(o.body);
  loonDone(o);
};
'''

# (old, new, expected count)
JS_PATCHES = [
    ("raw = $response.body;", "raw = loonText($response.body);", 1),
    ("var raw = $request.body,", "var raw = loonText($request.body),", 1),
    ("var raw = $response.body,", "var raw = loonText($response.body),", 1),
    ("$response.statusCode && $response.statusCode !== 200",
     "$response.status && $response.status !== 200", 1),
    ("raw = $response.bodyBytes;", "raw = $response.body;", 1),
    ("{ bodyBytes: tsqxJoin(chunks).buffer }", "{ body: tsqxJoin(chunks).buffer }", 1),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Quantumult%20X/1.5.5"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def adapt_js(js):
    for old, new, n in JS_PATCHES:
        c = js.count(old)
        if c != n:
            sys.exit(f"JS patch mismatch ({c}x, want {n}): {old}")
        js = js.replace(old, new)
    if "bodyBytes" in js:
        sys.exit("JS still references bodyBytes after adapting")
    return HEADER_JS + js


def convert(snippet):
    meta = dict(re.findall(r"^#!(\w+)\s*=\s*(.+)$", snippet, re.M))
    hosts = re.search(r"^hostname\s*=\s*(.+)$", snippet, re.M)
    if not hosts:
        sys.exit("no hostname line")
    rules, dropped, unknown = [], [], []
    for line in snippet.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "//", ";", "hostname")):
            continue
        m = re.match(r"^(\^\S+)\s+(?:.*\s)?(url|url-and-header)\s+script-response-body\s+(\S+)$", line)
        if not m:
            unknown.append(line)
            continue
        pattern = m.group(1)
        if any(d in pattern for d in DROP):
            dropped.append(pattern)
            continue
        rules.append(
            f"http-response {pattern} script-path={JS_URL}, requires-body=true, "
            f"binary-body-mode=true, timeout=10, tag=txsports-ad-clean"
        )
    if unknown:
        sys.exit("unrecognised snippet lines:\n" + "\n".join(unknown))
    if not rules:
        sys.exit("no rules parsed")
    if len(dropped) != len(DROP):
        print(f"warning: dropped {len(dropped)} of {len(DROP)} live rules", file=sys.stderr)
    host_list = ", ".join(h.strip() for h in hosts.group(1).split(",") if h.strip())
    out = [
        "#!name=腾讯体育净化（Loon）",
        "#!desc=原作者 ZenmoFeiShi，自动同步上游；已移除直播比分接口（liveSum / multiUpdate）以免直播卡顿。需启用 MitM 并信任证书。",
        "#!author=@ZenmoFeiShi / am-tmac（Loon适配）",
        "#!homepage=https://github.com/ZenmoFeiShi/Qx",
        f"#!upstream_update={meta.get('update', '?')}",
        "",
        "[Script]",
        *rules,
        "",
        "[Mitm]",
        f"hostname = {host_list}",
        "",
    ]
    return "\n".join(out), dropped


def main():
    snippet = get(SNIPPET)
    js = get(SCRIPT)
    if "<html" in snippet.lower() or "$done" not in js:
        sys.exit("upstream fetch returned something unexpected")
    plugin, dropped = convert(snippet)
    adapted = adapt_js(js)
    OUT_PLUGIN.write_text(plugin, encoding="utf-8")
    OUT_JS.write_text(adapted, encoding="utf-8")
    print(f"rules={plugin.count('http-response ')} dropped={len(dropped)}", file=sys.stderr)


if __name__ == "__main__":
    main()
