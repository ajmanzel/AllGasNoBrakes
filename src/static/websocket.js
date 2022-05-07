var socket = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/ws")

function sendMessage(event) {
    console.log('hi');
}

socket.onmessage = function (event) {
    const json_data = JSON.parse(event.data);
    const message = json_data.message
    const messageType = json_data.messageType

    switch (messageType) {
        case 'add':
            active_users = document.getElementById("active_users")

            new_user = document.createElement("a");
            new_user.href = '#'
            new_user.setAttribute('id', message)
            new_user.innerHTML = message
            new_user.onclick = sendMessage;

            active_users.appendChild(new_user)
            break
        case 'remove':
            del_user = document.getElementById(message)
            del_user.remove()
            break
        case 'active_users':
            active_users = document.getElementById("active_users")

            for (const user of message) {
                const new_user = document.createElement("a");
                new_user.setAttribute('id', user)
                new_user.innerHTML = user
                new_user.onclick = console.log("hi");

                active_users.appendChild(new_user)
            }
            break
        default:
            console.log("received an invalid WS messageType: " + messageType);
    }
}