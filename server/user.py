from datetime import datetime, timedelta
import random


class ChatUser:
    def __init__(self, ws, server) -> None:
        self.ws = ws
        self.username = "User_" + str(random.randint(0, 1000))
        self.is_banned = False
        self.reports = set()
        self.server = server
        self.unban_time = None
        self.msg_count = 0

    @staticmethod
    def format_date() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def check_ban(self) -> None:
        if self.is_banned and self.unban_time and datetime.now() >= self.unban_time:
            self.is_banned = False
            self.unban_time = None
            self.reports.clear()

        if self.msg_count >= 20:
            self.is_banned = True
            self.unban_time = datetime.now() + timedelta(hours=1)
            self.msg_count = 0

    async def send_message(self, message: str, with_prefix: bool = True) -> None:
        self.msg_count += 1
        if with_prefix:
            message = f"{self.format_date()} {message}"
        return await self.ws.send(message)

    def set_username(self, username: str) -> None:
        self.username = username

    def add_report(self, sender: "ChatUser") -> None:
        self.reports.add(sender)

        if len(self.reports) >= 3:
            self.is_banned = True
            self.unban_time = datetime.now() + timedelta(hours=4)

    async def broadcast(self, message: str) -> None:
        for user in self.server.get_all_users():
            await user.send(message)


class Message:
    def __init__(self, command="", data="", target=None):
        self.command = command
        self.data = data
        self.target = target

    @classmethod
    def parse(cls, data):
        if data.startswith("/"):
            data = data.split(" ", 2)
            return cls(*data)

        return cls("/send", data)
