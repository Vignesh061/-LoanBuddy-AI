from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
# CORS(app)
CORS(app, origins=["https://your-frontend-app.onrender.com", "http://localhost:5000"])

# Loan type questions mapping
LOAN_QUESTIONS = {
    'personal_loan': [
        {'key': 'age', 'question': 'What is your age?', 'validation': 'number', 'min': 21, 'max': 65},
        {'key': 'employment_type', 'question': 'Are you salaried or self-employed?', 'validation': 'choice', 'options': ['Salaried', 'Self-employed']},
        {'key': 'monthly_income', 'question': 'What is your monthly income?', 'validation': 'number', 'min': 25000},
        {'key': 'city', 'question': 'Current city of residence?', 'validation': 'text'},
        {'key': 'employer', 'question': 'Employer / company name?', 'validation': 'text'},
        {'key': 'work_experience', 'question': 'Total work experience (in years)?', 'validation': 'number', 'min': 1},
        {'key': 'existing_emis', 'question': 'Do you have any existing loans or EMIs? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'loan_amount', 'question': 'Required loan amount? (₹)', 'validation': 'number', 'min': 50000, 'max': 5000000},
        {'key': 'tenure', 'question': 'Preferred tenure (in months)?', 'validation': 'number', 'min': 12, 'max': 60},
    ],
    'home_loan': [
        {'key': 'age', 'question': 'What is your age?', 'validation': 'number', 'min': 21, 'max': 65},
        {'key': 'employment_type', 'question': 'Are you salaried or self-employed?', 'validation': 'choice', 'options': ['Salaried', 'Self-employed']},
        {'key': 'employer', 'question': 'Name of your employer / business?', 'validation': 'text'},
        {'key': 'work_experience', 'question': 'How many years of work experience do you have?', 'validation': 'number', 'min': 1},
        {'key': 'monthly_income', 'question': 'What is your monthly net income?', 'validation': 'number', 'min': 25000},
        {'key': 'existing_emis', 'question': 'Do you have any existing EMIs? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'credit_score', 'question': 'What is your credit score (if known)? Or type "unknown"', 'validation': 'text'},
        {'key': 'property_purpose', 'question': 'Are you buying or constructing a property?', 'validation': 'choice', 'options': ['Buying', 'Constructing']},
        {'key': 'property_value', 'question': 'What is the property value?', 'validation': 'number', 'min': 500000},
        {'key': 'property_status', 'question': 'Is the property ready-to-move or under construction?', 'validation': 'choice', 'options': ['Ready-to-move', 'Under construction']},
        {'key': 'property_location', 'question': 'Property location (city/state)?', 'validation': 'text'},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 500000, 'max': 50000000},
        {'key': 'tenure', 'question': 'Preferred loan tenure (in years)?', 'validation': 'number', 'min': 5, 'max': 30},
    ],
    'vehicle_loan': [
        {'key': 'vehicle_condition', 'question': 'Are you buying a new or used vehicle?', 'validation': 'choice', 'options': ['New', 'Used']},
        {'key': 'vehicle_type', 'question': 'Type of vehicle?', 'validation': 'choice', 'options': ['Car', 'Bike', 'Commercial Vehicle']},
        {'key': 'vehicle_price', 'question': 'Vehicle price?', 'validation': 'number', 'min': 50000},
        {'key': 'down_payment', 'question': 'Down payment amount?', 'validation': 'number', 'min': 0},
        {'key': 'monthly_income', 'question': 'Monthly income?', 'validation': 'number', 'min': 25000},
        {'key': 'employment_type', 'question': 'Employment type?', 'validation': 'choice', 'options': ['Salaried', 'Self-employed']},
        {'key': 'existing_emis', 'question': 'Existing EMIs? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'tenure', 'question': 'Preferred loan tenure (in years)?', 'validation': 'number', 'min': 1, 'max': 7},
        {'key': 'dealer_location', 'question': 'Dealer location?', 'validation': 'text'},
    ],
    'education_loan': [
        {'key': 'student_age', 'question': 'Student age?', 'validation': 'number', 'min': 16, 'max': 35},
        {'key': 'course_name', 'question': 'Course name?', 'validation': 'text'},
        {'key': 'institution_name', 'question': 'Institution name?', 'validation': 'text'},
        {'key': 'study_location', 'question': 'Study location (India / Abroad)?', 'validation': 'choice', 'options': ['India', 'Abroad']},
        {'key': 'course_fee', 'question': 'Total course fee?', 'validation': 'number', 'min': 50000},
        {'key': 'coapplicant_relation', 'question': 'Co-applicant relation (parent/guardian)?', 'validation': 'text'},
        {'key': 'coapplicant_income', 'question': 'Co-applicant monthly income?', 'validation': 'number', 'min': 25000},
        {'key': 'collateral', 'question': 'Collateral available? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 50000, 'max': 10000000},
    ],
    'business_loan': [
        {'key': 'business_type', 'question': 'Business type?', 'validation': 'text'},
        {'key': 'years_operation', 'question': 'Years in operation?', 'validation': 'number', 'min': 1},
        {'key': 'annual_turnover', 'question': 'Annual turnover?', 'validation': 'number', 'min': 100000},
        {'key': 'monthly_revenue', 'question': 'Monthly revenue?', 'validation': 'number', 'min': 10000},
        {'key': 'business_registration', 'question': 'Business registration available? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'existing_loans', 'question': 'Existing business loans? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 100000, 'max': 50000000},
        {'key': 'loan_purpose', 'question': 'Purpose of loan?', 'validation': 'text'},
        {'key': 'tenure', 'question': 'Preferred tenure (in years)?', 'validation': 'number', 'min': 1, 'max': 10},
    ],
    'gold_loan': [
        {'key': 'ornament_type', 'question': 'Type of gold ornaments?', 'validation': 'text'},
        {'key': 'gold_weight', 'question': 'Gold weight (in grams)?', 'validation': 'number', 'min': 1},
        {'key': 'gold_purity', 'question': 'Gold purity (if known, e.g., 22K, 24K)? Or type "unknown"', 'validation': 'text'},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 10000, 'max': 10000000},
        {'key': 'tenure', 'question': 'Preferred tenure (in months)?', 'validation': 'number', 'min': 3, 'max': 36},
        {'key': 'city', 'question': 'City/location?', 'validation': 'text'},
    ],
    'credit_card_loan': [
        {'key': 'has_credit_card', 'question': 'Do you own a credit card? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
        {'key': 'card_bank', 'question': 'Credit card issuing bank?', 'validation': 'text'},
        {'key': 'credit_limit', 'question': 'Credit limit?', 'validation': 'number', 'min': 10000},
        {'key': 'monthly_income', 'question': 'Monthly income?', 'validation': 'number', 'min': 25000},
        {'key': 'employment_type', 'question': 'Employment type?', 'validation': 'choice', 'options': ['Salaried', 'Self-employed']},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 10000, 'max': 500000},
        {'key': 'tenure', 'question': 'Preferred tenure (in months)?', 'validation': 'number', 'min': 6, 'max': 36},
    ],
    'agriculture_loan': [
        {'key': 'farmer_name', 'question': 'Farmer name?', 'validation': 'text'},
        {'key': 'land_ownership', 'question': 'Land ownership details?', 'validation': 'text'},
        {'key': 'land_size', 'question': 'Land size (in acres)?', 'validation': 'number', 'min': 0.5},
        {'key': 'crop_type', 'question': 'Crop type?', 'validation': 'text'},
        {'key': 'season_duration', 'question': 'Season duration (in months)?', 'validation': 'number', 'min': 3},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 10000, 'max': 5000000},
        {'key': 'repayment_preference', 'question': 'Repayment preference?', 'validation': 'text'},
    ],
    'consumer_durable_loan': [
        {'key': 'product_type', 'question': 'Product type?', 'validation': 'text'},
        {'key': 'product_price', 'question': 'Product price?', 'validation': 'number', 'min': 10000},
        {'key': 'employment_type', 'question': 'Employment type?', 'validation': 'choice', 'options': ['Salaried', 'Self-employed']},
        {'key': 'monthly_income', 'question': 'Monthly income?', 'validation': 'number', 'min': 25000},
        {'key': 'tenure', 'question': 'Required EMI tenure (in months)?', 'validation': 'number', 'min': 3, 'max': 24},
        {'key': 'documents', 'question': 'PAN / Aadhaar available? (Yes/No)', 'validation': 'choice', 'options': ['Yes', 'No']},
    ],
    'medical_loan': [
        {'key': 'patient_age', 'question': 'Patient age?', 'validation': 'number', 'min': 1, 'max': 100},
        {'key': 'treatment_type', 'question': 'Treatment type?', 'validation': 'text'},
        {'key': 'hospital_name', 'question': 'Hospital name?', 'validation': 'text'},
        {'key': 'treatment_cost', 'question': 'Estimated treatment cost?', 'validation': 'number', 'min': 10000},
        {'key': 'monthly_income', 'question': 'Monthly income?', 'validation': 'number', 'min': 15000},
        {'key': 'loan_amount', 'question': 'Required loan amount?', 'validation': 'number', 'min': 10000, 'max': 2000000},
        {'key': 'tenure', 'question': 'Preferred tenure (in months)?', 'validation': 'number', 'min': 6, 'max': 36},
    ],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_conversation', methods=['POST'])
def start_conversation():
    return jsonify({
        'message': "👋 Hello! I'm LoanMate AI, your personal loan assistant. I'm here to help you get a loan approved in minutes!\n\nMay I know your name to get started?",
        'state': 'awaiting_name',
        'user_data': {},
        'current_question_index': 0
    })

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '').strip()
    state = data.get('state', 'initial')
    user_data = data.get('user_data', {})
    current_question_index = data.get('current_question_index', 0)
    loan_questions = data.get('loan_questions', [])
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    response = process_conversation(user_message, state, user_data, current_question_index, loan_questions)
    
    return jsonify(response)

def process_conversation(user_input, state, user_data, current_question_index, loan_questions):
    if state == 'awaiting_name':
        user_data['name'] = user_input
        
        return {
            'message': f"Great to meet you, {user_input}! 😊\n\nNow, could you please share your mobile number?",
            'state': 'awaiting_phone',
            'user_data': user_data,
            'current_question_index': 0
        }
    
    elif state == 'awaiting_phone':
        user_data['phone'] = user_input
        
        loan_types = """Please select the type of loan you need:

1. Personal Loan
2. Home Loan
3. Vehicle Loan
4. Education Loan
5. Business Loan
6. Gold Loan
7. Credit Card Loan
8. Agriculture Loan
9. Consumer Durable Loan
10. Medical Loan

Please enter the number or name of your preferred loan type."""
        
        return {
            'message': f"Perfect! 📱\n\n{loan_types}",
            'state': 'awaiting_loan_type',
            'user_data': user_data,
            'current_question_index': 0
        }
    
    elif state == 'awaiting_loan_type':
        loan_type_map = {
            '1': 'personal_loan', 'personal loan': 'personal_loan', 'personal': 'personal_loan',
            '2': 'home_loan', 'home loan': 'home_loan', 'home': 'home_loan',
            '3': 'vehicle_loan', 'vehicle loan': 'vehicle_loan', 'vehicle': 'vehicle_loan',
            '4': 'education_loan', 'education loan': 'education_loan', 'education': 'education_loan',
            '5': 'business_loan', 'business loan': 'business_loan', 'business': 'business_loan',
            '6': 'gold_loan', 'gold loan': 'gold_loan', 'gold': 'gold_loan',
            '7': 'credit_card_loan', 'credit card loan': 'credit_card_loan', 'credit card': 'credit_card_loan',
            '8': 'agriculture_loan', 'agriculture loan': 'agriculture_loan', 'agriculture': 'agriculture_loan',
            '9': 'consumer_durable_loan', 'consumer durable loan': 'consumer_durable_loan', 'consumer durable': 'consumer_durable_loan',
            '10': 'medical_loan', 'medical loan': 'medical_loan', 'medical': 'medical_loan',
        }
        
        loan_type = loan_type_map.get(user_input.lower())
        
        if not loan_type:
            return {
                'message': '⚠️ Please enter a valid loan type (1-10 or the loan name).',
                'state': 'awaiting_loan_type',
                'user_data': user_data,
                'current_question_index': 0
            }
        
        user_data['loan_type'] = loan_type
        loan_questions = LOAN_QUESTIONS[loan_type]
        first_question = loan_questions[0]
        
        return {
            'message': f"Excellent! You've selected {loan_type.replace('_', ' ').title()}. 💼\n\nLet me collect some details to process your application.\n\n{first_question['question']}",
            'state': 'collecting_loan_details',
            'user_data': user_data,
            'current_question_index': 0,
            'loan_questions': loan_questions
        }
    
    elif state == 'collecting_loan_details':
        if current_question_index >= len(loan_questions):
            return move_to_kyc_verification(user_data)
        
        current_question = loan_questions[current_question_index]
        
        # Validate input
        validation_result = validate_input(user_input, current_question)
        
        if not validation_result['valid']:
            return {
                'message': f"⚠️ {validation_result['message']}",
                'state': 'collecting_loan_details',
                'user_data': user_data,
                'current_question_index': current_question_index,
                'loan_questions': loan_questions
            }
        
        # Store the answer
        user_data[current_question['key']] = validation_result['value']
        
        # Move to next question
        current_question_index += 1
        
        if current_question_index >= len(loan_questions):
            return move_to_kyc_verification(user_data)
        
        next_question = loan_questions[current_question_index]
        
        return {
            'message': f"✅ Got it!\n\n{next_question['question']}",
            'state': 'collecting_loan_details',
            'user_data': user_data,
            'current_question_index': current_question_index,
            'loan_questions': loan_questions
        }
    
    elif state == 'awaiting_pan':
        import re
        pan_regex = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        
        if not re.match(pan_regex, user_input.upper()):
            return {
                'message': '⚠️ Please enter a valid PAN Card number (e.g., ABCDE1234F)',
                'state': 'awaiting_pan',
                'user_data': user_data,
                'current_question_index': current_question_index
            }
        
        user_data['pan_card'] = user_input.upper()
        
        # Generate credit score
        credit_score = random.randint(650, 850)
        user_data['credit_score'] = credit_score
        
        if credit_score < 700:
            return {
                'message': f"🔍 Verifying your KYC details...\n\n✅ KYC Verification Successful!\n\nChecking your credit score...\n\n📉 Your credit score is {credit_score}. Unfortunately, we require a minimum score of 700 for loan approval.\n\nWe recommend improving your credit score and applying again in the future.",
                'state': 'rejected',
                'user_data': user_data,
                'current_question_index': current_question_index
            }
        
        # Generate application ID
        app_id = 'LM' + str(int(datetime.now().timestamp()))[-8:]
        user_data['application_id'] = app_id
        
        return {
            'message': f"🔍 Verifying your KYC details...\n\n✅ KYC Verification Successful!\n\nChecking your credit score...\n\n🎉 Excellent! Your credit score is {credit_score}.\n\n**All checks passed!** ✅\n\nGenerating your sanction letter...",
            'state': 'approved',
            'user_data': user_data,
            'current_question_index': current_question_index
        }
    
    else:
        return {
            'message': 'Thank you! If you need any further assistance, feel free to start a new conversation.',
            'state': 'completed',
            'user_data': user_data,
            'current_question_index': current_question_index
        }

def validate_input(user_input, question):
    validation_type = question.get('validation')
    
    if validation_type == 'number':
        try:
            value = int(user_input.replace(',', '').replace('₹', '').strip())
            min_val = question.get('min')
            max_val = question.get('max')
            
            if min_val and value < min_val:
                return {'valid': False, 'message': f'Value should be at least {min_val}'}
            if max_val and value > max_val:
                return {'valid': False, 'message': f'Value should not exceed {max_val}'}
            
            return {'valid': True, 'value': value}
        except ValueError:
            return {'valid': False, 'message': 'Please enter a valid number'}
    
    elif validation_type == 'choice':
        options = question.get('options', [])
        user_input_lower = user_input.lower()
        
        for option in options:
            if option.lower() in user_input_lower or user_input_lower in option.lower():
                return {'valid': True, 'value': option}
        
        return {'valid': False, 'message': f'Please choose from: {", ".join(options)}'}
    
    elif validation_type == 'text':
        if len(user_input) < 2:
            return {'valid': False, 'message': 'Please enter a valid response'}
        return {'valid': True, 'value': user_input}
    
    return {'valid': True, 'value': user_input}

def move_to_kyc_verification(user_data):
    loan_type = user_data.get('loan_type', '').replace('_', ' ').title()
    
    summary = f"📋 **Application Summary for {loan_type}:**\n\n"
    
    # Add key details to summary
    if 'loan_amount' in user_data:
        summary += f"• Loan Amount: ₹{user_data['loan_amount']:,}\n"
    if 'tenure' in user_data:
        tenure_label = "months" if user_data['tenure'] < 60 else "years"
        summary += f"• Tenure: {user_data['tenure']} {tenure_label}\n"
    if 'monthly_income' in user_data:
        summary += f"• Monthly Income: ₹{user_data['monthly_income']:,}\n"
    
    summary += "\n✅ All details collected successfully!\n\n"
    summary += "Now, could you please provide your PAN Card number for KYC verification?"
    
    return {
        'message': summary,
        'state': 'awaiting_pan',
        'user_data': user_data,
        'current_question_index': 0
    }

if __name__ == '__main__':
    app.run()