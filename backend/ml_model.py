import pandas as pd
import shap

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Load training data
data = pd.read_csv("property_data.csv")


# Features used by the model
X = data[
    [
        "price",
        "size",
        "age",
        "rent",
        "location",
    ]
]


# Target the model learns to predict
y = data["target_score"]


# Preprocess location
preprocessor = ColumnTransformer(
    transformers=[
        (
            "location",
            OneHotEncoder(handle_unknown="ignore"),
            ["location"],
        ),
    ],
    remainder="passthrough",
)


# Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
)


# Combine preprocessing and model
property_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# Train the model
property_model.fit(X, y)


def predict_property_score(
    price: float,
    size: float,
    age: float,
    rent: float,
    location: str,
) -> float:
    """
    Predict the property decision score.
    """

    property_input = pd.DataFrame(
        [
            {
                "price": price,
                "size": size,
                "age": age,
                "rent": rent,
                "location": location,
            }
        ]
    )

    prediction = property_model.predict(property_input)[0]

    return round(float(prediction), 2)


def explain_property_prediction(
    price: float,
    size: float,
    age: float,
    rent: float,
    location: str,
) -> list:
    """
    Explain the ML prediction using SHAP.
    """

    property_input = pd.DataFrame(
        [
            {
                "price": price,
                "size": size,
                "age": age,
                "rent": rent,
                "location": location,
            }
        ]
    )

    # Get the preprocessing and trained Random Forest
    preprocessor = property_model.named_steps["preprocessor"]
    model = property_model.named_steps["model"]

    # Apply the same preprocessing used during training
    transformed_data = preprocessor.transform(property_input)

    # Convert sparse data to normal array if necessary
    if hasattr(transformed_data, "toarray"):
        transformed_data = transformed_data.toarray()

    # Get the actual feature names created by the preprocessor
    feature_names = preprocessor.get_feature_names_out()

    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)

    # Calculate SHAP values
    shap_values = explainer.shap_values(transformed_data)

    # SHAP contributions for this property
    contributions = shap_values[0]

    explanations = []

    for feature, contribution in zip(
        feature_names,
        contributions,
    ):
        # Make feature names easier to understand
        if feature.startswith("remainder__"):
            feature = feature.replace(
                "remainder__",
                "",
            )

        if feature.startswith("location__location_"):
            feature = feature.replace(
                "location__location_",
                "location_",
            )

        explanations.append(
            {
                "feature": feature,
                "contribution": round(
                    float(contribution),
                    2,
                ),
            }
        )

    # Strongest factors first
    explanations.sort(
        key=lambda item: abs(item["contribution"]),
        reverse=True,
    )

    # Return top 5 factors
    return explanations[:5]