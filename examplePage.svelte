<script>

import io from "../../public/build/socket"
const socket = io("http://127.0.0.1:3581");
socket.on("connect", () => {
 alert("bağlandı")
})

function connect() {
 socket.emit("join_room", {
    name: document.querySelector("#username").value,
    roomname: document.querySelector("#roomID").value,
    location: window.location.href, //for identifying the user is room creator or not
    creator_options: {
     currently_watching: null
    }
  })
}

socket.on("send_data", (data) => {
 alert(`connected to room ${data.roomname}`)
})

function sendMessage() {
socket.emit("server_message", document.querySelector("#messageContent").value)
}

socket.on("client_message", (data) => {
 let cr = document.createElement("p")
 cr.innerHTML = data.author + ": " + data.message_content
 document.querySelector("#chatBar").appendChild(cr)
})

</script>

<style>
 #chatBar {
  height: 20rem;
  overflow: scroll;
  width: 30rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: pink;
 }
</style>

<input type="text" id="username">
<div id="chatBar">

</div>
<input type="text" id="messageContent">
<button id="send" on:click={() => sendMessage()}>Send</button>
<input type="text" id="roomID">
<button id="connect" on:click={() => connect()}>Connect</button>
