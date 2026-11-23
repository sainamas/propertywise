from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END


class PropertyState(TypedDict):
    decision: str
    price: float
    size: float
    age: float
    rent: float
    location: str

    score: int
    recommendation: str
    rental_yield: float
    reasons: list[str]
    risks: list[str]
    explanation: str


@tool
def calculate_rental_yield(price: float, monthly_rent: float) -> float:
    """Calculate annual rental yield as a percentage."""

    if price <= 0:
        return 0.0

    annual_rent = monthly_rent * 12
    rental_yield = (annual_rent / price) * 100

    return round(rental_yield, 2)


def decision_router(state: PropertyState):
    """Pass the property data to the correct decision agent."""

    return state


def route_decision(state: PropertyState) -> str:
    """Route the request to either the BUY or SELL agent."""

    if state["decision"] == "buy":
        return "buy_agent"

    return "sell_agent"


def buy_agent(state: PropertyState):
    """Analyze the property from a buying perspective."""

    rental_yield = calculate_rental_yield.invoke(
        {
            "price": state["price"],
            "monthly_rent": state["rent"],
        }
    )

    score = 50
    reasons = []
    risks = []

    if rental_yield >= 5:
        score += 20
        reasons.append("Rental yield is relatively strong.")
    else:
        risks.append("Rental yield is relatively low.")

    if state["age"] <= 10:
        score += 10
        reasons.append("The property is relatively new.")
    else:
        risks.append("The property is relatively old.")

    if state["size"] >= 1000:
        score += 10
        reasons.append("The property provides reasonable space.")

    if state["price"] <= 10_000_000:
        score += 5
    else:
        risks.append("The property has a relatively high price.")

    recommendation = "BUY" if score >= 60 else "REVIEW"

    explanation = (
        f"For the {state['location']} property, the current decision score is "
        f"{score}/100. The recommendation is {recommendation}. "
        f"This analysis considers property price, size, age, rental income, "
        f"and rental yield."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "rental_yield": rental_yield,
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation,
    }


def sell_agent(state: PropertyState):
    """Analyze the property from a selling perspective."""

    rental_yield = calculate_rental_yield.invoke(
        {
            "price": state["price"],
            "monthly_rent": state["rent"],
        }
    )

    score = 50
    reasons = []
    risks = []

    if state["age"] >= 10:
        score += 15
        reasons.append("The property is relatively old.")
    else:
        risks.append(
            "The property is relatively new, which may reduce the urgency to sell."
        )

    if state["price"] >= 5_000_000:
        score += 15
        reasons.append("The property has significant property value.")
    else:
        risks.append("The property value is relatively low.")

    if rental_yield < 4:
        score += 10
        reasons.append("Rental yield is relatively low.")
    else:
        risks.append("Rental yield is relatively strong.")

    recommendation = "SELL" if score >= 60 else "REVIEW"

    explanation = (
        f"For the {state['location']} property, the current decision score is "
        f"{score}/100. The recommendation is {recommendation}. "
        f"This analysis considers property price, size, age, rental income, "
        f"and rental yield."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "rental_yield": rental_yield,
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation,
    }


# ---------------------------------------------------------
# LangGraph workflow
# ---------------------------------------------------------

workflow = StateGraph(PropertyState)

# Add workflow nodes
workflow.add_node("decision_router", decision_router)
workflow.add_node("buy_agent", buy_agent)
workflow.add_node("sell_agent", sell_agent)

# Start → Decision Router
workflow.add_edge(START, "decision_router")

# Decision Router → BUY or SELL
workflow.add_conditional_edges(
    "decision_router",
    route_decision,
    {
        "buy_agent": "buy_agent",
        "sell_agent": "sell_agent",
    },
)

# BUY / SELL → End
workflow.add_edge("buy_agent", END)
workflow.add_edge("sell_agent", END)

# Compile the workflow
property_workflow = workflow.compile()