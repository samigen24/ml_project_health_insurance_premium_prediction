import streamlit as st
from prediction_helper import predict

# Define categorical values
categorical_options = {
    'gender': ['Male', 'Female'],
    'region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'marital_status': ['Unmarried', 'Married'],
    'bmi_category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'smoking_status': ['No Smoking', 'Regular', 'Occasional','Does Not Smoke', 'Not Smoking','Smoking=0'],
    'employment_status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'insurance_plan': ['Bronze', 'Silver', 'Gold'],
    'medical_history': [
        'Diabetes', 'High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ]
}

# Page title
st.title("Health Insurance Cost Prediction")

# Layout: 4 rows × 3 columns
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

# --- Row 1 ---
with row1[0]:
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
with row1[1]:
    number_of_dependants = st.number_input("Number of Dependants", min_value=0, step=1)
with row1[2]:
    income_lakhs = st.number_input("Income (in Lakhs)", min_value=0.0, step=0.1)

# --- Row 2 ---
with row2[0]:
    genetical_risk = st.number_input("Genetical Risk", min_value=0.0, step=0.1)
with row2[1]:
    insurance_plan = st.selectbox("Insurance Plan", categorical_options['insurance_plan'])
with row2[2]:
    employment_status = st.selectbox("Employment Status", categorical_options['employment_status'])

# --- Row 3 ---
with row3[0]:
    gender = st.selectbox("Gender", categorical_options['gender'])
with row3[1]:
    marital_status = st.selectbox("Marital Status", categorical_options['marital_status'])
with row3[2]:
    bmi_category = st.selectbox("BMI Category", categorical_options['bmi_category'])

# --- Row 4 ---
with row4[0]:
    smoking_status = st.selectbox("Smoking Status", categorical_options['smoking_status'])
with row4[1]:
    region = st.selectbox("Region", categorical_options['region'])
with row4[2]:
    medical_history = st.selectbox("Medical History", categorical_options['medical_history'])

# --- Create a dictionary for input values ---

input_data = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "genetical_risk": genetical_risk,
        "insurance_plan": insurance_plan,
        "employment_status": employment_status,
        "gender": gender,
        "marital_status": marital_status,
        "bmi_category": bmi_category,
        "smoking_status": smoking_status,
        "region": region,
        "medical_history": medical_history
    }

#... Create Predict Button
if st.button("Predict"):
    prediction = predict(input_data)
    st.success(f'Predicted Premium: {prediction}')