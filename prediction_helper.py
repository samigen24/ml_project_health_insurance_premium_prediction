import pandas as pd
from joblib import load



model_rest = load('artifacts_/model_rest.joblib')
model_young = load('artifacts_/model_young.joblib')

scaler_rest = load('artifacts_/scaler_rest.joblib')
scaler_young = load('artifacts_/scaler_young.joblib')


def calculate_normalized_risk_score(medical_history):
    # Define risk scores
    risk_scores = {
        'diabetes': 6,
        'heart disease': 8,
        'high blood pressure': 6,
        'thyroid': 5,
        'no disease': 0,
        'none': 0
    }

    # Normalize inputs
    diseases = [d.strip().lower() for d in medical_history.split('&')]

    # Fill with 'none' if only one disease or empty
    if len(diseases) == 1:
        diseases.append('none')

    # Calculate total risk score
    total_score = sum(risk_scores.get(disease, 0) for disease in diseases)

    # Use the same max and min values used in df2
    max_score = 14  # max from possible: 6 + 8
    min_score = 0  # minimum risk score

    # Normalize
    normalized_score = (total_score - min_score) / (max_score - min_score)

    return round(normalized_score, 2)

def preprocess_input(input_data):
    expected_columns = ['age', 'number_of_dependants', 'income_level', 'income_lakhs',
       'insurance_plan', 'genetical_risk', 'normalized_risk_score',
       'gender_Male', 'region_Northwest', 'region_Southeast',
       'region_Southwest', 'marital_status_Unmarried', 'bmi_category_Obesity',
       'bmi_category_Overweight', 'bmi_category_Underweight',
       'smoking_status_Occasional', 'smoking_status_Regular',
       'employment_status_Salaried', 'employment_status_Self-Employed']

    # insurance_plan_encoding = {'Bronze':1, 'Silver':2, 'Gold':3}
    # df = pd.DataFrame(0, columns=expected_columns, index=[0])
    # 🧹 Standardize smoking status values before processing
    replacements = {
        'Smoking=0': 'No Smoking',
        'Does Not Smoke': 'No Smoking',
        'Not Smoking': 'No Smoking'
    }
    if 'smoking_status' in input_data:
        input_data['smoking_status'] = replacements.get(input_data['smoking_status'], input_data['smoking_status'])

    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    # bmi = input_data['BMI Category']

# we could have just imported the feature_encoding as well.
# But for simplicity, we may achieve it with the below code stack.
    for key, value in input_data.items():
        if key == 'gender' and value == 'Male':
            df['gender_Male'] = 1

        elif key == 'region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1

        elif key == 'marital_status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1

        elif key == 'bmi_category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1

        elif key == 'smoking_status':
            value = value.strip().lower()

            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1

        elif key == 'employment_status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1

        elif key == 'age':
            df['age'] = value

        elif key == 'number_of_dependants':
            df['number_of_dependants'] = value

        elif key == 'income_lakhs':
            df['income_lakhs'] = value

        elif key == 'genetical_risk':
            df['genetical_risk'] = value
            # df['normalized_risk_score'] = round(value / 10, 2)

        elif key == 'insurance_plan':
            df['insurance_plan'] = insurance_plan_encoding.get(value, 0)

        elif key == 'Income Level':
            if value == '<10L':
                df['income_level'] = 1
            elif value == '10L - 25L':
                df['income_level'] = 2
            elif value == '25L - 40L':
                df['income_level'] = 3
            elif value == '> 40L':
                df['income_level'] = 4

# Next, we need to calculate normalized_risk_score
    df['normalized_risk_score'] = calculate_normalized_risk_score(input_data['medical_history'])
    df = handle_scaling(input_data['age'], df)
    return df

def handle_scaling(age, df):
    if age<=25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest
    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level']=None
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis='columns', inplace=True)
    return df

def predict(input_data):
    input_df = preprocess_input(input_data)

    if input_data['age']<=25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    return int(prediction)
