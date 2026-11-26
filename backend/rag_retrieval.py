from sentence_transformers import SentenceTransformer
from supabase_client import supabase


embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def retrieve_documents(query: str, match_count: int = 3) -> list:
    query_embedding = embedding_model.encode(query).tolist()

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": match_count,
        },
    ).execute()

    return response.data


if __name__ == "__main__":
    query = "What should I consider when buying a property?"

    results = retrieve_documents(query)

    for result in results:
        print("\n--- Document ---")
        print(result["content"])
        print("Similarity:", result["similarity"])