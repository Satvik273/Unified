const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const port = 3000;

app.use(express.static(__dirname));

let users = {};

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('joinRoom', ({ username, room }) => {
        socket.join(room);
        users[socket.id] = { username, room };
        io.to(room).emit('message', { user: 'System', text: `${username} has joined the room.` });
    });

    socket.on('sendMessage', (message) => {
        const user = users[socket.id];
        if (user) {
            io.to(user.room).emit('message', { user: user.username, text: message, time: new Date().toLocaleTimeString() });
        }
    });

    socket.on('disconnect', () => {
        const user = users[socket.id];
        if (user) {
            io.to(user.room).emit('message', { user: 'System', text: `${user.username} has left the room.` });
            delete users[socket.id];
        }
    });
});

http.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
