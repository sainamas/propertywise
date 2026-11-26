import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_property_explanation(
    decision: str,
    location: str,
    score: int,
    ml_score: float,
    rental_yield: float,
    shap_explanations: list,
    rag_context: list,
) -> str:

    rag_text = "\n".join(
        document["content"]
        for document in rag_context
    )

    shap_text = "\n".join(
        f"{item['feature']}: {item['contribution']}"
        for item in shap_explanations
    )

    prompt = f"""
You are a property decision assistant.

Explain the existing property analysis to a customer
using ONLY the information supplied below.

Decision: {decision}
Location: {location}
Final decision score: {score}/100
ML predicted score: {ml_score}
Rental yield: {rental_yield}%

SHAP factors:
{shap_text}

Relevant property guidance:
{rag_text}

IMPORTANT RULES:

1. The final decision and final decision score are authoritative.
2. Do not recalculate or change the final decision score.
3. Do not describe the ML predicted score as confidence or probability.
4. The ML predicted score describes the model's prediction only.
5. SHAP values explain the influence of features on the ML model's prediction.
6. Do not say that SHAP values directly determine the final BUY/SELL decision.
7. Do not invent property facts, market prices, valuations, or statistics.
8. Do not guarantee rental income, appreciation, or investment returns.
9. The rental yield is a calculated estimate based on the supplied price and rent.
10. Do not claim that the final score uses factors that are not explicitly
    provided in the analysis.
11. Do not give a new BUY/SELL recommendation different from the supplied decision.
12. Keep the explanation concise and easy for a customer to understand.

Explain:
- the existing recommendation,
- the final decision score,
- what the ML predicted score represents,
- the rental yield,
- the strongest SHAP factors,
- and relevant considerations from the retrieved guidance.

Do not introduce information that is not present in the supplied data.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content