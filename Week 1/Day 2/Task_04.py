#4. Merge two dictionaries; if a key exists in both, sum the values.

account_1 = {"FFC": 500, "HUBC": 300, "SAZEW": 150}
account_2 = {"HUBC": 200, "SAZEW": 50,  "MEBL": 100}

merged_portfolio = account_1.copy()

for ticker, shares in account_2.items():
    merged_portfolio[ticker] = merged_portfolio.get(ticker, 0) + shares

print(f"Account 1: {account_1}")
print(f"Account 2: {account_2}")
print(f"Merged:    {merged_portfolio}")