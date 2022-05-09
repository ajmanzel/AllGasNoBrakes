var socket = new WebSocket("ws://" + window.location.hostname + ":" + window.location.port + "/ws")

socket.onmessage = function (event) {
    const json_data = JSON.parse(event.data);
    const message = json_data.message
    const messageType = json_data.messageType

    switch (messageType) {
        case 'add':
            active_users = document.getElementById("active_users")

            new_user = document.createElement("p");
            new_user.setAttribute('id', message)
            new_user.innerHTML = message

            active_users.appendChild(new_user)
            break
        case 'remove':
            del_user = document.getElementById(message)
            del_user.remove()
            break
        case 'active_users':
            active_users = document.getElementById("active_users")

            for (const user of message) {
                const new_user = document.createElement("p");
                new_user.setAttribute('id', user)
                new_user.innerHTML = user

                active_users.appendChild(new_user)
            }
            break
        default:
            console.log("received an invalid WS messageType: " + messageType);
    }
}