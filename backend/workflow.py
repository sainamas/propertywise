from typing import TypedDict

from langgraph.graph import END, StateGraph


class PropertyState(TypedDict):
    decision: str
    price: float
    size: float
    age: int
    rent: float
    location: str

    score: float
    recommendation: str
    rental_yield: float

    reasons: list[str]
    risks: list[str]
    explanation: str


def calculate_rental_yield(
    state: PropertyState,
):
    rental_yield = round(
        (state["rent"] * 12 / state["price"]) * 100,
        2,
    )

    return {
        "rental_yield": rental_yield,
    }


def buy_agent(state: PropertyState):

    score = 50
    reasons = []
    risks = []

    rental_yield = state["rental_yield"]

    if rental_yield >= 5:
        score += 20
        reasons.append(
            "Rental yield is relatively strong."
        )
    else:
        risks.append(
            "Rental yield is relatively low."
        )

    if state["age"] <= 10:
        score += 10
        reasons.append(
            "The property is relatively new."
        )
    else:
        risks.append(
            "The property is relatively old."
        )

    if state["size"] >= 1000:
        score += 10
        reasons.append(
            "The property provides reasonable space."
        )

    if state["price"] <= 10000000:
        score += 5

    if state["price"] > 10000000:
        risks.append(
            "The property has a relatively high purchase price."
        )

    score = min(score, 100)

    recommendation = (
        "BUY"
        if score >= 60
        else "REVIEW"
    )

    explanation = (
        f"For the {state['location']} property, "
        f"the current decision score is "
        f"{score}/100. The recommendation is "
        f"{recommendation}. This initial analysis "
        f"is based on the property price, size, "
        f"age, rental income, and selected decision."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation,
    }


def sell_agent(state: PropertyState):

    score = 50
    reasons = []
    risks = []

    rental_yield = state["rental_yield"]

    if state["age"] >= 10:
        score += 15
        reasons.append(
            "The property is relatively old."
        )

    if state["price"] >= 5000000:
        score += 15
        reasons.append(
            "The property has significant property value."
        )

    if rental_yield < 4:
        score += 10
        reasons.append(
            "Rental yield is relatively low."
        )
    else:
        risks.append(
            "Rental yield may support holding the property."
        )

    score = min(score, 100)

    recommendation = (
        "SELL"
        if score >= 60
        else "REVIEW"
    )

    explanation = (
        f"For the {state['location']} property, "
        f"the current decision score is "
        f"{score}/100. The recommendation is "
        f"{recommendation}. This initial analysis "
        f"is based on the property price, size, "
        f"age, rental income, and selected decision."
    )

    return {
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation,
    }


def route_decision(state: PropertyState):

    if state["decision"] == "buy":
        return "buy_agent"

    return "sell_agent"


workflow = StateGraph(PropertyState)

workflow.add_node(
    "calculate_rental_yield",
    calculate_rental_yield,
)

workflow.add_node(
    "buy_agent",
    buy_agent,
)

workflow.add_node(
    "sell_agent",
    sell_agent,
)

workflow.set_entry_point(
    "calculate_rental_yield"
)

workflow.add_conditional_edges(
    "calculate_rental_yield",
    route_decision,
    {
        "buy_agent": "buy_agent",
        "sell_agent": "sell_agent",
    },
)

workflow.add_edge(
    "buy_agent",
    END,
)

workflow.add_edge(
    "sell_agent",
    END,
)

property_workflow = workflow.compile()