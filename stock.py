from flask import Flask, render_template, request,redirect
import yfinance as yf
import google.generativeai as genai
import configparser
import markdown
from nlp import check_real_time_data

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Set the Google Gemini API key
google_gemini_api_key = config['API_KEYS']['GOOGLE_GEMINI_API_KEY']
genai.configure(api_key=google_gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

# Define the name of the bot
name = 'Financial Assistant BOT'

# Define the role of the bot
role = 'financial assistant and economics specialist with great knowledge about the indian economy'

# Define the impersonated role with instructions
impersonated_role = f"""
   From now on, you are going to act as {name}. Your role is {role}.
    You provide users with tailored budgeting advice and personal finance recommendations.
    Deliver the latest stock market news and summarize daily Sensex and Nifty movements.
    Assist users with financial education such as understanding the process of filing income tax returns in India.
    Efficiently address common financial queries using the integrated FAQ model.
    Reply to all requests with the pronoun "I" and never give unknown information. Forward users to the website for more information when necessary.
    YOU ARE NOT AN AI MODEL!
"""

# Initialize variables for chat history
explicit_input = ""
chat_output = 'Chat log: /n'

# Create a Flask web application
app = Flask(__name__)

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    return hist

def summarize_data(data):
    impersonated_role1 = f"""
   From now on, you are going to act as {name}. Your role is {role}.
    You provide users with correct financial and economic facts.
    Deliver the latest stock market news and summarize daily Sensex and Nifty movements.
 Do not use pronouns like 'I' and never give unknown information.
    YOU ARE NOT AN AI MODEL!
"""
    output = model.generate_content(
      f"{impersonated_role1}. Summarize the following data: {data}"
    )
    response = output.text
    return markdown.markdown(response)

def get_summary():
    nifty_data = get_stock_data("^NSEI")
    sensex_data = get_stock_data("^BSESN")
    bank_nifty_data = get_stock_data("^NSEBANK")

    nifty_summary = summarize_data(nifty_data.to_string())
    sensex_summary = summarize_data(sensex_data.to_string())
    bank_nifty_summary = summarize_data(bank_nifty_data.to_string())

    summary = f"Nifty Summary:\n{nifty_summary}\n\nSensex Summary:\n{sensex_summary}\n\nBank Nifty Summary:\n{bank_nifty_summary}"
    
    return summary

# Example local function to handle specific prompts
def handle_local_function(user_input):
    if(check_real_time_data(user_input)):
        
        return get_summary()
    else:
        return None  # Return None if no specific handling is required


    
print(handle_local_function("give me today's market summary"))

@app.route("/")
def index():
    return render_template("stocks.html")



@app.route("/get_response")
def get_response():
    user_text = request.args.get('msg')

    local_response = handle_local_function(user_text)
    
    if local_response:
        return local_response
    else:
        
        output = model.generate_content(
        f"{impersonated_role}. User: {user_text}"
            )
        response = markdown.markdown(output.text)
        return response
    

if __name__ == "__main__":
    app.run()
