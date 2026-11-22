from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ==============================
# Create FastAPI application
# ==============================

app = FastAPI(
    title="PropertyWise API",
    description="API for property BUY/SELL decision support",
    version="1.0.0"
)


# ==============================
# Allow frontend to call backend
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# Request model
# ==============================

class PropertyRequest(BaseModel):
    decision: str
    price: float
    size: float
    age: float
    rent: float
    location: str


# ==============================
# Health check
# ==============================

@app.get("/")
def home():
    return {
        "message": "PropertyWise API is running"
    }


# ==============================
# Property analysis
# ==============================

@app.post("/analyze")
def analyze_property(property: PropertyRequest):

    score = 50

    # Price factor
    if property.price <= 5_000_000:
        score += 10
    elif property.price <= 10_000_000:
        score += 5
    else:
        score -= 5

    # Size factor
    if property.size >= 1500:
        score += 10
    elif property.size >= 1000:
        score += 5
    else:
        score -= 5

    # Age factor
    if property.age <= 5:
        score += 10
    elif property.age <= 15:
        score += 5
    else:
        score -= 5

    # Rental yield
    annual_rent = property.rent * 12
    rental_yield = (annual_rent / property.price) * 100

    if rental_yield >= 5:
        score += 15
    elif rental_yield >= 3:
        score += 5
    else:
        score -= 5

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    # Recommendation
    if property.decision.lower() == "buy":

        if score >= 70:
            recommendation = "BUY"
        elif score >= 50:
            recommendation = "CONSIDER BUYING"
        else:
            recommendation = "AVOID BUYING"

    else:

        if score >= 70:
            recommendation = "SELL"
        elif score >= 50:
            recommendation = "CONSIDER SELLING"
        else:
            recommendation = "HOLD"

    # Reasons
    reasons = []

    if property.price <= 10_000_000:
        reasons.append(
            "The property price is within a moderate range."
        )
    else:
        reasons.append(
            "The property has a relatively high purchase price."
        )

    if property.size >= 1500:
        reasons.append(
            "The property offers good usable space."
        )
    else:
        reasons.append(
            "The property size is relatively compact."
        )

    if property.age <= 5:
        reasons.append(
            "The property is relatively new."
        )
    elif property.age <= 15:
        reasons.append(
            "The property has moderate age."
        )
    else:
        reasons.append(
            "The property is relatively old and may require additional maintenance."
        )

    if rental_yield >= 5:
        reasons.append(
            "The estimated rental yield is attractive."
        )
    elif rental_yield >= 3:
        reasons.append(
            "The estimated rental yield is moderate."
        )
    else:
        reasons.append(
            "The estimated rental yield is relatively low."
        )

    # Risks
    risks = []

    if property.price > 10_000_000:
        risks.append(
            "Higher property price may increase financial exposure."
        )

    if property.age > 15:
        risks.append(
            "Older property may require higher maintenance."
        )

    if rental_yield < 3:
        risks.append(
            "Low rental yield may reduce income potential."
        )

    if not risks:
        risks.append(
            "No major risk identified from the basic inputs."
        )

    # Explanation
    explanation = (
        f"PropertyWise gives this property a score of "
        f"{score}/100 for the selected {property.decision.upper()} decision. "
        f"The estimated rental yield is {rental_yield:.2f}%. "
        "This is an initial decision-support result and should be "
        "combined with market, legal, financial and property-specific "
        "analysis before making a final decision."
    )

    # Return JSON response
    return {
        "score": score,
        "recommendation": recommendation,
        "location": property.location,
        "rental_yield": round(rental_yield, 2),
        "reasons": reasons,
        "risks": risks,
        "explanation": explanation
    }