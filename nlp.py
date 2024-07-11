import spacy

# Load the English NLP model from spaCy
nlp = spacy.load('en_core_web_sm')

def check_real_time_data(user_input):
    # Define keywords or patterns indicating real-time data requests
    keywords = ['current', 'latest', 'now', 'live', 'today', 'right-now', 'real-time']
    negations = ['not', 'n\'t', 'no']

    # Process user input using spaCy
    doc = nlp(user_input.lower())  # Convert to lowercase for case-insensitive matching
    
    # Check for direct keyword matches
    for token in doc:
        if token.text in keywords:
            return True
    
    # Check for more complex patterns using dependency parsing
    for token in doc:
        if token.dep_ == 'prep' and token.head.text in keywords:
            return True
        if token.dep_ == 'advmod' and token.head.text in keywords:
            return True
    
    # Handle negations
    for token in doc:
        if token.text in negations:
            for child in token.children:
                if child.text in keywords:
                    return False  # Negation followed by a keyword indicates absence of real-time request

    return False

# # Example usage:
# user_input1 = "What is the current price of Bitcoin?"
# user_input2 = "Show me the latest news updates."
# user_input3 = "What is today's nifty trend?"
# user_input4 = "Not now, I don't need the latest updates."

# print(check_real_time_data(user_input1))  # Output: True
# print(check_real_time_data(user_input2))  # Output: True
# print(check_real_time_data(user_input3))  # Output: True
# print(check_real_time_data(user_input4))  # Output: False
