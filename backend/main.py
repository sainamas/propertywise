import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field, field_validator

from workflow import property_workflow


app = FastAPI(
    title="PropertyWise API",
    description="AI-powered property decision-support API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


class PropertyRequest(BaseModel):
    decision: str
    price: float = Field(gt=0)
    size: float = Field(gt=0)
    age: int = Field(ge=0)
    rent: float = Field(ge=0)
    location: str = Field(min_length=2)

    @field_validator("decision")
    @classmethod
    def validate_decision(cls, value):
        value = value.lower()

        if value not in ["buy", "sell"]:
            raise ValueError(
                "Decision must be either 'buy' or 'sell'"
            )

        return value

    @field_validator("location")
    @classmethod
    def validate_location(cls, value):
        value = value.strip()

        if not value:
            raise ValueError(
                "Location cannot be empty"
            )

        return value


class PropertyResponse(BaseModel):
    score: float
    recommendation: str
    location: str
    rental_yield: float
    ml_score: float
    shap_explanations: list[dict]
    reasons: list[str]
    risks: list[str]
    explanation: str


def create_access_token(username: str):

    payload = {
        "sub": username
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM,
    )


def verify_token(
    token: str = Depends(oauth2_scheme),
):

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise ValueError()

        return username

    except (JWTError, ValueError):

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


@app.get("/")
def root():

    return {
        "message": "PropertyWise API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):

    if (
        form_data.username == "demo"
        and form_data.password == "propertywise123"
    ):

        token = create_access_token(
            form_data.username
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password",
    )


@app.post(
    "/analyze",
    response_model=PropertyResponse,
)
def analyze_property(
    property_data: PropertyRequest,
    username: str = Depends(verify_token),
):

    workflow_input = {
        "decision": property_data.decision,
        "price": property_data.price,
        "size": property_data.size,
        "age": property_data.age,
        "rent": property_data.rent,
        "location": property_data.location,
    }

    result = property_workflow.invoke(
        workflow_input
    )

    return {
        "score": result["score"],
        "recommendation": result["recommendation"],
        "location": property_data.location,
        "rental_yield": result["rental_yield"],
        "ml_score": result["ml_score"],
        "shap_explanations": result["shap_explanations"],
        "reasons": result["reasons"],
        "risks": result["risks"],
        "explanation": result["explanation"],
    }