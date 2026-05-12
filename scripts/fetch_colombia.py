import json, urllib.request, datetime, os, re, sys

EVENT_ID = "34584"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'colombia-market.json')

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'GoMarket-DataBot/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def parse_field(v):
    return json.loads(v) if isinstance(v, str) else (v or [])

def extract_name(market):
    if market.get("groupItemTitle"):
        return market["groupItemTitle"]
    q = market.get("question", "")
    m = re.match(r"Will (.+?) win", q, re.IGNORECASE)
    return m.group(1) if m else q

event = fetch(f"https://gamma-api.polymarket.com/events/{EVENT_ID}")

candidates = []
for m in event.get("markets", []):
    if not m.get("active"):
        continue
    prices = parse_field(m.get("outcomePrices", "[]"))
    if not prices:
        continue
    prob = float(prices[0])
    if prob == 0.0:
        continue  # resolved/delisted market
    candidates.append({
        "name": extract_name(m),
        "prob": round(prob, 4),
        "volume": round(float(m.get("volume") or 0), 2),
        "liquidity": round(float(m.get("liquidity") or 0), 2),
        "marketId": str(m.get("id", "")),
    })

candidates.sort(key=lambda x: x["prob"], reverse=True)

data = {
    "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "event": {
        "title": event.get("title", "Colombia Presidential Election"),
        "volume": round(float(event.get("volume") or 0), 2),
        "liquidity": round(float(event.get("liquidity") or 0), 2),
    },
    "candidates": candidates,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

sys.stdout.buffer.write(("Saved " + str(len(candidates)) + " candidates -> " + OUT + "\n").encode("utf-8"))
sys.stdout.buffer.write(("Top 3: " + ", ".join(c["name"] + " " + str(round(c["prob"]*100)) + "%" for c in candidates[:3]) + "\n").encode("utf-8"))
