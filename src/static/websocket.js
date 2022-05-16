var socket = new WebSocket(
    "ws://" + window.location.hostname + ":" + window.location.port + "/ws"
  );
var chatModal = $("#chatModal");
var messageBox = $("#messageBox");
var modalTitle = $(".modal-title");
var modalBodyInput = $(".modal-body");
var recipient = "";
var modalOpen = false;
var messages = {} // dict of stacks
var audio = ""

$('document').ready(function () {
    audio = new Audio();
    audio.src = "https://www.soundjay.com/buttons/beep-08b.mp3"
});

function findStats(e) {
    e.preventDefault();
    var steamID = $('#steamID').val()

    this.action = '/profile/' + steamID
    this.submit()
}

$('#csgo-data').submit(findStats)


function createUserElement(username) {
active_users = $("#active_users");

new_user = $(
  '<li style="list-style-type: none;" id="' +
    username +
    '"> <image width="64" height="56" src="/api/profile/' + username + '" /> <a href="#" data-bs-recipient="' +
    username +
    '" data-bs-toggle="modal" data-bs-target="#chatModal" class="h4">' +
    username +
    "</a></li>"
);

active_users.append(new_user);
}

socket.onmessage = function (event) {
const json_data = JSON.parse(event.data);
const message = json_data.message;
const messageType = json_data.messageType;

switch (messageType) {
  case "add":
    createUserElement(message);
    break;
  case "remove":
    del_user = $('#' + message)
    console.log(del_user)
    del_user.remove();
    break;
  case "active_users":
    for (const user of message) {
      createUserElement(user);
    }
    break;
  case "receive_message":
      var sender = message.sender
      var msg = message.msg

      if (messages[sender])
          messages[sender].push(sender + ": " + msg)
      else
          messages[sender] = [sender + ": " + msg]

      if (sender === recipient)
        modalBodyInput.append("<p>" + sender + ": " + msg + "</p>")
      else {
        var sender_link = $("a[data-bs-recipient='" + sender + "']")
        sender_link.css("font-weight","Bold")
        audio.play();
    }
      console.log("Message from " + sender + ": " + msg)
      break;
  case "vote":
    var comment_id = message.comment_id
    var vote = message.vote
    console.log(comment_id)
    console.log(vote)

    if (vote === 'upvote') {
        var label = $('#upvote-label-' + comment_id)
        var count = parseInt(label.text())
        label.text(count + 1)
    }
    else {
        var label = $('#downvote-label-' + comment_id)
        var count = parseInt(label.text())
        label.text(count + 1)
    }
    break;
  default:
    console.log("received an invalid WS messageType: " + messageType);
}
};

$(chatModal).on("hidden.bs.modal", function (event) {
    recipient = ''
});

$(chatModal).on("show.bs.modal", function (event) {
var modal_trigger_element = $(event.relatedTarget);
modal_trigger_element.css("font-weight","normal")
modalBodyInput.html('')

recipient = modal_trigger_element.attr("data-bs-recipient");

var msgs = messages[recipient]
if (msgs) {
    for (const m of msgs) {
    modalBodyInput.append("<p>" + m + "</p>")
    }
}

modalTitle.text("Chatting with " + recipient);
});

$(chatModal).on("keypress", function (event) {
if (event.key == "Enter") {
  var msg = messageBox.val();
  messageBox.val("");
  messageBox.focus();

  ws_message = {"messageType": "send_message", "message": {"recipient": recipient, "msg": msg}}

  socket.send(JSON.stringify(ws_message))
  $(".modal-body").append("<p>Me: " + msg + "</p>")

  if (messages[recipient])
      messages[recipient].push("Me: " + msg)
  else
      messages[recipient] = ["Me: " + msg]
  console.log(messages)
  // then add the message to the messages cache stack
}
});

function sendVote(comment_id, vote) {
    ws_message = {"messageType": "vote", "message": {"comment_id": comment_id, "vote": vote}}
    socket.send(JSON.stringify(ws_message))
}