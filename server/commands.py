from server.user import Message, ChatUser


class ServerCommand:
    commands = {}

    @classmethod
    def append(cls, command: str):
        def decorator(func):
            cls.commands[command] = func
            return func

        return decorator

    @classmethod
    def handle(cls, message: Message, user: ChatUser):
        if message.command not in cls.commands:
            return
        handler = cls.commands[message.command]
        return handler(message, user)


@ServerCommand.append("/send")
async def send(message: Message, user: ChatUser):
    user.check_ban()

    if user.is_banned:
        if user.unban_time:
            await user.send_message(
                f"You are banned until {user.unban_time}", with_prefix=True
            )
        return

    msg_data = message.data

    if not message.target:
        send_data = f"[{user.username}]: {msg_data}"
        user.server.history.append(send_data)
        await user.broadcast(send_data)
        return

    target = message.target
    target_user = user.server.get_user_by_name(target)

    if target_user:
        send_data = f"[{user.username}]: {msg_data}"
        await target_user.send_message(send_data)
        await user.send_message(send_data)


@ServerCommand.append("/status")
async def status(message: Message, user: ChatUser):
    answer = "Users online:\n"
    for user in user.server.users.values():
        answer += f"{user.username}\n"

    await user.send_message(answer, with_prefix=False)


@ServerCommand.append("/history")
async def history(message: Message, user: ChatUser):
    server_history = user.server.history[-user.server.message_cnt :]
    server_history = "\n".join(server_history)
    await user.send_message(server_history, with_prefix=False)


@ServerCommand.append("/rename")
async def rename(message: Message, user: ChatUser):
    new_name = message.data
    old_name = user.username
    user.set_username(new_name)
    user.server.users[new_name] = user
    del user.server.users[old_name]
    await user.send_message(f"You changed your name to {new_name}", with_prefix=True)
    await user.broadcast(f"User {old_name} changed his name to {new_name}")


@ServerCommand.append("/report")
async def report(message: Message, user: ChatUser):
    target = message.data
    target_user = user.server.get_user_by_name(target)

    if not target_user:
        await user.send_message(f"User {target} not found")
        return

    target_user.add_report(user)
    await user.send_message(f"User {target} reported", with_prefix=True)
    await target_user.send_message(
        f"User {user.username} reported you", with_prefix=True
    )
