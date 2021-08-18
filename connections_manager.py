from typing import Dict, final

from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from nanoid import generate as generate_nanoid

from commands import Commands


class ConnectionsManager:
    _NANOID_ALPHABET = '0123456789'
    _ID_LENGTH = 5

    def __init__(self) -> None:
        self._initiator: WebSocket = None
        self._subscribers: Dict[int, WebSocket] = {}

    def _generate_subscriber_id(self) -> int:
        generated_id = int(generate_nanoid(self._NANOID_ALPHABET, self._ID_LENGTH))
        while generated_id in self._subscribers:
            generated_id = int(generate_nanoid(self._NANOID_ALPHABET, self._ID_LENGTH))
        return generated_id

    async def _connect_initiator(self, websocket: WebSocket) -> None:
        self._initiator = websocket
        await self._initiator.accept()
        await self._listen_initiator()

    async def _connect_subscriber(self, websocket: WebSocket):
        subscriber_id = self._generate_subscriber_id()
        self._subscribers[subscriber_id] = websocket
        await websocket.accept()
        await self._listen_subscriber(websocket, subscriber_id)

    async def accept_connection(self, websocket: WebSocket, is_initiator: bool) -> None:
        if is_initiator and not self._initiator:
            await self._connect_initiator(websocket)
        elif not is_initiator:
            await self._connect_subscriber(websocket)
        else:
            websocket.close()

    async def _notify_subscribers(self, signal: bytes) -> None:
        for subscriber_id, subscriber in self._subscribers.items():
            try:
                await subscriber.send_bytes(signal)
            except ConnectionClosed:
                await subscriber.close()
                self._subscribers.pop(subscriber_id)

    async def _listen_initiator(self):
        try:
            if len(self._subscribers) == 0:
                await self._notify_subscribers(Commands.OUT_OF_CLIENTS.value)

            await self._notify_subscribers(Commands.INITIATOR_CONNECTED.value)

            while True:
                signal = await self._initiator.receive_bytes()
                await self._notify_subscribers(signal)

        except WebSocketDisconnect:
            self._initiator = None
        finally:
            await self._initiator.close()
            await self._notify_subscribers(Commands.INITIATOR_DISCONNECTED.value)

    async def _listen_subscriber(self, websocket: WebSocket, subscriber_id: int):
        try:
            if not self._initiator:
                await self._notify_subscribers(Commands.INITIATOR_DISCONNECTED.value)
            else:
                await self._initiator.send_bytes(Commands.INITIATOR_CONNECTED.value)

            while True:
                signal = await websocket.receive_bytes()
                print(f'Client {subscriber_id} sent: {int.from_bytes(signal, "big", signed=False)}')

        except WebSocketDisconnect:
            self._subscribers.pop(subscriber_id)
        finally:
            await websocket.close()
            await self._initiator.send_bytes(Commands.CLIENT_DISCONNECTED.value)
