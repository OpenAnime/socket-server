const socket = io('http://127.0.0.1:3581');
socket.on('connect', () => {
    alert('bağlandı');
});

function connect() {
    socket.emit('join_room', {
        name: document.querySelector('#username').value.trim(),
        roomname: document.querySelector('#roomID').value.trim(),
        location: window.location.href,
        creator_options: {
            currently_watching: 'Nothing', 
        },
    });
}

socket.on('send_data', (data) => {
    alert(`connected to room ${data.roomname} ${socket.id}`);
});

function sendMessage() {
    socket.emit(
        'server_message',
        document.querySelector('#messageContent').value,
    );
}

socket.on('client_message', (data) => {
    let cr = document.createElement('p');
    cr.innerHTML = data.author + ': ' + data.message_content;
    document.querySelector('#chatBar').appendChild(cr);
});
