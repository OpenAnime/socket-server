class User:
    def __init__(self, sid, name, roomname, currently_watcing) -> None:
        self.sid = sid
        self.name = name
        self.roomname = roomname
        self.currently_watching = currently_watcing
        self.create_options = {"currently_watching": currently_watcing}


class UserManager:
    def __init__(self) -> None:
        self.users: list[User] = []

    def join_user(self, *args):
        user = User(*args)

        self.users.append(user)

        return user

    def remove_user(self, id) -> None:
        self.users = [i for i in self.users if i.sid != id]

    def get_user(self, sid) -> list[User]:
        for i in self.users:
            if i.sid == sid:
                return i
        return None

    def get_room_users(self, roomname) -> list[User]:
        return [i for i in self.users if i.roomname == roomname]
