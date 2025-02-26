import streamlit as st
import requests
from streamlit_extras.card import card

# Updated Custom CSS based on your aesthetic requirements
st.markdown(f"""
<style>
    /* Overall background: Deep Chocolate Brown */
    .stApp {{
        background-color: #4E342E;
        background-size: cover;
        background-position: center;
    }}
    
    /* Input Boxes */
    .stNumberInput {{
        background-color: #FFFFFF; /* Crisp White */
        border: 1px solid #D7CCC8; /* Light subtle contrast */
        color: #3E2723; /* Rich, dark brown */
        border-radius: 8px;
        padding: 1rem;
    }}
    .stNumberInput label {{
        font-family: 'Roboto', 'Lato', sans-serif;
        color: #3E2723; /* Rich, dark brown */
    }}

    /* Buttons */
    .stButton>button {{
        background-color: #D4AF37; /* Luxurious Gold Accent */
        color: #FFFFFF; /* Bright White */
        border-radius: 8px;
        padding: 0.8rem 2rem;
        border: none;
        transition: background 0.3s ease;
        font-family: 'Roboto', 'Lato', sans-serif;
    }}
    .stButton>button:hover {{
        background-color: #E6C16A; /* Lighter gold on hover */
    }}
    
    /* Sliders */
    input[type="range"] {{
        -webkit-appearance: none;
        width: 100%;
        height: 8px;
        background: #A1887F; /* Muted Taupe */
        border-radius: 8px;
        outline: none;
    }}
    input[type="range"]::-webkit-slider-thumb {{
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        background: #6D4C41; /* Deeper refined brown */
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }}
    input[type="range"]::-moz-range-thumb {{
        width: 20px;
        height: 20px;
        background: #6D4C41;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }}

    /* Cards */
    .recommendation-card {{
        background-color: #FFFFFF; /* Clean White */
        border: 1px solid #E0E0E0; /* Very light gray */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
        border-radius: 10px;
        padding: 2rem;
    }}

    /* Typography */
    body, .stMarkdown, .stTitle, .stText, .stExpander {{
        font-family: 'Roboto', 'Lato', sans-serif;
        color: #FFFFFF; /* Primary Text Color */
    }}
</style>
""", unsafe_allow_html=True)

st.title("👗 LitFit Size Recommender")
st.markdown("### Your Personal Clothing Size Assistant")

# ---------------------------
# Step 1: Always show the Height Input
# ---------------------------
height = st.number_input("Enter your height (cm)", min_value=0.0, value=170.0, step=1.0)

# ---------------------------
# Step 2: Optionally ask for Weight input
# ---------------------------
if 'show_weight_input' not in st.session_state:
    st.session_state.show_weight_input = False

if not st.session_state.show_weight_input:
    # Button to reveal weight input (does not mention default)
    if st.button("Click here if you want to enter your weight"):
        st.session_state.show_weight_input = True
else:
    weight = st.number_input("Enter your weight (kg)", min_value=0.0, value=65.0, step=1.0)

# If not revealed, we silently assign the default
if not st.session_state.show_weight_input:
    weight = 55.0

# ---------------------------
# Step 3: Optionally ask for Chest & Waist Measurements (via sliders)
# ---------------------------
if 'show_measurements' not in st.session_state:
    st.session_state.show_measurements = False

if not st.session_state.show_measurements:
    if st.button("Click here if you want to enter chest and waist measurements"):
        st.session_state.show_measurements = True
else:
    chest = st.slider("Chest Measurement (cm)", min_value=0.0, max_value=200.0, value=100.0, step=1.0)
    waist = st.slider("Waist Measurement (cm)", min_value=0.0, max_value=200.0, value=80.0, step=1.0)
if not st.session_state.show_measurements:
    chest = 95.0
    waist = 80.0

# ---------------------------
# Get Recommendations
# ---------------------------
if st.button("Get Size Recommendations"):
    payload = {
        "ChestCMS": chest,
        "WaistCMS": waist,
        "HeightCMS": height,
        "WeightKGS": weight
    }

    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.markdown("## 📏 Your Perfect Fit")
            col1, col2 = st.columns(2)
            with col1:
                card(
                    title="👖 Jeans Size",
                    text=data["size_recommendation"]["Jeans"],
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "150px",
                            "background": "#FFFFFF",
                            "border": "1px solid #E0E0E0",
                            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.15)",
                            "border-radius": "10px"
                        },
                        "title": {"color": "#3E2723"},
                        "text": {"color": "#3E2723", "font-size": "2rem"}
                    }
                )
            with col2:
                card(
                    title="👕 T-Shirt Size",
                    text=data["size_recommendation"]["T-Shirt"],
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "150px",
                            "background": "#FFFFFF",
                            "border": "1px solid #E0E0E0",
                            "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.15)",
                            "border-radius": "10px"
                        },
                        "title": {"color": "#3E2723"},
                        "text": {"color": "#3E2723", "font-size": "2rem"}
                    }
                )
            with st.expander("📐 Detailed Body Measurements", expanded=True):
                st.markdown(f"""
                **Your Measurements:**
                - **Height:** {data["body_measurements"]["HeightCMS"]} cm
                - **Weight:** {data["body_measurements"]["WeightKGS"]} kg
                - **Chest:** {data["body_measurements"]["ChestCMS"]} cm
                - **Waist:** {data["body_measurements"]["WaistCMS"]} cm
                """)
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
