import streamlit as st
import pandas as pd
import numpy as np
import pickle

@st.cache_resource
def load_assets():
    try:
        with open('model.pkl', 'rb') as f:
            m = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            s = pickle.load(f)
        return m, s
    except FileNotFoundError:
        return None, None

model, scaler = load_assets()

st.title("💳 Credit Card Fraud Detection Dashboard")

if model is None:
    st.error("⚠️ Local assets missing. Please click 'Run All' in `project.ipynb` first to create the model binaries.")
else:
    st.header("Transaction Evaluation Interface")
    amount = st.number_input("Transaction Value (\$)", min_value=0.0, value=50.0)
    
    st.write("Enter V1 to V28 Anonymized Features:")
    pca_inputs = []
    cols = st.columns(4)
    for i in range(1, 29):
        with cols[(i-1) % 4]:
            val = st.number_input(f"Feature V{i}", value=0.0, key=f"v{i}")
            pca_inputs.append(val)
            
    if st.button("Run Security Diagnosis", type="primary"):
        scaled_amount = scaler.transform([[amount]])
        full_vector = np.array(pca_inputs + [scaled_amount[0][0]]).reshape(1, -1)
        
        prediction = model.predict(full_vector)
        probs = model.predict_proba(full_vector)[0]
        
        if prediction[0] == 1:
            st.error(f"🚨 Flagged: Highly unusual transaction fingerprint. (Fraud probability: {probs[1]:.1%})")
        else:
            st.success(f"✅ Verified: Legitimate transaction patterns. (Legitimacy score: {probs[0]:.1%})")
