
from modules.tools import get_voyage_tools

tools = get_voyage_tools()

print("Available VoyageAI tools:")

for item in tools:
    print("-", item.name)

print("\nTest 1: Currency Conversion")

currency_result = tools[0].invoke({
    "amount": 100,
    "source_currency": "USD",
    "target_currency": "JPY"
})

print(currency_result)

print("\nTest 2: Travel Budget Estimation")

budget_result = tools[1].invoke({
    "days": 7,
    "travel_style": "moderate"
})

print(budget_result)

print("\nTest 3: Invalid Travel Style")

invalid_result = tools[1].invoke({
    "days": 7,
    "travel_style": "premium"
})

print(invalid_result)

print("\nSUCCESS: Travel tool tests completed!")
