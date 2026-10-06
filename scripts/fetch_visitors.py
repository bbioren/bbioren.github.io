"""Pull visitor countries from GoatCounter into _data/visitors.json.

Run by .github/workflows/visitor-map.yml once a day. Needs a GoatCounter API
token (Settings -> API, with "read statistics" permission) in the repo secret
GOATCOUNTER_TOKEN. Without the token it exits quietly and changes nothing.
"""

import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

SITE = "https://bbioren.goatcounter.com"
START = "2026-10-05"  # first day of counting
OUT = Path(__file__).resolve().parents[1] / "_data" / "visitors.json"


def get(path, token):
    req = urllib.request.Request(
        SITE + path,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    if not token:
        print("GOATCOUNTER_TOKEN not set; leaving visitors.json alone.")
        return 0
    end = date.today().isoformat()
    locs = get(f"/api/v0/stats/locations?start={START}&end={end}&limit=200", token)
    countries = []
    for s in locs.get("stats", []):
        iso = (s.get("id") or "").split("-")[0].upper()
        if len(iso) == 2 and s.get("count", 0) > 0:
            countries.append({"iso": iso, "count": int(s["count"])})
    countries.sort(key=lambda c: -c["count"])
    total = get(f"/api/v0/stats/total?start={START}&end={end}", token).get("total", sum(c["count"] for c in countries))
    data = {"simulated": False, "updated": end, "total": int(total), "countries": countries}
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {len(countries)} countries, total {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
