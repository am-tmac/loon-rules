#!/usr/bin/env python3
"""Convert ddgksf2013's QuantumultX WeiboEnhanced.conf into a Loon plugin.

Source order: the author's own URL first; if that host refuses the runner, fall back to a
verbatim mirror of the same file. The generated plugin always points script-path at the
author's original script URL (whatever the conf says), so the logic comes from the author.
Exit code 1 if nothing usable was fetched or parsed, so a broken upstream never overwrites
a working plugin.
"""
import re
import sys
import urllib.request
from pathlib import Path

SOURCES = [
    "https://ddgksf2013.top/rewrite/WeiboEnhanced.conf",
    "https://raw.githubusercontent.com/ifflagged/Romeo/main/Modules/QuantumultX/ddgksf2013/Official/WeiboEnhanced.conf",
]
UA = "Quantumult%20X/1.5.5 (iPhone; iOS 26.0)"
OUT = Path(__file__).resolve().parents[1] / "WeiboEnhanced.plugin"

# QX script type -> (Loon type, needs body)
SCRIPT_TYPES = {
    "script-echo-response": ("http-request", False),
    "script-analyze-echo-response": ("http-request", True),
    "script-request-header": ("http-request", False),
    "script-request-body": ("http-request", True),
    "script-response-header": ("http-response", False),
    "script-response-body": ("http-response", True),
}
REJECTS = {"reject": "reject", "reject-200": "reject-200", "reject-img": "reject-img",
           "reject-dict": "reject-dict", "reject-array": "reject-array", "reject-video": "reject-video"}


def fetch():
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        except Exception as error:  # noqa: BLE001
            print(f"skip {url}: {error}", file=sys.stderr)
            continue
        if "hostname" in text and " url " in text and "<html" not in text.lower():
            print(f"source: {url}", file=sys.stderr)
            return url, text
        print(f"skip {url}: not a QX rewrite file", file=sys.stderr)
    sys.exit("no usable source")


def convert(text):
    meta = dict(re.findall(r"//\s*@(\w+)\s+(.+)", text))
    hosts = re.search(r"^hostname\s*=\s*(.+)$", text, re.M)
    scripts, rewrites, unknown = [], [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("//", "#", ";", "hostname")):
            continue
        m = re.match(r"^(\S+)\s+url\s+(\S+)(?:\s+(\S+))?$", line)
        if not m:
            unknown.append(line)
            continue
        pattern, kind, target = m.groups()
        if kind in SCRIPT_TYPES:
            loon, body = SCRIPT_TYPES[kind]
            script = target
            tag = Path(script.split("?")[0]).stem
            scripts.append(f"{loon} {pattern} script-path={script}"
                           + (", requires-body=true" if body else "") + f", timeout=60, tag={tag}")
        elif kind in REJECTS:
            rewrites.append(f"{pattern} {REJECTS[kind]}")
        elif kind in ("302", "307"):
            rewrites.append(f"{pattern} {kind} {target}")
        else:
            unknown.append(line)
    if unknown:
        sys.exit("unsupported lines, refusing to publish a partial plugin:\n" + "\n".join(unknown))
    if not scripts or not hosts:
        sys.exit("parsed nothing")
    return meta, hosts.group(1).strip(), scripts, rewrites


def main():
    source, text = fetch()
    meta, hosts, scripts, rewrites = convert(text)
    version = meta.get("Version", "?")
    updated = meta.get("UpdateTime", "?")
    lines = [
        "#!name=微博净化[墨鱼版]",
        f"#!desc=墨鱼微博助手 规则 {version}（{updated}）· Loon 自动转换，脚本随原作者更新。设置页：Safari 打开 https://api.weibo.cn/__qx_weibo_settings__/",
        "#!author=@ddgksf2013（原作）",
        "#!homepage=https://ddgksf2013.top/rewrite/WeiboEnhanced.conf",
        "#!icon=https://github.com/Toperlock/Quantumult/raw/main/icon/Doraemon/Doraemon-1063.png",
        "#!tag=去广告",
        f"# 由 Scripts/convert_weibo.py 从 {source} 生成，勿手改",
        "",
    ]
    if rewrites:
        lines += ["[Rewrite]", *rewrites, ""]
    lines += ["[Script]", *scripts, "", "[MITM]", f"hostname = {hosts}", ""]
    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.name}: {len(scripts)} scripts, {len(rewrites)} rewrites, version {version}")


if __name__ == "__main__":
    main()
