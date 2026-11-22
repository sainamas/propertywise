import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="PropertyWise API",
    description="AI-powered property decision-support API",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Authentication configuration
# --------------------------------------------------

SECRET_KEY = os.getenv("JWT_SECRET", "development-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
)


# --------------------------------------------------
# Request / Response models
# --------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


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


# --------------------------------------------------
# Temporary demo user
# --------------------------------------------------

DEMO_USER = {
    "username": "demo",
    "password_hash": pwd_context.hash("propertywise123"),
}


# --------------------------------------------------
# Authentication helpers
# --------------------------------------------------

def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        return username

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    return verify_token(token)


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "PropertyWise API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "propertywise-api",
    }


@app.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):

    if request.username != DEMO_USER["username"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not pwd_context.verify(
        request.password,
        DEMO_USER["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(request.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.post(
    "/analyze",
    response_model=PropertyResponse,
)
def analyze_property(
    property: PropertyRequest,
    current_user: str = Depends(get_current_user),
):

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
        recommendation = (
            "BUY" if score >= 60 else "REVIEW"
        )
    else:
        recommendation = (
            "SELL" if score >= 60 else "REVIEW"
        )

    reasons = []
    risks = []

    if rental_yield >= 5:
        reasons.append(
            "Rental yield is relatively strong."
        )
    else:
        risks.append(
            "Rental yield is relatively low."
        )

    if property.age <= 10:
        reasons.append(
            "The property is relatively new."
        )
    else:
        risks.append(
            "The property is relatively old."
        )

    if property.size >= 1000:
        reasons.append(
            "The property provides reasonable space."
        )

    if property.price > 10000000:
        risks.append(
            "The property has a relatively high purchase price."
        )

    explanation = (
        f"For the {property.location} property, the current "
        f"decision score is {score}/100. The recommendation is "
        f"{recommendation}. This initial analysis is based on "
        f"the property price, size, age, rental income, and "
        f"selected decision."
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