import socketio
from aiohttp import web
from user_manager import UserManager

from utils import check_join_data

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
    is_data_valid = check_join_data(data)

    if not is_data_valid:
        return

    s_user = user_manager.get_user(sid)

    if s_user is not None:
        user_manager.remove_user(sid)
        sio.leave_room(sid, s_user.roomname)

    room = user_manager.check_room(data["roomname"])

    if not room:
        new_user = user_manager.join_user(
            sid, data["name"], data["roomname"], data["location"]
        )
    else:
        new_user = user_manager.join_user(sid, data["name"], data["roomname"], None)
        opts = [i for i in user_manager.users if i.create_options["currently_watching"]]

        if len(opts) < 1:
            return

        await sio.emit(
            "change_location",
            {
                "change_to": opts[0].create_options["currently_watching"],
            },
        )

    sio.enter_room(sid, data["roomname"])
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
