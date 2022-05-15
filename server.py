import socketio
from aiohttp import web
from user_manager import UserManager


HOST = "127.0.0.1"
PORT = 3581

sio = socketio.AsyncServer(
    async_mode="aiohttp", logger=False, engineio_logger=False, cors_allowed_origins="*"
)

app = web.Application()
sio.attach(app)

user_manager = UserManager()


@sio.event
async def connect(sid, environ):
    print("connect", sid)


@sio.event
async def join_room(sid, data):
    s_user = user_manager.get_user(sid)
    room_users = user_manager.get_room_users(data["roomname"])

    if s_user is not None:
        user_manager.remove_user(sid)

    if len(room_users) == 0:
        new_user = user_manager.join_user(
            sid, data["name"], data["roomname"], data["location"]
        )
    else:
        new_user = user_manager.join_user(sid, data["name"], data["roomname"], None)
        opts = [
            i for i in user_manager.users if i["creater_options"]["currently_watching"]
        ]

        await sio.emit(
            "change_location",
            {
                "change_to": opts["create_options"]["currently_watching"],
            },
        )

    await sio.emit(
        "send_data",
        {"id": sid, "username": new_user.name, "roomname": new_user.roomname},
    )


@sio.event
async def change_video_status(sid, data):
    user = user_manager.get_user(sid)
    if user is not None:
        await sio.emit("video_status_changed", data, room=user.roomname)
    else:
        print("User not found")


@sio.event
async def server_message(sid, data):
    print(data)
    user = user_manager.get_user(sid)
    if user is not None:
        await sio.emit(
            "client_message",
            {"message_content": data, "author": user.name},
            room=user.roomname,
        )


@sio.event
async def disconnect(sid):
    user_manager.remove_user(sid)


if __name__ == "__main__":
    web.run_app(app, host=HOST, port=PORT)
