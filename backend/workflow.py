from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

from financial_analysis import calculate_financial_metrics


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
def property_financial_analysis(
    price: float,
    monthly_rent: float,
    age: float,
) -> dict:
    """Calculate basic financial metrics for a property."""

    return calculate_financial_metrics(
        price=price,
        monthly_rent=monthly_rent,
        age=age,
    )


def decision_router(state: PropertyState):
    return state


def route_decision(state: PropertyState) -> str:
    if state["decision"] == "buy":
        return "buy_agent"

    return "sell_agent"


def buy_agent(state: PropertyState):
    financials = property_financial_analysis.invoke(
        {
            "price": state["price"],
            "monthly_rent": state["rent"],
            "age": state["age"],
        }
    )

    rental_yield = financials["rental_yield"]

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
        f"The property has a rental yield of {rental_yield}%. "
        f"The estimated total annual return is "
        f"{financials['total_return_percentage']}%."
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
    financials = property_financial_analysis.invoke(
        {
            "price": state["price"],
            "monthly_rent": state["rent"],
            "age": state["age"],
        }
    )

    rental_yield = financials["rental_yield"]

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
        f"The property has a rental yield of {rental_yield}%. "
        f"The estimated total annual return is "
        f"{financials['total_return_percentage']}%."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "rental_yield": rental_yield,
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation,
    }


workflow = StateGraph(PropertyState)

workflow.add_node("decision_router", decision_router)
workflow.add_node("buy_agent", buy_agent)
workflow.add_node("sell_agent", sell_agent)

workflow.add_edge(START, "decision_router")

workflow.add_conditional_edges(
    "decision_router",
    route_decision,
    {
        "buy_agent": "buy_agent",
        "sell_agent": "sell_agent",
    },
)

workflow.add_edge("buy_agent", END)
workflow.add_edge("sell_agent", END)

property_workflow = workflow.compile()