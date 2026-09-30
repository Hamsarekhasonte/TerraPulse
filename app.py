import os
import re
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TerraPulse",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel(
        model_name="gemini-3.8-flash"
    )
else:
    model = None


# =========================================================
# SYSTEM PROMPT
# =========================================================

PROMPT_PATH = Path("prompts/system_prompt.txt")

if PROMPT_PATH.exists():
    SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")
else:
    SYSTEM_PROMPT = """
    You are TerraPulse, an AI assistant for regenerative agriculture.
    Provide practical and explainable recommendations based on
    soil, crop and environmental information.
    """


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🌱 TerraPulse</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Regenerative Agricultural Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Transform farm data into practical insights for soil health, "
    "regenerative practices, water management and climate resilience."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🌾 About TerraPulse")

    st.write(
        "TerraPulse uses Gemini-powered analysis to help farmers "
        "understand field conditions and explore regenerative "
        "agriculture practices."
    )

    st.divider()

    st.caption("Hackathon Track")
    st.write("**Track 4 — AgriN & Regenerative Agricultural Intelligence**")

    st.caption("Team")
    st.write("**TerraPulse**")

    st.divider()

    st.caption(
        "AI-generated recommendations should be validated "
        "with local agricultural experts and field conditions."
    )


# =========================================================
# INPUT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">🌾 Farm Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    crop = st.selectbox(
        "Crop",
        [
            "Rice",
            "Wheat",
            "Maize",
            "Cotton",
            "Groundnut",
            "Vegetables",
            "Other"
        ]
    )

    location = st.text_input(
        "Location",
        placeholder="Example: Hyderabad, Telangana"
    )

    farming_practice = st.selectbox(
        "Current Farming Practice",
        [
            "Conventional farming",
            "Mixed farming",
            "Organic farming",
            "Crop rotation",
            "Cover cropping",
            "Reduced tillage",
            "Other"
        ]
    )

with col2:

    soil_ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )

    nitrogen = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=45.0,
        step=1.0
    )

    phosphorus = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=30.0,
        step=1.0
    )

    potassium = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=40.0,
        step=1.0
    )


st.markdown(
    '<div class="section-title">🌦️ Environmental Conditions</div>',
    unsafe_allow_html=True
)

col3, col4, col5 = st.columns(3)

with col3:

    soil_moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=55.0,
        step=1.0
    )

with col4:

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=120.0,
        step=1.0
    )

with col5:

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-20.0,
        max_value=60.0,
        value=28.0,
        step=0.5
    )


st.divider()


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(
    "🔍 Analyze Farm with TerraPulse AI",
    type="primary",
    use_container_width=True
)


# =========================================================
# AI ANALYSIS
# =========================================================

if analyze:

    if not API_KEY:

        st.error(
            "Gemini API key not found. "
            "Please configure GEMINI_API_KEY in your .env file."
        )

        st.stop()

    farm_data = f"""
Crop: {crop}
Location: {location}
Current Farming Practice: {farming_practice}

Soil pH: {soil_ph}
Nitrogen (N): {nitrogen}
Phosphorus (P): {phosphorus}
Potassium (K): {potassium}

Soil Moisture: {soil_moisture}%
Rainfall: {rainfall} mm
Temperature: {temperature} °C
"""

    prompt = f"""
{SYSTEM_PROMPT}

Analyze this farm:

{farm_data}

Return the response using EXACTLY these sections:

SOIL HEALTH ASSESSMENT
Give a concise assessment.

FARM HEALTH SCORE
Give one score from 0 to 100 and explain the main factors.

KEY RISKS
List the most important risks.

REGENERATIVE RECOMMENDATIONS
Give 3 to 5 practical regenerative agriculture practices.

WATER MANAGEMENT
Give practical water-management guidance.

ACTION PLAN
Give 3 prioritized actions.

EXPLANATION
Explain how the provided data influenced the recommendations.

Important:
Do not claim certainty.
These are AI-assisted recommendations and should be validated
with local agricultural experts and field conditions.
"""

    with st.spinner("🌱 TerraPulse AI is analyzing your farm..."):

        try:

            response = model.generate_content(prompt)

            result = response.text

            # -------------------------------------------------
            # Extract health score
            # -------------------------------------------------

            score_match = re.search(
                r"(?:Score|score)[^\d]*(\d{1,3})\s*(?:/|out of)?\s*100",
                result
            )

            score = None

            if score_match:
                score = int(score_match.group(1))

            # -------------------------------------------------
            # Farm overview metrics
            # -------------------------------------------------

            st.success("AI analysis completed successfully.")

            st.markdown(
                '<div class="section-title">📊 Farm Snapshot</div>',
                unsafe_allow_html=True
            )

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                if score is not None:
                    st.metric("Farm Health", f"{score}/100")
                else:
                    st.metric("Farm Health", "AI assessed")

            with metric2:
                st.metric("Soil pH", f"{soil_ph}")

            with metric3:
                st.metric("Moisture", f"{soil_moisture}%")

            with metric4:
                st.metric("Rainfall", f"{rainfall} mm")

            st.divider()

            # -------------------------------------------------
            # AI RESULTS
            # -------------------------------------------------

            st.markdown(
                '<div class="section-title">🤖 TerraPulse AI Analysis</div>',
                unsafe_allow_html=True
            )

            st.markdown(result)

        except Exception as e:

            st.error("Unable to generate the AI analysis.")

            st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "TerraPulse • AI-powered regenerative agricultural intelligence • "
    "Track 4"
)