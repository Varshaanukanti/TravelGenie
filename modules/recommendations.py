import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors

from .travel import load_destinations


def recommend_destinations(
    travel_type="city",
    budget=30000,
    days=4
):
    df = load_destinations().copy()

    # Prepare data for machine learning
    features = df[
        ["type", "budget", "ideal_days"]
    ].copy()

    features["budget"] = (
        features["budget"] / budget
    )

    features["ideal_days"] = (
        features["ideal_days"] / days
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    )

    type_encoded = encoder.fit_transform(
        features[["type"]]
    )

    numeric_features = features[
        ["budget", "ideal_days"]
    ].values

    import numpy as np

    X = np.hstack(
        [type_encoded, numeric_features]
    )

    # Create user preference vector
    user_type = encoder.transform(
        [[travel_type]]
    )

    user_numeric = np.array([
        [1.0, 1.0]
    ])

    user_vector = np.hstack(
        [user_type, user_numeric]
    )

    # Find nearest destinations
    model = NearestNeighbors(
        n_neighbors=min(5, len(df)),
        metric="euclidean"
    )

    model.fit(X)

    distances, indices = model.kneighbors(
        user_vector
    )

    recommendations = df.iloc[
        indices[0]
    ].copy()

    recommendations["match_score"] = (
        1 / (1 + distances[0])
    )

    return recommendations