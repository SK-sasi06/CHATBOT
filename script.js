// script.js — frontend logic
const messagesEl = document.getElementById('messages');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');

// Conversation array sent to server; keep roles: 'user' or 'model'
let conversation = [];

function addMessage(role, text) {
    const el = document.createElement('div');
    el.className = `message ${role === 'user' ? 'user' : 'bot'}`;
    el.textContent = text;
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    // show user message
    addMessage('user', text);
    conversation.push({ role: 'user', text });
    input.value = '';

    // add a temporary 'typing' placeholder
    const loadingEl = document.createElement('div');
    loadingEl.className = 'message bot';
    loadingEl.textContent = '...';
    messagesEl.appendChild(loadingEl);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
        // Call backend — replace host if opening index.html directly
        const res = await fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: conversation })
        });

        const data = await res.json();
        // remove placeholder
        messagesEl.removeChild(loadingEl);

        if (data.error) {
            addMessage('bot', `Error: ${data.error}`);
            console.error(data.error);
            return;
        }

        const reply = data.reply || '';
        addMessage('bot', reply);
        conversation.push({ role: 'model', text: reply });

    } catch (err) {
        messagesEl.removeChild(loadingEl);
        addMessage('bot', 'Network error — check console');
        console.error(err);
    }
});
