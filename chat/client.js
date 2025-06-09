const socket = io();

const params = new URLSearchParams(window.location.search);
const username = params.get('username');
const room = params.get('room');

socket.emit('joinRoom', { username, room });

socket.on('message', (message) => {
    displayMessage(message);
});

function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('sendMessage', message);
        messageInput.value = '';
    }
}

function displayMessage({ user, text, time }) {
    const chatWindow = document.getElementById('chat-window');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = `<strong>${user}:</strong> ${text} <span class="timestamp">${time || ''}</span>`;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}
