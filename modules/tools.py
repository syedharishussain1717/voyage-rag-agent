
from langchain.tools import tool


# Approximate reference rates against USD.
# These are illustrative rates, NOT live exchange rates.
EXCHANGE_RATES = {
    "USD": 1.00,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 155.00,
    "INR": 83.50,
    "AUD": 1.52,
    "CAD": 1.36,
}


@tool
def convert_currency(
    amount: float,
    source_currency: str,
    target_currency: str
) -> str:
    """
    Convert an amount between supported currencies.

    Supported currencies: USD, EUR, GBP, JPY, INR, AUD, CAD.
    Uses approximate reference rates, not live market rates.
    """

    source = source_currency.strip().upper()
    target = target_currency.strip().upper()

    if amount < 0:
        return "Error: Amount cannot be negative."

    if source not in EXCHANGE_RATES:
        return f"Error: Unsupported source currency: {source}."

    if target not in EXCHANGE_RATES:
        return f"Error: Unsupported target currency: {target}."

    amount_in_usd = amount / EXCHANGE_RATES[source]
    converted_amount = amount_in_usd * EXCHANGE_RATES[target]

    return (
        f"{amount:,.2f} {source} is approximately "
        f"{converted_amount:,.2f} {target}.\n"
        "Note: This uses illustrative reference rates, "
        "not live exchange rates. Check a financial provider "
        "for the current rate before making transactions."
    )


@tool
def estimate_travel_budget(
    days: int,
    travel_style: str
) -> str:
    """
    Estimate a Japan travel budget in USD.

    Travel styles:
    budget, moderate, luxury.

    Estimates include approximate daily accommodation,
    food, and local transportation costs.
    International flights and major shopping are excluded.
    """

    if days <= 0:
        return "Error: Number of travel days must be greater than zero."

    if days > 365:
        return "Error: Please provide a trip duration of 365 days or less."

    style = travel_style.strip().lower()

    daily_estimates = {
        "budget": 50,
        "moderate": 150,
        "luxury": 400
    }

    if style not in daily_estimates:
        return (
            "Invalid travel style. Choose budget, moderate, or luxury."
        )

    daily_cost = daily_estimates[style]
    total_cost = daily_cost * days

    return (
        f"Estimated Japan travel budget:\n"
        f"Travel duration: {days} days\n"
        f"Travel style: {style.title()}\n"
        f"Estimated daily cost: ${daily_cost:,.2f}\n"
        f"Estimated total: ${total_cost:,.2f} USD\n\n"
        "This is a rough planning estimate, not a live price quote. "
        "International flights and major shopping are excluded."
    )


def get_voyage_tools():
    """
    Return all tools available to the VoyageAI agent.
    """

    return [
        convert_currency,
        estimate_travel_budget
    ]
