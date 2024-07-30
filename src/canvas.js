const socket = io();
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
const chatBox = document.getElementById('chatBox');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const usersList = document.getElementById('users');
const startButton = document.getElementById('startButton');
let drawing = false;
let canDraw = false;

// Capture the username from the server-side
const username = "{{ username }}";  // Get username from Flask server

canvas.addEventListener('mousedown', (e) => {
    if (canDraw) startDrawing(e);
});
canvas.addEventListener('mouseup', (e) => {
    if (canDraw) stopDrawing();
});
canvas.addEventListener('mousemove', (e) => {
    if (canDraw) draw(e);
});

function startDrawing(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function stopDrawing() {
    drawing = false;
}

function draw(e) {
    if (!drawing) return;

    const x = e.clientX - canvas.offsetLeft;
    const y = e.clientY - canvas.offsetTop;

    ctx.lineTo(x, y);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Emit draw event with the coordinates
    socket.emit('draw', { x, y });
}

// Listen for draw events from the server
socket.on('draw', (data) => {
    ctx.lineTo(data.x, data.y);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.stroke();
});

// Send message on button click
sendButton.addEventListener('click', sendMessage);

// Send message on enter key press
chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = chatInput.value;
    if (message.trim() !== '') {
        // Send the message along with the username
        socket.emit('chat', { username, message });
        chatInput.value = ''; // Clear the input field
    }
}

// Listen for chat messages from the server
socket.on('chat', (data) => {
    const { username, message } = data;
    const messageElement = document.createElement('div');
    messageElement.textContent = `${username}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
});

// Listen for user list updates from the server
socket.on('user_list', (users) => {
    usersList.innerHTML = ''; // Clear the list
    users.forEach((user) => {
        const userElement = document.createElement('li');
        userElement.textContent = user;
        usersList.appendChild(userElement);
    });
});

// Notify the server of a new user
socket.emit('new_user', username);

// Notify the server of a user disconnect
window.addEventListener('beforeunload', () => {
    socket.emit('disconnect_user', username);
});

// Start the game when the "Start Game" button is clicked
startButton.addEventListener('click', () => {
    console.log('Start game button clicked');
    socket.emit('start_game');
});

// Listen for turn updates from the server
socket.on('turn', (data) => {
    const currentDrawer = data;
    console.log('inside turn method');
    canDraw = (currentDrawer === username); // Only the current user can draw
});
