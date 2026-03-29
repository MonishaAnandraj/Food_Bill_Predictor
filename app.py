import streamlit as st
import pandas as pd
import joblib
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Food Bill Predictor 🍔", layout="wide")

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- CSS ----------------
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* DARK OVERLAY */
.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.70);
    z-index: 0;
}

/* CONTENT */
.block-container {
    position: relative;
    z-index: 1;
}

/* TITLE */
h1 {
    text-align: center !important;
    color: white !important;
}


/* Style all text and input elements */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    color: white !important;
    font-size: 20px !important;
}

/* Style button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(90deg, #ff512f, #dd2476) !important;
    color: white !important;
    border-radius: 10px !important;
    height: 50px !important;
    font-size: 18px !important;
    border: none !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #dd2476, #ff512f) !important;
    box-shadow: 0 4px 15px rgba(255, 81, 47, 0.4) !important;
}

/* KPI CARDS */
.kpi {
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-top: 10px;
    font-size: 16px;
    font-weight: bold;
}

.k1 {background: linear-gradient(135deg,#36d1dc,#5b86e5);}
.k2 {background: linear-gradient(135deg,#ff9966,#ff5e62);}
.k3 {background: linear-gradient(135deg,#56ab2f,#a8e063);}

/* RESULT */
.result-box {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("<h1 style='text-align: center; color: white;'>🍔 Food Bill Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ddd; font-size: 18px; margin-bottom: 25px;'>Know your order cost instantly</p>", unsafe_allow_html=True)

# -------- GLASS CONTAINER WITH BORDER --------
with st.container():
    c1, c2, c3 = st.columns(3)

    with c1:
        meal_time = st.selectbox("🍳 Meal", ["Breakfast", "Lunch", "Dinner"])

    with c2:
        restaurant = st.selectbox("🏪 Restaurant", [
            "Green Bowl", "Noodle Nest", "Pizza Palace",
            "Spice Garden", "Sushi Stop", "Taco Town"
        ])

    with c3:
        cuisine = st.selectbox("🍜 Cuisine", [
            "Chinese", "Healthy", "Indian", "Italian", "Japanese", "Mexican"
        ])
        
    c4, c5, c6 = st.columns(3)

    with c4:
        num_items = st.number_input("🍽️ Items", 1, 20, 2)
        avg_price = st.number_input("💰 Avg Price", 50.0, 1000.0, 200.0)
        discount = st.slider("🏷️ Discount %", 0, 50, 10)

    with c5:
        distance = st.slider("🚚 Distance (km)", 1, 20, 5)
        rating = st.slider("⭐ Rating", 1.0, 5.0, 4.0)
        age = st.slider("👤 Age", 18, 60, 25)

    with c6:
        gender = st.selectbox("🧑 Gender", ["Male", "Female"])
        weekend = st.selectbox("📅 Weekend", ["Yes", "No"])
        num_orders = st.slider("📦 Orders", 0, 50, 5)

    predict_btn = st.button("🚀 Predict Bill")

# -------- PREDICTION --------
if predict_btn:

    with st.spinner("Calculating..."):
        time.sleep(1.5)

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    weekend_val = 1 if weekend == "Yes" else 0
    gender_val = 1 if gender == "Male" else 0

    total_items_price = num_items * avg_price
    discount_amount = total_items_price * (discount / 100)

    input_data = pd.DataFrame({
        'num_items': [num_items],
        'avg_item_price': [avg_price],
        'discount_percent': [discount],
        'delivery_distance_km': [distance],
        'delivery_rating': [rating],
        'customer_age': [age],
        'weekend': [weekend_val],
        'num_previous_orders': [num_orders],
        'total_items_price': [total_items_price],
        'discount_amount': [discount_amount],
        'customer_gender': [gender_val]
    })

    restaurants = ['Green Bowl','Noodle Nest','Pizza Palace',
                   'Spice Garden','Sushi Stop','Taco Town']
    for r in restaurants:
        input_data[f"restaurant_name_{r}"] = 1 if restaurant == r else 0

    cuisines = ['chinese','healthy','indian','italian','japanese','mexican']
    for c in cuisines:
        input_data[f"cuisine_type_{c}"] = 1 if cuisine.lower() == c else 0

    input_data['meal_time_lunch'] = 1 if meal_time == "Lunch" else 0
    input_data['meal_time_dinner'] = 1 if meal_time == "Dinner" else 0

    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    prediction = model.predict(input_data)[0]

    # -------- KPI --------
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(f'<div class="kpi k1"><h4>Total</h4><h2>₹ {total_items_price}</h2></div>', unsafe_allow_html=True)

    with k2:
        st.markdown(f'<div class="kpi k2"><h4>Saved</h4><h2>₹ {round(discount_amount,2)}</h2></div>', unsafe_allow_html=True)

    with k3:
        st.markdown(f'<div class="kpi k3"><h4>Final</h4><h2>₹ {round(prediction,2)}</h2></div>', unsafe_allow_html=True)

    # -------- RESULT --------
    st.markdown(f"""
    <div class="result-box">
        <h2>Estimated Bill</h2>
        <h1>₹ {round(prediction,2)}</h1>
    </div>
    """, unsafe_allow_html=True)