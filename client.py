import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("connection established")
    await sio.emit("server_message", "Hello World")


@sio.event
async def my_message(data):
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
