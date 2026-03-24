"""Tiered fee calculation: by amount bracket × term multiplier. Cap at 15%."""

def get_fee_rate(amount: float, days: int) -> float:
    # Base rate by amount bracket
    if amount < 500:
        base = 0.05
    elif amount < 1000:
        base = 0.04
    elif amount < 2000:
        base = 0.035
    else:
        base = 0.03
    
    # Multiplier by term
    if days == 7:
        mult = 1.0
    elif days == 15:
        mult = 1.6
    elif days == 30:
        mult = 2.4
    else:
        mult = 1.0
    
    return min(base * mult, 0.15)

def calculate_fee(amount: float, days: int) -> dict:
    rate = get_fee_rate(amount, days)
    fee = round(amount * rate, 2)
    total = round(amount + fee, 2)
    return {
        "rate": rate,
        "rate_pct": f"{rate*100:.1f}%",
        "fee": fee,
        "total": total,
        "amount": amount,
        "days": days,
    }

def get_all_term_options(amount: float) -> list[dict]:
    return [calculate_fee(amount, d) for d in [7, 15, 30]]

def get_finance_options(max_amount: float) -> list[dict]:
    """Returns 100%, 50%, 25% options with absolute amounts."""
    options = []
    for pct, label in [(1.0, "Total"), (0.5, "50%"), (0.25, "25%")]:
        amt = round(max_amount * pct, 2)
        options.append({"pct": pct, "label": label, "amount": amt})
    return options
