#!/usr/bin/env python3
import sys, csv
from pathlib import Path

def normalize_text(text: str) -> list[str]:
    # Normalize CRLF/CR to LF
    t = text.replace('\r\n', '\n').replace('\r', '\n')
    # If file has very few newlines but many commas, it's likely a comma-joined list
    if t.count('\n') < 3 and t.count(',') > 3:
        # also strip any surrounding quotes
        t = t.replace('"','')
        t = t.replace(',', '\n')
    return [line.strip() for line in t.split('\n') if line.strip()]

def to_rows(lines: list[str]) -> list[tuple[str,str]]:
    rows = []
    for line in lines:
        # Support chained pairs like CRYPTOCAP:ETH-AMEX:USD
        for seg in line.split('-'):
            seg = seg.strip().strip('"')
            if not seg:
                continue
            if ':' in seg:
                ex, tk = seg.split(':', 1)
            else:
                ex, tk = "", seg
            rows.append((ex.strip(), tk.strip()))
    return rows

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert_watchlist.py <input_txt_or_csv> <output_csv>")
        sys.exit(1)

    src = Path(sys.argv[1]).expanduser()
    dest = Path(sys.argv[2]).expanduser()
    if not src.exists():
        sys.exit(f"❌ File not found: {src}")

    text = src.read_text(encoding="utf-8", errors="ignore")
    lines = normalize_text(text)
    rows = to_rows(lines)

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Exchange","Ticker"])
        w.writerows(rows)

    print(f"✅ Wrote {len(rows)} rows to {dest}")

if __name__ == "__main__":
    main()