from flask import Flask, render_template, request,redirect
import yfinance as yf
import google.generativeai as genai
import configparser
import markdown
from nlp import check_real_time_data

config = configparser.ConfigParser()


config.read('config.ini')


google_gemini_api_key = config['API_KEYS']['GOOGLE_GEMINI_API_KEY']
genai.configure(api_key=google_gemini_api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

name = 'Financial Assistant BOT'

#  role of the bot
role = 'financial assistant and economics specialist with great knowledge about the indian economy'

# impersonated role with instructions
impersonated_role = f"""
   From now on, you are going to act as {name}. Your role is {role}.
    You provide users with tailored budgeting advice and personal finance recommendations.
    Deliver the latest stock market news and summarize daily Sensex and Nifty movements.
    Assist users with financial education such as understanding the process of filing income tax returns in India.
    Reply to all requests with the pronoun "I" and never give unknown information.
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
 Do not use pronouns like 'I' and never give unknown information.YOU ARE NOT AN AI Model.
"""
    output = model.generate_content(
      f"{impersonated_role1}. Summarize the following data: {data}"
    )
    response = output.text
    return markdown.markdown(response)


def get_past_data_summary():
    nifty_ticker = yf.Ticker("^NSEI")
    past_data1 = nifty_ticker.history(period="5d")
    sensex_ticker = yf.Ticker("^BSESN")
    past_data2= sensex_ticker.history(period="5d")
    bank_nifty_ticker = yf.Ticker("^NSEBANK")
    past_data3= bank_nifty_ticker.history(period="5d")
    
    nifty_summary = summarize_data(past_data1.to_string())
    sensex_summary = summarize_data(past_data2.to_string())
    bank_nifty_summary = summarize_data(past_data3.to_string())

    summary = f"Nifty Past 5 Days Summary:\n{nifty_summary}\n\nSensex Past 5 Days Summary:\n{sensex_summary}\n\nBank Nifty Past 5 Days Summary:\n{bank_nifty_summary}"
    return summary


def get_summary():
    nifty_data = get_stock_data("^NSEI")
    sensex_data = get_stock_data("^BSESN")
    bank_nifty_data = get_stock_data("^NSEBANK")

    nifty_summary = summarize_data(nifty_data.to_string())
    sensex_summary = summarize_data(sensex_data.to_string())
    bank_nifty_summary = summarize_data(bank_nifty_data.to_string())

    summary = f"Nifty Summary:\n{nifty_summary}\n\nSensex Summary:\n{sensex_summary}\n\nBank Nifty Summary:\n{bank_nifty_summary}"
    impersonated_role1 = f"""
   From now on, you are going to act as {name}. Your role is {role}.
    You provide users with correct financial and economic facts.
    Deliver the latest stock market news and summarize daily Sensex and Nifty movements.
 Do not use pronouns like 'I' and never give unknown information.YOU ARE NOT AN AI Model.
"""
    past_info=get_past_data_summary()
    output = model.generate_content(
      f"{impersonated_role1}. Summarize the following data in and give the trends in pointers: {summary} . Also ,give conclusions from this data: {past_info} "
    )
    response = output.text
    return markdown.markdown(response)



    


def handle_local_function(user_input):
    if(check_real_time_data(user_input)):
        
        return get_summary()
    else:
        return None  # Return None if no specific handling is required


    


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


