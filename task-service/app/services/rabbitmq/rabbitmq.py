import asyncio

from typing import List
from starlette.websockets import WebSocket
from aio_pika import connect, Message, IncomingMessage
from app.core.config import settings

class Notifier:
    def __init__(self):
        self.connections: WebSocket
        self.is_ready = False
        self.tag: str

    async def setup(self, queue_name: str):
        self.rmq_conn = await connect(
            f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}/",
            loop=asyncio.get_running_loop()
        )
        self.queue_name = queue_name

        self.channel = await self.rmq_conn.channel()
        self.queue = await self.channel.declare_queue(self.queue_name)
        await self.queue.consume(self._notify, no_ack=True)
        self.is_ready = True

    async def push(self, msg: str):
        await self.channel.default_exchange.publish(
            Message(msg.encode("utf-8")),
            routing_key=self.queue_name,
        )

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections = websocket

    async def remove(self):
        self.connections.close()
        self.rmq_conn.close()
        
    async def _notify(self, message: IncomingMessage):
        try:
            await self.connections.send_text(message.body.decode('utf-8'))
        except:
            pass
