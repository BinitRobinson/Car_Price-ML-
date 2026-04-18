import streamlit as st
import pandas as pd
import joblib

# Page config
st.set_page_config(
    page_title="Car Price AI",
    page_icon="🚗",
    layout="centered"
)

# Load model
model = joblib.load("car_price_rf.pkl")

# Extract brands dynamically
brand_columns = [col for col in model.feature_names_in_ if col.startswith("brand_")]
brands = sorted([col.replace("brand_", "") for col in brand_columns])

# ---------- CSS ----------
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .title {
        font-size: 42px;
        font-weight: 700;
        color: white;
        text-align: center;
    }
    .subtitle {
        font-size: 16px;
        color: #A0A0A0;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: #1c1f26;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
        max-width: 700px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">🚗 Car Price AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict resale value instantly using Machine Learning</div>', unsafe_allow_html=True)

# ---------- MAIN CARD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

# Inputs
year = st.slider("Year", 1990, 2025, 2015)
km_driven = st.number_input("KM Driven", 0, 500000, 50000)

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner", [
    "First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"
])

brand = st.selectbox("Brand", brands)

st.write("")

# Predict button
predict_btn = st.button("🚀 Predict Price", use_container_width=True)

# ---------- RESULT ----------
if predict_btn:
    input_df = pd.DataFrame({
        "year": [year],
        "km_driven": [km_driven],
        "fuel": [fuel],
        "seller_type": [seller_type],
        "transmission": [transmission],
        "owner": [owner],
        "brand": [brand]
    })

    try:
        input_encoded = pd.get_dummies(input_df)

        input_encoded = input_encoded.reindex(
            columns=model.feature_names_in_,
            fill_value=0
        )

        prediction = model.predict(input_encoded)
        price = int(prediction[0])

        st.markdown(f"""
            <div style='text-align:center; margin-top:20px;'>
                <h1 style='color:#4CAF50;'>₹ {price:,}</h1>
                <p style='color:#A0A0A0;'>Estimated resale price</p>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Something went wrong")
        st.text(str(e))

st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.write("")
st.markdown(
    "<center style='color:gray;'>Built using Machine Learning</center>",
    unsafe_allow_html=True
)