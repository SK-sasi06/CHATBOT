// script.js — Chatbot frontend logic

const messagesEl = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("input");

// Add message to chat window
function addMessage(role, text) {
    const el = document.createElement("div");
    el.className = role === "user" ? "message user" : "message bot";
    el.innerText = text;
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight; // auto-scroll
}

// Handle form submit
form.addEventListener("submit", (e) => {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Show user message
    addMessage("user", userMessage);
    input.value = "";

    // Send to backend
    fetch("https://chatbot-5-gufh.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then((res) => res.json())
    .then((data) => {
        addMessage("bot", data.reply);
    })
    .catch((err) => {
        addMessage("bot", "⚠️ Server error: " + err.message);
    });
});
