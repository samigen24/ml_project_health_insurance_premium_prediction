import gradio as gr
from prediction_helper import predict

# Define categorical options
categorical_options = {
    'gender': ['Male', 'Female'],
    'region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'marital_status': ['Unmarried', 'Married'],
    'bmi_category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'smoking_status': ['No Smoking', 'Regular', 'Occasional', 'Does Not Smoke', 'Not Smoking', 'Smoking=0'],
    'employment_status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'insurance_plan': ['Bronze', 'Silver', 'Gold'],
    'medical_history': [
        'Diabetes', 'High blood pressure', 'No Disease', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ]
}


def predict_premium(age, dependants, income, risk, plan, emp_status, gender, marital, bmi, smoking, region, medical):
    input_data = {
        "age": age,
        "number_of_dependants": dependants,
        "income_lakhs": income,
        "genetical_risk": risk,
        "insurance_plan": plan,
        "employment_status": emp_status,
        "gender": gender,
        "marital_status": marital,
        "bmi_category": bmi,
        "smoking_status": smoking,
        "region": region,
        "medical_history": medical
    }
    prediction = predict(input_data)
    return f"Predicted Premium: {prediction}"


with gr.Blocks() as demo:
    gr.Markdown("# Health Insurance Cost Prediction")
    gr.Markdown("Fill in the fields to predict your health insurance premium.")

    with gr.Row():
        with gr.Column():
            age = gr.Number(label="Age", value=30)
            dependants = gr.Number(label="Number of Dependants", value=0)
            income = gr.Number(label="Income (in Lakhs)", value=5.0)

        with gr.Column():
            risk = gr.Number(label="Genetical Risk", value=0.5)
            plan = gr.Dropdown(categorical_options['insurance_plan'], label="Insurance Plan")
            emp_status = gr.Dropdown(categorical_options['employment_status'], label="Employment Status")

        with gr.Column():
            gender = gr.Dropdown(categorical_options['gender'], label="Gender")
            marital = gr.Dropdown(categorical_options['marital_status'], label="Marital Status")
            bmi = gr.Dropdown(categorical_options['bmi_category'], label="BMI Category")

        with gr.Column():
            smoking = gr.Dropdown(categorical_options['smoking_status'], label="Smoking Status")
            region = gr.Dropdown(categorical_options['region'], label="Region")
            medical = gr.Dropdown(categorical_options['medical_history'], label="Medical History")

    output = gr.Textbox(label="Prediction Result")
    submit_btn = gr.Button("Predict")

    submit_btn.click(
        fn=predict_premium,
        inputs=[age, dependants, income, risk, plan, emp_status, gender, marital, bmi, smoking, region, medical],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share=True)
