# from flask import Flask, render_template, request, redirect
# from tabulate import tabulate
# import google.generativeai as genai
# import os
# import time
# import configparser

# # Create a ConfigParser object
# config = configparser.ConfigParser()

# # Read the configuration file
# config.read('config.ini')

# # Set the Google Gemini API key
# google_gemini_api_key = config['API_KEYS']['GOOGLE_GEMINI_API_KEY']
# genai.configure(api_key=google_gemini_api_key)



# model = genai.GenerativeModel('gemini-1.5-flash')
# # response = model.generate_content('Define Budget')
# # print(response.text)

# # Define the name of the bot
# name = 'Financial Assistant BOT'

# # Define the role of the bot
# role = 'financial assistant'

# # Define the impersonated role with instructions
# impersonated_role = f"""
#    From now on, you are going to act as {name}. Your role is {role}.
#     You provide users with tailored budgeting advice and personal finance recommendations.
#     Deliver the latest stock market news and summarize daily Sensex and Nifty movements.
#     Assist users with financial education such as understanding the process of filing income tax returns in India.
#     Efficiently address common financial queries using the integrated FAQ model.
#     Reply to all requests with the pronoun "I" and never give unknown information. Forward users to the website for more information when necessary.
#     YOU ARE NOT AN AI MODEL!
# """

# # Initialize variables for chat history
# explicit_input = ""
# chat_output = 'Chat log: /n'
# cwd = os.getcwd()
# i = 1

# # Find an available chat history file
# while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
#     i += 1

# history_file = os.path.join(cwd, f'chat_history{i}.txt')

# # Create a new chat history file
# with open(history_file, 'w') as f:
#     f.write('\n')

# # Initialize chat history
# chat_history = ''

# # Create a Flask web application
# app = Flask(__name__)

# # Function to complete chat input using Google Gemini
# def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
#     output = model.generate_content(
#        f"{impersonated_role}. Conversation history: {chat_history} User: {user_input}. {explicit_input}",
#     )

#     # chat_output = output.text
#     chat_output = tabulate.to_markdown(output.text)
   
#     return chat_output

# # Function to handle user chat input
# def chat(user_input):
#     global chat_history, name, chat_output
#     current_day = time.strftime("%d/%m", time.localtime())
#     current_time = time.strftime("%H:%M:%S", time.localtime())
#     chat_history += f'\nUser: {user_input}\n'
#     chat_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
#     chat_output = f'{name}: {chat_raw_output}'
#     chat_history += chat_output + '\n'
#     with open(history_file, 'a') as f:
#         f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chat_output + '\n')
#         f.close()
#     return chat_raw_output

# # Function to get a response from the chatbot
# def get_response(userText):
#     return chat(userText)

# # Define app routes
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/get")
# # Function for the bot response
# def get_bot_response():
#     userText = request.args.get('msg')
#     return str(get_response(userText))

# @app.route('/refresh')
# def refresh():
#     time.sleep(60) # Wait for 1 minutes
#     return redirect('/refresh')

# # Run the Flask app
# if __name__ == "__main__":
#     app.run()



from flask import Flask, render_template, request, redirect
from tabulate import tabulate
import google.generativeai as genai
import os
import time
import configparser
import markdown

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
role = 'financial assistant'

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
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)

# Function to complete chat input using Google Gemini
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = model.generate_content(
       f"{impersonated_role}. Conversation history: {chat_history} User: {user_input}. {explicit_input}",
    )

    chat_output = output.text
    return chat_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chat_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chat_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chat_output = f'{name}: {chat_raw_output}'
    chat_history += chat_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chat_output + '\n')
        f.close()
    return chat_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    response = get_response(userText)
    response_md = markdown.markdown(response)
    return response_md

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
