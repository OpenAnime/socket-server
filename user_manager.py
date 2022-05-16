class User:
    sid: int
    name: str
    roomname: str
    create_options: dict

    def __init__(
        self, sid=None, name=None, roomname=None, currently_watcing=None
    ) -> None:
        self.sid = sid
        self.name = name
        self.roomname = roomname
        self.create_options = {"currently_watching": currently_watcing}


class UserManager:
    def __init__(self) -> None:
        self.users: list[User] = []

    def join_user(self, *args) -> User:
        user = User(*args)

        self.users.append(user)

        return user

    def remove_user(self, id) -> None:
        self.users = [i for i in self.users if i.sid != id]

    def get_user(self, sid) -> User:
        for i in self.users:
            if i.sid == sid:
                return i
        return None

    def check_room(self, roomname) -> bool:
        for i in self.users:
            if i.roomname == roomname:
                return True
        return False
