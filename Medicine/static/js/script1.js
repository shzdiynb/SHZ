function sendMessage() {
    var userInput = document.getElementById("user-input");
    var userMessage = userInput.value;

    if (userMessage.trim() === "") {
        return;
    }

    appendMessage("user", userMessage);
    userInput.value = "";

    // Simulate bot response (replace with actual backend integration)
    setTimeout(function() {
        var botMessage = "I'm sorry, I can't answer that right now.";
        appendMessage("bot", botMessage);
    }, 500);
}

function appendMessage(sender, message) {
    var chatBox = document.getElementById("chat-box");
    var messageElem = document.createElement("div");
    messageElem.classList.add("chat-message", sender);
    messageElem.innerHTML = `<span class="message">${message}</span>`;
    chatBox.appendChild(messageElem);

    // Scroll to bottom of chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}
