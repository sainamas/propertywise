from typing import TypedDict

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

from financial_analysis import calculate_financial_metrics
from ml_model import predict_property_score


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
    ml_score: float
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


@tool
def property_ml_score(
    price: float,
    size: float,
    age: float,
    monthly_rent: float,
    location: str,
) -> float:
    """Predict a property decision score using the trained ML model."""

    return predict_property_score(
        price=price,
        size=size,
        age=age,
        rent=monthly_rent,
        location=location,
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

    ml_score = property_ml_score.invoke(
        {
            "price": state["price"],
            "size": state["size"],
            "age": state["age"],
            "monthly_rent": state["rent"],
            "location": state["location"],
        }
    )

    rental_yield = financials["rental_yield"]

    score = round((ml_score + rental_yield * 5) / 2)

    reasons = []
    risks = []

    if rental_yield >= 5:
        reasons.append("Rental yield is relatively strong.")
    else:
        risks.append("Rental yield is relatively low.")

    if ml_score >= 70:
        reasons.append("The machine learning model gives the property a strong score.")
    else:
        risks.append("The machine learning model gives the property a lower score.")

    if state["age"] <= 10:
        reasons.append("The property is relatively new.")
    else:
        risks.append("The property is relatively old.")

    recommendation = "BUY" if score >= 60 else "REVIEW"

    explanation = (
        f"For the {state['location']} property, the combined decision score is "
        f"{score}/100. The recommendation is {recommendation}. "
        f"The machine learning model produced a score of {ml_score}. "
        f"The rental yield is {rental_yield}%."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "rental_yield": rental_yield,
        "ml_score": ml_score,
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

    ml_score = property_ml_score.invoke(
        {
            "price": state["price"],
            "size": state["size"],
            "age": state["age"],
            "monthly_rent": state["rent"],
            "location": state["location"],
        }
    )

    rental_yield = financials["rental_yield"]

    score = round((ml_score + (100 - rental_yield * 10)) / 2)

    reasons = []
    risks = []

    if state["age"] >= 10:
        reasons.append("The property is relatively old.")
    else:
        risks.append(
            "The property is relatively new, which may reduce the urgency to sell."
        )

    if rental_yield < 4:
        reasons.append("Rental yield is relatively low.")
    else:
        risks.append("Rental yield is relatively strong.")

    if ml_score < 70:
        reasons.append("The machine learning model gives the property a lower score.")
    else:
        risks.append("The machine learning model gives the property a stronger score.")

    recommendation = "SELL" if score >= 60 else "REVIEW"

    explanation = (
        f"For the {state['location']} property, the combined decision score is "
        f"{score}/100. The recommendation is {recommendation}. "
        f"The machine learning model produced a score of {ml_score}. "
        f"The rental yield is {rental_yield}%."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "rental_yield": rental_yield,
        "ml_score": ml_score,
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