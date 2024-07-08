function submitUserMessage(event) {
    event.preventDefault();
    const userInput = document.getElementById('user-msg').value;
    addUserMessage(userInput);
    getBotResponse(userInput);
    document.getElementById('user-msg').value = '';
}

function addUserMessage(message) {
    var chatContainer = document.getElementById('chat-container');
    var userDiv = document.createElement('div');
    userDiv.className = 'msg user user-msg';
    userDiv.innerHTML = message;
    chatContainer.appendChild(userDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addBotMessage(message) {
    var chatContainer = document.getElementById('chat-container');
    var botDiv = document.createElement('div');
    botDiv.className = 'msg bot bot-msg';
    botDiv.innerHTML = message;
    chatContainer.appendChild(botDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function getBotResponse(userInput) {
    fetch(`/get?msg=${encodeURIComponent(userInput)}`)
        .then(response => response.text())
        .then(data => addBotMessage(data));
}