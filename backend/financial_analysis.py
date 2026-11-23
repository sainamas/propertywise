def calculate_financial_metrics(
    price: float,
    monthly_rent: float,
    age: float,
) -> dict:
    """
    Calculate basic financial metrics for a property.
    """

    annual_rent = monthly_rent * 12

    rental_yield = 0.0
    if price > 0:
        rental_yield = (annual_rent / price) * 100

    # Simple estimated appreciation assumption.
    # This is intentionally kept basic for the first version.
    estimated_appreciation_rate = 5.0

    estimated_annual_appreciation = (
        price * estimated_appreciation_rate / 100
    )

    estimated_total_annual_return = (
        annual_rent + estimated_annual_appreciation
    )

    total_return_percentage = 0.0
    if price > 0:
        total_return_percentage = (
            estimated_total_annual_return / price
        ) * 100

    return {
        "annual_rent": round(annual_rent, 2),
        "rental_yield": round(rental_yield, 2),
        "estimated_appreciation_rate": estimated_appreciation_rate,
        "estimated_annual_appreciation": round(
            estimated_annual_appreciation, 2
        ),
        "estimated_total_annual_return": round(
            estimated_total_annual_return, 2
        ),
        "total_return_percentage": round(
            total_return_percentage, 2
        ),
    }