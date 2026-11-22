from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="PropertyWise API",
    description="AI-powered property decision-support API",
    version="1.0.0",
)


# Allow the frontend to communicate with the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PropertyRequest(BaseModel):
    decision: str = Field(..., description="buy or sell")
    price: float = Field(..., gt=0)
    size: float = Field(..., gt=0)
    age: int = Field(..., ge=0)
    rent: float = Field(..., ge=0)
    location: str = Field(..., min_length=2)


class PropertyResponse(BaseModel):
    score: float
    recommendation: str
    location: str
    rental_yield: float
    reasons: list[str]
    risks: list[str]
    explanation: str


@app.get("/")
def home():
    return {"message": "PropertyWise API is running"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "propertywise-api",
    }


@app.post("/analyze", response_model=PropertyResponse)
def analyze_property(property: PropertyRequest):

    rental_yield = round(
        (property.rent * 12 / property.price) * 100,
        2
    )

    score = 50

    if property.decision.lower() == "buy":
        if rental_yield >= 5:
            score += 20

        if property.age <= 10:
            score += 10

        if property.size >= 1000:
            score += 10

        if property.price <= 10000000:
            score += 5

    elif property.decision.lower() == "sell":
        if property.age >= 10:
            score += 15

        if property.price >= 5000000:
            score += 15

        if rental_yield < 4:
            score += 10

    score = min(score, 100)

    if property.decision.lower() == "buy":
        recommendation = "BUY" if score >= 60 else "REVIEW"
    else:
        recommendation = "SELL" if score >= 60 else "REVIEW"

    reasons = []
    risks = []

    if rental_yield >= 5:
        reasons.append("Rental yield is relatively strong.")
    else:
        risks.append("Rental yield is relatively low.")

    if property.age <= 10:
        reasons.append("The property is relatively new.")
    else:
        risks.append("The property is relatively old.")

    if property.size >= 1000:
        reasons.append("The property provides reasonable space.")

    if property.price > 10000000:
        risks.append("The property has a relatively high purchase price.")

    explanation = (
        f"For the {property.location} property, the current "
        f"decision score is {score}/100. The recommendation is "
        f"{recommendation}. This initial analysis is based on the "
        f"property price, size, age, rental income, and selected decision."
    )

    return PropertyResponse(
        score=score,
        recommendation=recommendation,
        location=property.location,
        rental_yield=rental_yield,
        reasons=reasons,
        risks=risks,
        explanation=explanation,
    )