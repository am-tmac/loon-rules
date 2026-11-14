#!/usr/bin/env python3
"""Sync RavelloH's QX block_check.js (节点阻断检测) into a Loon generic script.

QX-only APIs are bridged by a small prelude:
- $environment.params (QX: node name string)  -> Loon $environment.params.node
- $configuration.sendMessage(get_server_description) -> Loon nodeInfo.address/port
- $task.fetch (QX, promise)                   -> Loon $httpClient (callback), opts.policy -> node
Every textual replacement must match the expected count, otherwise exit 1 and leave the
existing file untouched, so an upstream rewrite never ships a half-adapted script.
"""
import sys
import urllib.request
from pathlib import Path

SRC = "https://gist.githubusercontent.com/RavelloH/383354955aa3800e1d7e98666e11e16f/raw/block_check.js"
OUT = Path(__file__).resolve().parents[1] / "Scripts" / "block_check.js"

PRELUDE = r'''// Original: RavelloH (https://github.com/RavelloH), QX 节点阻断检测
// Upstream: https://gist.github.com/RavelloH/383354955aa3800e1d7e98666e11e16f (auto-synced)
// Loon bridge: am-tmac. Bridges $environment / $configuration / $task to Loon APIs.
var __lp = (typeof $environment !== "undefined" && $environment && $environment.params) || {};
var __loonNode = typeof __lp === "string" ? __lp : (__lp.node || "");
var __loonInfo = (typeof __lp === "object" && __lp.nodeInfo) || {};
var __qxConfiguration = {
  sendMessage: function (msg) {
    var ret = {};
    var host = __loonInfo.address || __loonInfo.server || "";
    var port = __loonInfo.port ? String(__loonInfo.port) : "";
    if (host && port) {
      if (host.indexOf(":") !== -1 && host.charAt(0) !== "[") host = "[" + host + "]";
      ret[msg.content] = "loon=" + host + ":" + port;
    }
    return Promise.resolve({ ret: ret });
  }
};
var __qxTask = {
  fetch: function (req) {
    return new Promise(function (resolve, reject) {
      var o = { url: req.url, timeout: req.timeout || 8000, headers: req.headers || {} };
      if (req.body !== undefined) o.body = req.body;
      if (req.opts && req.opts.policy) o.node = req.opts.policy;
      var m = String(req.method || "GET").toLowerCase();
      var fn = $httpClient[m] || $httpClient.get;
      fn(o, function (err, resp, data) {
        if (err) return reject(err);
        resolve({ statusCode: resp && resp.status, headers: resp && resp.headers, body: data });
      });
    });
  }
};
'''

# (old, new, expected count)
PATCHES = [
    ("$environment.params", "__loonNode", 2),
    ("$configuration.sendMessage(", "__qxConfiguration.sendMessage(", 1),
    ("$task.fetch(", "__qxTask.fetch(", 6),
]


def main():
    req = urllib.request.Request(SRC, headers={"User-Agent": "Quantumult%20X/1.5.5"})
    js = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    if "$done" not in js or "<html" in js.lower():
        sys.exit("upstream fetch returned something unexpected")
    for old, new, n in PATCHES:
        c = js.count(old)
        if c != n:
            sys.exit(f"patch mismatch ({c}x, want {n}): {old}")
        js = js.replace(old, new)
    for left in ("$task", "$configuration", "$environment"):
        if left in js:
            sys.exit(f"unbridged QX API left: {left}")
    OUT.write_text(PRELUDE + js, encoding="utf-8")
    print(f"ok {len(js)} bytes", file=sys.stderr)


if __name__ == "__main__":
    main()
