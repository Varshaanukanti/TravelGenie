import pandas as pd
from pathlib import Path

# Location of destinations.csv
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "destinations.csv"


def load_destinations():
    """Load destination data from CSV."""
    return pd.read_csv(DATA_FILE)


def search_destinations(query):
    """Search destinations by name, country, or type."""
    df = load_destinations()

    query = query.lower().strip()

    result = df[
        df["name"].str.lower().str.contains(query, na=False)
        | df["country"].str.lower().str.contains(query, na=False)
        | df["type"].str.lower().str.contains(query, na=False)
    ]

    return result


def estimate_budget(destination, days, travelers):
    """Estimate total travel budget."""
    df = load_destinations()

    result = df[
        df["name"].str.lower() == destination.lower()
    ]

    if result.empty:
        return None

    daily_cost = (
        float(result.iloc[0]["budget"])
        / float(result.iloc[0]["ideal_days"])
    )

    total = daily_cost * days * travelers

    return {
        "daily_cost": round(daily_cost, 2),
        "total_cost": round(total, 2),
        "days": days,
        "travelers": travelers
    }


def create_itinerary(destination, days):
    """Create a simple sample itinerary."""
    df = load_destinations()

    result = df[
        df["name"].str.lower() == destination.lower()
    ]

    if result.empty:
        return []

    description = result.iloc[0]["description"]

    activities = [
        "Explore major local attractions",
        "Visit famous historical or cultural places",
        "Try local food",
        "Explore local markets",
        "Enjoy a relaxing activity",
        "Visit nearby attractions",
        "Free time for shopping and photography"
    ]

    itinerary = []

    for day in range(1, days + 1):
        activity = activities[(day - 1) % len(activities)]

        itinerary.append({
            "day": day,
            "activity": activity,
            "description": description
        })

    return itinerary