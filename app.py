import os
from pathlib import Path

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="TerraPulse",
    page_icon="🌱",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# ---------------------------------------------------------
# GEMINI CONFIGURATION
# ---------------------------------------------------------

if API_KEY:
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel(
    model_name="gemini-3.8-flash"
)
else:
    model = None


# ---------------------------------------------------------
# LOAD SYSTEM PROMPT
# ---------------------------------------------------------

PROMPT_PATH = Path("prompts/system_prompt.txt")

if PROMPT_PATH.exists():
    SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")
else:
    SYSTEM_PROMPT = """
    You are TerraPulse, an AI assistant for regenerative agriculture.
    Provide practical and explainable recommendations based on
    soil, crop and environmental information.
    """


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🌱 TerraPulse")

st.subheader(
    "AI-Powered Regenerative Agricultural Intelligence"
)

st.write(
    "Analyze farm conditions and receive AI-assisted insights "
    "for soil health, regenerative practices, water management "
    "and climate-related risks."
)

st.divider()


# ---------------------------------------------------------
# FARM INFORMATION
# ---------------------------------------------------------

st.header("🌾 Farm Information")

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


st.subheader("🌦️ Environmental Conditions")

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


# ---------------------------------------------------------
# ANALYZE FARM
# ---------------------------------------------------------

analyze = st.button(
    "🔍 Analyze Farm",
    type="primary",
    use_container_width=True
)


if analyze:

    if not API_KEY:

        st.error(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY to your .env file."
        )

    else:

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

Analyze the following farm information:

{farm_data}

Return your response using these sections:

### 🌱 Soil Health Assessment
Give a concise assessment.

### 📊 Farm Health Score
Give a score from 0 to 100 and explain the main factors.

### ⚠️ Key Risks
Identify important soil, water or climate-related risks.

### ♻️ Regenerative Recommendations
Give 3 to 5 practical regenerative agriculture practices.

### 💧 Water Management
Give practical water-management guidance.

### 🌾 Action Plan
Give 3 prioritized actions the farmer can consider.

### 🤖 Explanation
Briefly explain how the provided data influenced your recommendations.

Important:
Do not claim certainty.
These are AI-assisted recommendations and should be validated with
local agricultural experts and field conditions.
"""

        with st.spinner("🌱 TerraPulse is analyzing the farm..."):

            try:

                response = model.generate_content(prompt)

                st.success("Analysis completed!")

                st.divider()

                st.header("🌱 TerraPulse AI Analysis")

                st.markdown(response.text)

            except Exception as e:

                st.error(
                    "Unable to generate the AI analysis."
                )

                st.code(str(e))