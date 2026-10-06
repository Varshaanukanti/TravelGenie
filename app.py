import base64
from pathlib import Path

import streamlit as st

from modules.travel import (
    load_destinations,
    search_destinations,
    create_itinerary,
    estimate_budget
)

from modules.recommendations import recommend_destinations


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TravelGenie",
    page_icon="✈️",
    layout="wide"
)


# =========================================================
# BACKGROUND IMAGE
# =========================================================

PROJECT_FOLDER = Path(__file__).resolve().parent
IMAGE_PATH = PROJECT_FOLDER / "assets" / "travel_background.png"

if IMAGE_PATH.exists():

    with open(IMAGE_PATH, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(255,255,255,0.35),
            rgba(255,255,255,0.35)
        ),
        url("data:image/png;base64,{encoded_image}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}}

.hero {{
    text-align: center;
    padding: 25px;
    margin-bottom: 25px;
    border-radius: 25px;
    background: rgba(255,255,255,0.90);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}}

.hero-title {{
    font-size: 52px;
    font-weight: 800;
    margin: 0;
}}

.hero-text {{
    font-size: 20px;
    margin-top: 10px;
}}

.section-card {{
    background: rgba(255,255,255,0.90);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 22px;
    margin-top: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}}

.destination-card {{
    background: rgba(255,255,255,0.93);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 15px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.10);
}}

div.stButton > button {{
    border-radius: 12px;
    font-weight: 600;
}}

</style>
""",
        unsafe_allow_html=True
    )


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("✈️ TravelGenie")

    st.write("Your personal travel assistant")

    st.divider()

    st.subheader("🌍 Explore TravelGenie")

    if st.button(
        "🔎 Search Destinations",
        use_container_width=True
    ):
        st.session_state.page = "search"
        st.rerun()


    if st.button(
        "🗺️ Create Trip",
        use_container_width=True
    ):
        st.session_state.page = "trip"
        st.rerun()


    if st.button(
        "💰 Travel Budget",
        use_container_width=True
    ):
        st.session_state.page = "budget"
        st.rerun()


    if st.button(
        "⭐ Recommendations",
        use_container_width=True
    ):
        st.session_state.page = "recommendations"
        st.rerun()


    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.session_state.page = "home"
        st.rerun()


    st.divider()

    st.info(
        "💡 Explore destinations, plan trips, "
        "calculate budgets and discover "
        "personalized travel recommendations."
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">

<div class="hero-title">
✈️ TravelGenie
</div>

<div class="hero-text">
🌍 Your Intelligent Travel Information & Planning Assistant
</div>

<div class="hero-text">
🔎 Explore &nbsp;•&nbsp;
🗺️ Plan &nbsp;•&nbsp;
💰 Calculate &nbsp;•&nbsp;
⭐ Discover
</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

destinations = load_destinations()


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown(
        """
<div class="section-card">

<h2>👋 Welcome to TravelGenie!</h2>

<p>
Your intelligent travel assistant for discovering
destinations and planning your perfect trip.
</p>

</div>
""",
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.info(
            "🔎 Search destinations"
        )


    with col2:

        st.info(
            "🗺️ Plan your trip"
        )


    with col3:

        st.info(
            "⭐ Get recommendations"
        )


    st.markdown(
        """
<div class="section-card">

<h3>🌍 Start Exploring</h3>

<p>
Use the buttons in the sidebar to explore
TravelGenie features.
</p>

</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# SEARCH PAGE
# =========================================================

elif st.session_state.page == "search":

    st.markdown(
        """
<div class="section-card">

<h2>🔎 Search Destinations</h2>

<p>
Find destinations by name, country or travel type.
</p>

</div>
""",
        unsafe_allow_html=True
    )


    query = st.text_input(
        "Enter a destination, country, or travel type",
        placeholder="Example: Goa, India, beach..."
    )


    if query:

        results = search_destinations(query)


        if results.empty:

            st.warning(
                "😔 No destinations found. Try another search."
            )


        else:

            st.success(
                f"🎉 Found {len(results)} destination(s)!"
            )


            for _, row in results.iterrows():

                st.markdown(
                    f"""
<div class="destination-card">

<h3>
📍 {row["name"]}, {row["country"]}
</h3>

<p>
🌍 <b>Type:</b> {row["type"]}
</p>

<p>
💰 <b>Budget:</b> ₹{row["budget"]:,}
</p>

<p>
📅 <b>Ideal Days:</b> {row["ideal_days"]}
</p>

<p>
🌤️ <b>Best Season:</b> {row["best_season"]}
</p>

<p>
📝 {row["description"]}
</p>

</div>
""",
                    unsafe_allow_html=True
                )


# =========================================================
# TRIP PLANNER PAGE
# =========================================================

elif st.session_state.page == "trip":

    st.markdown(
        """
<div class="section-card">

<h2>🗺️ Trip Planner</h2>

<p>
Create a day-by-day itinerary for your trip.
</p>

</div>
""",
        unsafe_allow_html=True
    )


    destination_names = destinations["name"].tolist()


    selected_destination = st.selectbox(
        "📍 Choose your destination",
        destination_names
    )


    days = st.number_input(
        "📅 Number of days",
        min_value=1,
        max_value=30,
        value=3
    )


    travelers = st.number_input(
        "👥 Number of travelers",
        min_value=1,
        max_value=20,
        value=1
    )


    if st.button(
        "✨ Create My Trip",
        use_container_width=True
    ):

        itinerary = create_itinerary(
            selected_destination,
            days
        )


        budget = estimate_budget(
            selected_destination,
            days,
            travelers
        )


        st.success(
            f"🎉 Trip plan created for "
            f"{selected_destination}!"
        )


        st.subheader("📅 Your Itinerary")


        for item in itinerary:

            st.markdown(
                f"""
<div class="destination-card">

<h4>
📅 Day {item["day"]}
</h4>

<p>
✨ {item["activity"]}
</p>

</div>
""",
                unsafe_allow_html=True
            )


        if budget:

            st.subheader("💰 Estimated Budget")


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Daily Cost / Traveler",
                    f"₹{budget['daily_cost']:,.2f}"
                )


            with col2:

                st.metric(
                    "Total Estimated Cost",
                    f"₹{budget['total_cost']:,.2f}"
                )


# =========================================================
# BUDGET PAGE
# =========================================================

elif st.session_state.page == "budget":

    st.markdown(
        """
<div class="section-card">

<h2>💰 Travel Budget Calculator</h2>

<p>
Estimate the approximate cost of your trip.
</p>

</div>
""",
        unsafe_allow_html=True
    )


    destination_names = destinations["name"].tolist()


    selected_destination = st.selectbox(
        "📍 Choose your destination",
        destination_names
    )


    days = st.number_input(
        "📅 Number of days",
        min_value=1,
        max_value=30,
        value=3
    )


    travelers = st.number_input(
        "👥 Number of travelers",
        min_value=1,
        max_value=20,
        value=1
    )


    if st.button(
        "💰 Calculate Budget",
        use_container_width=True
    ):

        budget = estimate_budget(
            selected_destination,
            days,
            travelers
        )


        if budget:

            st.success(
                "✅ Budget calculated successfully!"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Daily Cost / Traveler",
                    f"₹{budget['daily_cost']:,.2f}"
                )


            with col2:

                st.metric(
                    "Total Estimated Cost",
                    f"₹{budget['total_cost']:,.2f}"
                )


            st.write(
                f"👥 Travelers: {travelers}"
            )

            st.write(
                f"📅 Days: {days}"
            )


# =========================================================
# RECOMMENDATIONS PAGE
# =========================================================

elif st.session_state.page == "recommendations":

    st.markdown(
        """
<div class="section-card">

<h2>⭐ Personalized Recommendations</h2>

<p>
Tell TravelGenie your preferred travel style,
budget and number of days.
</p>

</div>
""",
        unsafe_allow_html=True
    )


    recommendation_type = st.selectbox(
        "🌍 What type of trip do you prefer?",
        [
            "city",
            "beach",
            "nature",
            "heritage",
            "mountains",
            "hills"
        ]
    )


    recommendation_budget = st.number_input(
        "💰 Your budget (₹)",
        min_value=5000,
        max_value=500000,
        value=30000,
        step=5000
    )


    recommendation_days = st.number_input(
        "📅 How many days?",
        min_value=1,
        max_value=30,
        value=4
    )


    if st.button(
        "⭐ Find My Destinations",
        use_container_width=True
    ):

        recommendations = recommend_destinations(
            recommendation_type,
            recommendation_budget,
            recommendation_days
        )


        st.success(
            "🎉 Here are your recommended destinations!"
        )


        for _, row in recommendations.iterrows():

            st.markdown(
                f"""
<div class="destination-card">

<h3>
📍 {row["name"]}, {row["country"]}
</h3>

<p>
🌍 <b>Type:</b> {row["type"]}
</p>

<p>
💰 <b>Budget:</b> ₹{row["budget"]:,}
</p>

<p>
📅 <b>Ideal Days:</b> {row["ideal_days"]}
</p>

<p>
🌤️ <b>Best Season:</b> {row["best_season"]}
</p>

<p>
📝 {row["description"]}
</p>

</div>
""",
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div class="section-card" style="text-align:center;">

<h3>✈️ TravelGenie</h3>

<p>
🌍 Explore the world •
🗺️ Plan your journey •
💰 Travel smart
</p>

<p>
Made with ❤️ using Python & Streamlit
</p>

</div>
""",
    unsafe_allow_html=True
)