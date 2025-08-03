document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.getElementById("messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message !== "") {
            appendMessage(message, "user-message");
            userInput.value = "";

            // Fetch bot response from FastAPI backend
            try {
                const response = await fetch(`http://localhost:8000/query?query=${encodeURIComponent(message)}`);
                const botReply = await response.text();
                appendMessage(botReply, "bot-message");
            } catch (error) {
                appendMessage("Sorry, I couldn't connect to the server.", "bot-message");
            }
        }
    }

    function appendMessage(text, className) {
        const messageWrapper = document.createElement("div");
        messageWrapper.className = className;
        messageWrapper.textContent = text;

        messagesContainer.appendChild(messageWrapper);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });
});
