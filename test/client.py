import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("connection established")
    await sio.emit(
        "join_room",
        {
            "roomname": "test_room",
            "name": "test_name",
            "location": "idk what is this",
            "creator_options": {
                "currently_watching": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
        },
    )
    await sio.emit("server_message", "Hello World")


@sio.event
async def client_message(data):
    print("message received with ", data)
    await sio.emit("my response", {"response": "my response"})


@sio.event
async def disconnect():
    print("disconnected from server")


async def main():
    await sio.connect("http://127.0.0.1:3581")
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
