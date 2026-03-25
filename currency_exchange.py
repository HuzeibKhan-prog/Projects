import requests , sys

BASE = input("Enter Your Currency(e.g., INR,USD): ")
TARGETS = ["USD", "EUR", "GBP", "JPY", "AUD"]

URL = f"https://api.frankfurter.app/latest?from={BASE}"

try:
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("Error fetching data:", e)
    sys.exit(1)

print(f"Currency Exchange Rates (Base: {BASE}) on {data['date']}")
print("-" * 50)

for target in TARGETS:
    if target in data["rates"]:
        rate = data["rates"][target]
        print(f"1 {BASE} = {rate:.4f} {target}")
    else:
        print(f"{target} rate not available")
