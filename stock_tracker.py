# stock_tracker.py

# 1) Hardcoded prices
PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "MSFT": 420.0,
    "GOOGL": 140.0,
    "AMZN": 175.0,
    "NVDA": 950.0,
    "NFLX": 620.0,
}

def prompt_portfolio():
    print("Enter <TICKER> <QTY>. Press Enter on an empty line to finish.")
    print("Known prices:", ", ".join(f"{k}=${v}" for k, v in PRICES.items()))
    holdings = {}  # ticker -> total qty
    while True:
        line = input("> ").strip()
        if not line:
            break
        parts = line.split()
        if len(parts) != 2:
            print("Please enter exactly two items, e.g. AAPL 10")
            continue

        ticker, qty_str = parts[0].upper(), parts[1]
        if ticker not in PRICES:
            print(f"Unknown ticker: {ticker}. Known: {', '.join(PRICES.keys())}")
            continue

        try:
            qty = float(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("Quantity must be a positive number.")
            continue

        holdings[ticker] = holdings.get(ticker, 0.0) + qty

    return holdings

def compute_summary(holdings):
    rows = []  # List of tuples: (ticker, qty, price, value)
    total_value = 0.0
    for ticker, qty in sorted(holdings.items()):
        price = PRICES[ticker]
        value = price * qty
        total_value += value
        rows.append((ticker, qty, price, value))
    return rows, total_value

def print_summary(rows, total):
    print("\nYour Portfolio")
    print("-" * 60)
    print(f"{'Ticker':<10}{'Qty':>8}{'Price':>12}{'Value':>15}")
    print("-" * 60)
    for t, q, p, v in rows:
        print(f"{t:<10}{q:>8.2f}{p:>12.2f}{v:>15.2f}")
    print("-" * 60)
    print(f"{'TOTAL':<30}{total:>30.2f}")

def save_summary(rows, total, kind="txt", filename=None):
    import csv, datetime, os
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not filename:
        filename = f"portfolio_summary_{stamp}.{kind}"

    if kind == "csv":
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Ticker", "Quantity", "Price", "Value"])
            for t, q, p, v in rows:
                writer.writerow([t, q, p, v])
            writer.writerow([])
            writer.writerow(["TOTAL", "", "", total])
    else:
        with open(filename, "w") as f:
            f.write("Your Portfolio\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Ticker':<10}{'Qty':>8}{'Price':>12}{'Value':>15}\n")
            f.write("-" * 60 + "\n")
            for t, q, p, v in rows:
                f.write(f"{t:<10}{q:>8.2f}{p:>12.2f}{v:>15.2f}\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'TOTAL':<30}{total:>30.2f}\n")

    print(f"Saved to {os.path.abspath(filename)}")

def main():
    holdings = prompt_portfolio()
    if not holdings:
        print("No holdings entered. Exiting.")
        return
    rows, total = compute_summary(holdings)
    print_summary(rows, total)

    choice = input("\nSave result? (n/txt/csv): ").strip().lower()
    if choice in ("txt", "csv"):
        save_summary(rows, total, kind=choice)
    else:
        print("Not saved.")

if __name__ == "__main__":
    main()
