import pandas as pd

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


# Numerical features
numeric_features = [
    "price",
    "size",
    "age",
    "rent",
]

# Categorical features
categorical_features = [
    "location",
]


# Preprocess location and keep numerical values unchanged
preprocessor = ColumnTransformer(
    transformers=[
        (
            "location",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
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