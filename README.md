# 🤖 LoanBuddy AI – AI-Powered Loan Assistant

**LoanBuddy AI** is a Flask-based intelligent loan application platform that replicates human loan sales executives using agentic AI. It provides instant loan processing, automated KYC verification, credit score evaluation, and instant sanction letter generation - all through a conversational interface.

---

## ✨ Features

✅ AI-powered conversational loan assistant  
💼 Supports 10 different loan types (Personal, Home, Vehicle, Education, Business, Gold, Credit Card, Agriculture, Consumer Durable, Medical)  
🔍 Automated KYC verification with PAN card validation  
📊 Real-time credit score assessment  
⚡ Instant loan approval in minutes  
📄 Auto-generated sanction letters with EMI calculations  
🔒 Bank-grade security with input validation  
🖥️ Responsive and user-friendly chat interface  
🌐 24/7 availability with no branch visits required  

---

## 🌐 Live Demo

Try it now:  
🔗 [https://loanbuddy-ai.onrender.com/](https://loanbuddy-ai.onrender.com/)  

---

## 🛠️ Tech Stack

**Frontend**: HTML, CSS, JavaScript  
**Backend**: Python (Flask)  
**Libraries**: Flask-CORS  
**Deployment**: Render  

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vignesh061/loanbuddy-ai.git
cd loanbuddy-ai
```

### 2️⃣ Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App
```bash
python app.py
```

### 5️⃣ Open in Browser
```bash
http://localhost:5000
```

---

## 📁 Project Structure
```
loanbuddy-ai/
├── app.py                 # Flask backend with loan processing logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Complete frontend UI with chat interface
└── README.md             # Project documentation
```

---

## 💳 Loan Types Supported

1. **Personal Loan** - Quick unsecured loans for personal needs
2. **Home Loan** - Financing for property purchase or construction
3. **Vehicle Loan** - New and used car/bike financing
4. **Education Loan** - Student loans for Indian and international studies
5. **Business Loan** - Working capital and business expansion loans
6. **Gold Loan** - Loans against gold ornaments
7. **Credit Card Loan** - Instant loans on existing credit cards
8. **Agriculture Loan** - Crop and farm equipment financing
9. **Consumer Durable Loan** - EMI for electronics and appliances
10. **Medical Loan** - Emergency medical treatment financing

---

## 🎯 How It Works

1. **User Registration** → Collects name and mobile number
2. **Loan Selection** → Choose from 10 loan types
3. **Smart Questionnaire** → AI asks relevant questions based on loan type
4. **KYC Verification** → Validates PAN card format
5. **Credit Check** → Evaluates credit score (minimum 700 required)
6. **Instant Approval** → Generates sanction letter with EMI details

---

## 📊 API Endpoints

### Start Conversation
```http
POST /api/start_conversation
```
Initializes a new loan application session.

### Send Message
```http
POST /api/send_message
Content-Type: application/json

{
  "message": "user input",
  "state": "conversation_state",
  "user_data": {},
  "current_question_index": 0,
  "loan_questions": []
}
```

---

## 💡 Eligibility Criteria

✅ Minimum age: 21 years  
✅ Minimum monthly income: ₹25,000  
✅ Credit score: 700+  
✅ Valid PAN & Aadhaar required  
✅ Loan amounts: ₹10,000 - ₹5 Crores (varies by type)  

---

## 🔒 Security Features

🔐 Input validation for all fields  
🔐 PAN card format verification (Regex validation)  
🔐 Credit score threshold enforcement  
🔐 CORS protection enabled  
🔐 No sensitive data stored in frontend  

---

## 🚀 Deployment on Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Set **Build Command**: `pip install -r requirements.txt`
5. Set **Start Command**: `python app.py`
6. Deploy! 🎉

---


---
