from sentence_transformers import SentenceTransformer

from supabase_client import supabase


embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


documents = [
    {
        "content": (
            "Rental yield is calculated as annual rental income divided by "
            "property purchase price, multiplied by 100. Higher rental yield "
            "can indicate stronger rental income relative to the purchase price."
        ),
        "metadata": {
            "topic": "rental_yield",
            "source": "PropertyWise reference"
        }
    },
    {
        "content": (
            "Property age can affect maintenance requirements and resale "
            "considerations. Newer properties may require less immediate "
            "maintenance, while older properties may require more inspection "
            "before purchase."
        ),
        "metadata": {
            "topic": "property_age",
            "source": "PropertyWise reference"
        }
    },
    {
        "content": (
            "Property location can influence demand, rental potential, "
            "resale value, accessibility, and nearby infrastructure. "
            "Location should therefore be considered alongside price, "
            "property condition, and expected rental income."
        ),
        "metadata": {
            "topic": "location",
            "source": "PropertyWise reference"
        }
    },
    {
        "content": (
            "When evaluating whether to buy a property, consider purchase "
            "price, property size, age, expected rental income, rental yield, "
            "location, and potential risks. A property decision should not "
            "be based on a single metric."
        ),
        "metadata": {
            "topic": "buy_decision",
            "source": "PropertyWise reference"
        }
    },
    {
        "content": (
            "When evaluating whether to sell a property, consider the "
            "property's current value, age, rental performance, market "
            "conditions, holding costs, and potential future returns. "
            "A sell decision should consider multiple factors rather than "
            "a single metric."
        ),
        "metadata": {
            "topic": "sell_decision",
            "source": "PropertyWise reference"
        }
    }
]


for document in documents:
    embedding = embedding_model.encode(
        document["content"]
    ).tolist()

    supabase.table("documents").insert({
        "content": document["content"],
        "metadata": document["metadata"],
        "embedding": embedding
    }).execute()


print(f"Inserted {len(documents)} documents into Supabase.")