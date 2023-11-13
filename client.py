import asyncio
import websockets
from aioconsole import ainput


class Client:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.uri = f"ws://{self.host}:{self.port}"
        self._connection = None

    async def __aenter__(self):
        self._connection = await websockets.connect(self.uri)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._connection.close()

    async def handle_and_receive(self):
        tasks = [
            asyncio.create_task(self.send_message()),
            asyncio.create_task(self.receive_message()),
        ]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

    async def send_message(self):
        while True:
            message = await ainput()
            await self._connection.send(message)
            if message == "quit":
                break

    async def receive_message(self):
        try:
            while True:
                message = await self._connection.recv()
                print(message)
        except websockets.ConnectionClosedOK:
            pass


async def main():
    async with Client() as client:
        await client.handle_and_receive()


if __name__ == "__main__":
    asyncio.run(main())
