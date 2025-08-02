import streamlit as st
import requests

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/ibm/granite-3-3b-instruct-v1"
API_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


# Chatbot backend using IBM Granite
def query_ibm_granite(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return "Sorry, I couldn't connect to the AI."
    except Exception as e:
        return f"Error: {str(e)}"


# Page Config
st.set_page_config(page_title="BudgetBoss - Finance Chatbot", layout="wide")

# --- Sidebar: User Financial Details ---
st.sidebar.title("Your Financial Info")

with st.sidebar.form("user_form"):
    user_name = st.text_input("Name", value="")
    income = st.number_input("Monthly Income (₹)", min_value=0)
    fixed_expenses = st.number_input("Fixed Expenses (₹)", min_value=0)
    savings = st.number_input("Current Savings (₹)", min_value=0)
    investments = st.number_input("Investments (₹)", min_value=0)
    tax_deductions = st.number_input("Tax Deductions (₹)", min_value=0)
    submitted = st.form_submit_button("Save Details")

if submitted:
    st.sidebar.success("Details Saved!")

# Display Header
st.markdown("<h1 style='text-align: center;'>Welcome to <span style='color: navy;'>BudgetBoss</span></h1>", unsafe_allow_html=True)

# --- Three Columns Layout ---
col1, col2, col3 = st.columns([1.1, 2, 1])

# --- Column 1: Display Saved User Details ---
with col1:
    st.subheader("Your Saved Details")
    st.markdown(f"**Name:** {user_name or 'N/A'}")
    st.markdown(f"**Monthly Income:** ₹{income}")
    st.markdown(f"**Fixed Expenses:** ₹{fixed_expenses}")
    st.markdown(f"**Current Savings:** ₹{savings}")
    st.markdown(f"**Investments:** ₹{investments}")
    st.markdown(f"**Tax Deductions:** ₹{tax_deductions}")

# --- Column 2: Financial Tips ---
with col2:
    st.subheader("💡 Financial Tips")
    tips = [
        "Track your income and expenses diligently to understand where every rupee goes.",
        "Save 3–6 months' expenses in an emergency fund.",
        "Pay off high-interest debts like credit cards first.",
        "Invest consistently — compounding works wonders over time.",
        "Set up auto-transfers from salary to savings/investments.",
        "Revisit your budget yearly.",
        "Diversify across asset classes.",
        "Use tax-saving tools (PPF, ELSS, etc.) wisely.",
        "Stay informed on personal finance & market trends."
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")

# --- Column 3: Chatbot Container with Input at Bottom ---
with col3:
    st.subheader("🤖 BuxBot Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # list of (user_msg, bot_msg)

    # Chat display container
    with st.container():
        for user_msg, bot_msg in st.session_state.chat_history:
            st.chat_message("user").write(user_msg)
            st.chat_message("assistant").write(bot_msg)

    # Divider for layout
    st.markdown("---")

    # Input at bottom
    user_input = st.chat_input("Type your message here...")

    if user_input:
        bot_reply = query_ibm_granite(user_input)

        # Basic rule-based enhancements
        prompt = user_input.lower()
        if "suggest" in prompt or "advice" in prompt:
            if income == 0 and fixed_expenses == 0 and savings == 0:
                bot_reply = "Please enter your financial details to get personalized suggestions."
            elif income > (fixed_expenses + investments + tax_deductions):
                bot_reply = "Try to save more. You're spending a bit too much."
            else:
                bot_reply = "Good job! You're managing your finances well."
        elif "budget" in prompt:
            bot_reply = f"Based on your income of ₹{income} and expenses of ₹{fixed_expenses}, you should aim to save at least 20% of your income."
        elif "invest" in prompt:
            if investments < 10000:
                bot_reply = "Consider starting with small investments in mutual funds or stocks."
            else:
                bot_reply = "Great! Keep investing regularly to build wealth over time."
        elif "tax" in prompt:
            if tax_deductions < 5000:
                bot_reply = "Maximize your tax deductions using tools like PPF or ELSS."
            else:
                bot_reply = "Good job on utilizing tax-saving instruments!"
        elif "savings" in prompt:
            if savings < 50000:
                bot_reply = "Consider building your savings to at least ₹50,000 for emergencies."
            else:
                bot_reply = "Excellent! You have a solid savings cushion."
        elif "expenses" in prompt:
            if fixed_expenses > income * 0.5:
                bot_reply = "Your fixed expenses are quite high. Consider reviewing them."
            else:
                bot_reply = "Your expenses seem manageable. Keep tracking them!"
        elif "income" in prompt:
            if income < 30000:
                bot_reply = "Consider ways to increase your income, like side gigs or upskilling."
            else:
                bot_reply = "Good job! Your income is healthy for your expenses."
        elif "financial goals" in prompt:
            bot_reply = "Setting clear financial goals is crucial. Consider short-term and long-term objectives."
        elif "debt" in prompt:
            if fixed_expenses > income * 0.4:
                bot_reply = "Try to reduce your debt burden. Focus on high-interest loans first."
            else:
                bot_reply = "Your debt seems manageable. Keep it up!"
        elif "retirement" in prompt:
            bot_reply = "Start planning for retirement early. Consider PPF or NPS for long-term savings."
        elif "insurance" in prompt:
            bot_reply = "Ensure you have adequate health and life insurance coverage."
        elif "emergency fund" in prompt:
            if savings < 3 * fixed_expenses:
                bot_reply = "Aim to build an emergency fund covering at least 3–6 months of expenses."
            else:
                bot_reply = "Great! You have a solid emergency fund."
        elif "how to save" in prompt:
            bot_reply = "Automate your savings by setting up auto-transfers to a separate savings account.\nOr follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings."
        elif "how to follow budget" in prompt:
            bot_reply = "Use budgeting apps or spreadsheets to track your income and expenses. Stick to your budget categories."
        elif "how to invest" in prompt:
            bot_reply = "Start with mutual funds or index funds for diversification. Consider SIPs for regular investments."
        elif "hi" in prompt or "hello" in prompt:
            bot_reply = f"Hello {user_name or 'there'}! How can I assist you with your finances today?"
        elif "bye" in prompt or "exit" in prompt:
            bot_reply = "Goodbye! Remember, financial discipline is key. See you next time!"
        elif "how to earn" in prompt:
            bot_reply = "Consider freelancing, online tutoring, or starting a small business based on your skills."

        # Save and display
        st.session_state.chat_history.append((user_input, bot_reply))
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(bot_reply)
