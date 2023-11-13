import asyncio
from loguru import logger

import websockets

from server.commands import ServerCommand
from server.user import ChatUser, Message

hello_message = (
    "Available commands:\n"
    "/send <message> - send message to all users\n"
    "/send <username> <message> - send message to specific user\n"
    "/status - show online users\n"
    "/history - show last 20 messages\n"
    "/rename <new_username> - change your username\n"
    "/report <username> - report user\n"
    "/quit - disconnect from server\n"
)


class Server:
    def __init__(self, host="127.0.0.1", port=8000, message_cnt=20):
        self.host = host
        self.port = port
        self.users = {}
        self.message_cnt = message_cnt
        self.history = []

    async def start(self) -> None:
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()

    def get_all_users(self):
        websockets_list = []

        for user in self.users.values():
            websockets_list.append(user.ws)

        return websockets_list

    def get_user_by_name(self, name: str) -> ChatUser | None:
        if name in self.users:
            return self.users[name]
        return None

    async def handler(self, websocket: websockets.WebSocketServerProtocol):
        user = ChatUser(websocket, self)
        await user.send_message(hello_message, with_prefix=False)
        self.users[user.username] = user

        try:
            while True:
                message = await websocket.recv()

                if not message:
                    logger.debug("Empty message")
                    break

                msg_object = Message.parse(message)
                update = ServerCommand.handle(msg_object, self.users[user.username])

                if not update:
                    break

                asyncio.create_task(update)
        except Exception as ex:
            logger.debug(ex)
        finally:
            logger.debug("User disconnected")
            del self.users[user.username]
