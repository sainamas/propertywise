# PropertyWise

### AI-Powered Property Decision Support Platform

PropertyWise is an end-to-end AI-powered property analysis platform that helps users make informed **BUY / SELL decisions** using financial analysis, machine learning, explainable AI, and retrieval-augmented generation.

The system combines deterministic property calculations with a Random Forest model, SHAP explainability, domain-specific RAG, and an LLM-powered explanation layer.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         │   Property Investor  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │     Render Static Site      │
                    │       HTML / CSS / JS       │
                    └──────────────┬──────────────┘
                                   │ HTTPS / JSON
                                   ▼
                    ┌─────────────────────────────┐
                    │       FastAPI Backend       │
                    │                             │
                    │       JWT Authentication    │
                    │             │               │
                    │             ▼               │
                    │      LangGraph Workflow     │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
      ┌──────────────┐   ┌──────────────┐   ┌────────────────┐
      │   Financial  │   │ Random Forest │   │   RAG + LLM    │
      │   Analysis   │   │  + SHAP       │   │                │
      │ Yield / ROI  │   │ ML Score      │   │ Supabase       │
      └──────────────┘   └──────────────┘   │ + Groq          │
                                              └────────────────┘
                                                       │
                                                       ▼
                                           ┌────────────────────┐
                                           │ Final Explanation  │
                                           │ Score / Reasons    │
                                           │ Risks / SHAP       │
                                           └────────────────────┘

                  Docker → Render Production Deployment
```

---

## What PropertyWise Does

A user provides:

- Investment decision — BUY or SELL
- Property price
- Property size
- Property age
- Expected rental income
- Location

PropertyWise then produces:

- Overall decision score
- BUY / SELL recommendation
- Rental yield
- Machine-learning score
- SHAP feature contributions
- Reasons supporting the recommendation
- Identified risks
- Natural-language AI explanation

---

## Core Features

### 1. Secure Authentication

JWT-based authentication protects the analysis API.

The JWT secret is supplied through environment configuration rather than stored directly in the production source code.

### 2. Financial Analysis

PropertyWise calculates financial indicators such as rental yield and incorporates them into the overall decision process.

### 3. Machine Learning

A Random Forest model evaluates property characteristics and produces a model-based attractiveness score.

### 4. Explainable AI

SHAP is used to identify which property features contributed most strongly to the ML prediction.

Example:

```text
age       → +10.98
size      → +0.94
rent      → +0.77
price     → +0.35
location  → +0.11
```

This makes the ML result more interpretable than simply returning a prediction.

### 5. RAG-Based AI Advisor

PropertyWise uses retrieval-augmented generation to provide explanations grounded in property and market-related knowledge.

The RAG layer uses:

- Supabase
- Vector search
- Sentence Transformers
- Groq LLM

### 6. LangGraph Orchestration

LangGraph coordinates the analysis workflow and connects the different reasoning components.

### 7. Production Deployment

The backend is containerized using Docker and deployed as a Render Web Service.

The frontend is deployed independently as a Render Static Site.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Authentication | JWT |
| Workflow | LangGraph |
| Tools | LangChain |
| Machine Learning | scikit-learn |
| Explainability | SHAP |
| Embeddings | Sentence Transformers |
| Vector/Data Layer | Supabase / pgvector |
| LLM | Groq |
| API | REST |
| Containerization | Docker |
| Deployment | Render |
| Version Control | Git, GitHub |

---

## End-to-End Workflow

```text
1. User logs in
       ↓
2. JWT access token is issued
       ↓
3. User submits property information
       ↓
4. FastAPI validates the request
       ↓
5. LangGraph starts the analysis workflow
       ↓
6. Financial metrics are calculated
       ↓
7. Random Forest generates an ML score
       ↓
8. SHAP explains the ML prediction
       ↓
9. RAG retrieves relevant knowledge
       ↓
10. Groq generates the natural-language explanation
       ↓
11. PropertyWise combines the results
       ↓
12. BUY / SELL recommendation is returned
```

---

## Example Result

```text
Recommendation: BUY

Final Score: 60 / 100

Rental Yield: 6.0%

ML Predicted Score: 90.68

Strongest SHAP Influence:
age → +10.98
size → +0.94
rent → +0.77
price → +0.35
location → +0.11
```

The system does not rely solely on the ML prediction. The final decision combines multiple analytical signals.

---

## Why This Project Matters

Traditional property calculators usually provide isolated financial metrics.

Generic AI chatbots can explain investment concepts but may not perform a structured property assessment.

PropertyWise combines both approaches:

**Financial Analysis + Machine Learning + Explainability + RAG + LLM**

This creates a more transparent decision-support workflow.

---

## Engineering Decisions

### Why FastAPI?

FastAPI provides a lightweight Python API layer with validation, authentication, and easy integration with the ML/AI stack.

### Why LangGraph?

The analysis consists of multiple stages rather than one LLM call. LangGraph provides explicit workflow orchestration between those stages.

### Why SHAP?

A prediction without an explanation is difficult to trust. SHAP provides feature-level attribution for the Random Forest prediction.

### Why RAG?

The LLM should not rely entirely on its internal knowledge when answering domain-specific questions. Retrieval provides relevant knowledge before generation.

### Why Docker?

Docker provides a reproducible runtime environment and makes the backend easier to deploy consistently.

### Why Render?

Render provides straightforward deployment for both the Dockerized backend and static frontend while keeping the project simple enough to maintain and demonstrate.

---

## Production Deployment

### Frontend

```text
Render Static Site
        ↓
propertywise-frontend
```

### Backend

```text
Docker Container
        ↓
Render Web Service
        ↓
FastAPI
```

### External Data / AI Services

```text
Supabase → RAG / Vector Data
Groq     → LLM Generation
```

---

## Security

Implemented security measures include:

- JWT authentication
- Protected analysis endpoint
- Pydantic input validation
- Decision validation
- Positive numeric constraints
- Environment-based production secrets
- CORS configuration

---

## Testing

The deployed application has been tested across the complete request path:

```text
Frontend
   ↓
JWT Login
   ↓
Authenticated API Request
   ↓
Financial Analysis
   ↓
ML Prediction
   ↓
SHAP Explanation
   ↓
RAG / LLM
   ↓
Final Response
   ↓
Frontend Rendering
```

---

## Project Structure

```text
propertywise/
│
├── backend/
│   ├── main.py
│   ├── workflow.py
│   ├── financial_analysis.py
│   ├── ml_model.py
│   ├── llm.py
│   ├── rag_ingest.py
│   ├── rag_retrieval.py
│   ├── supabase_client.py
│   ├── property_data.csv
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── Dockerfile
├── .gitignore
└── README.md
```

---

## Future Improvements

Potential next-stage improvements include:

- Real property-market data integration
- More sophisticated property valuation models
- User-specific investment profiles
- Historical market trend analysis
- Portfolio-level property analysis
- Automated model monitoring
- More comprehensive authentication and authorization
- Production observability and monitoring

---

## Project Status

**Implemented and deployed.**

PropertyWise currently provides a working end-to-end property decision-support workflow from user input through authenticated API processing, financial analysis, ML scoring, SHAP explainability, RAG, LLM generation, and production deployment.
