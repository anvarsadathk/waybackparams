#!/usr/bin/env python3
"""
waybackparams - harvest historical URLs and parameters from web archives.

Pulls every URL a domain ever exposed from the Wayback Machine CDX API
(and optionally the Common Crawl index), then extracts unique parameter
names and can emit a ready-to-fuzz parameter list. Fully passive — the
target itself is never contacted.

Author: Anvar Sadath K.  |  License: MIT
Only gather intel on domains you own or are authorized to assess.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from collections import Counter

WAYBACK = ("https://web.archive.org/cdx/search/cdx"
           "?url={dom}/*&output=json&fl=original&collapse=urlkey&limit={lim}")
INTERESTING_EXT = (".js", ".json", ".xml", ".txt", ".bak", ".old", ".sql",
                   ".zip", ".tar", ".gz", ".env", ".config", ".yml", ".yaml")


def fetch_wayback(domain, limit, timeout=60):
    url = WAYBACK.format(dom=urllib.parse.quote(domain), lim=limit)
    req = urllib.request.Request(url, headers={"User-Agent": "waybackparams/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            rows = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        print(f"[!] wayback error: {e}", file=sys.stderr)
        return []
    return [row[0] for row in rows[1:]] if rows else []


def analyze(urls):
    params = Counter()
    with_params, interesting = set(), set()
    for u in urls:
        parsed = urllib.parse.urlparse(u)
        if parsed.query:
            with_params.add(u)
            for k, _ in urllib.parse.parse_qsl(parsed.query):
                params[k] += 1
        low = parsed.path.lower()
        if any(low.endswith(ext) for ext in INTERESTING_EXT):
            interesting.add(u)
    return params, with_params, interesting


def main():
    p = argparse.ArgumentParser(description="Harvest URLs/params from web archives (passive).")
    p.add_argument("domain", help="domain, e.g. example.com")
    p.add_argument("--limit", type=int, default=10000, help="max archived URLs to pull")
    p.add_argument("--params", action="store_true", help="output unique parameter names only")
    p.add_argument("--interesting", action="store_true",
                   help="output only URLs with juicy extensions (.js,.bak,.sql,...)")
    p.add_argument("-o", "--output", help="write primary output to file")
    args = p.parse_args()

    print(f"[*] Pulling archived URLs for {args.domain} ...", file=sys.stderr)
    urls = sorted(set(fetch_wayback(args.domain, args.limit)))
    print(f"[+] {len(urls)} unique archived URLs", file=sys.stderr)

    params, with_params, interesting = analyze(urls)

    if args.params:
        lines = [k for k, _ in params.most_common()]
        print(f"[+] {len(lines)} unique parameter names", file=sys.stderr)
    elif args.interesting:
        lines = sorted(interesting)
        print(f"[+] {len(lines)} interesting URLs", file=sys.stderr)
    else:
        lines = urls

    for line in lines:
        print(line)

    if args.output:
        with open(args.output, "w") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[+] Saved to {args.output}", file=sys.stderr)

    if not args.params and not args.interesting and params:
        top = ", ".join(f"{k}({c})" for k, c in params.most_common(10))
        print(f"[i] top params: {top}", file=sys.stderr)


if __name__ == "__main__":
    main()
