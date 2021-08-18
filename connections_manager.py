from typing import Dict
from fastapi.responses import JSONResponse

from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from nanoid import generate as generate_nanoid

from commands import Commands


class ConnectionsManager:
    """Processes connections & messages passing"""

    def __init__(self) -> None:
        self._initiator: WebSocket = None
        self._subscribers: Dict[int, WebSocket] = {}

    def _generate_subscriber_id(self) -> int:
        """Generates nanoid untill it is unique. Generated nanoid converts to int identifier for new client connection.

        Returns:
            int: generated unique nanoid
        """
        generated_id = int(generate_nanoid('0123456789', 5))
        while generated_id in self._subscribers:
            generated_id = int(generate_nanoid(self._NANOID_ALPHABET, self._ID_LENGTH))
        return generated_id

    async def _connect_initiator(self, websocket: WebSocket) -> None:
        """Accepts initiator websocket connection and runs initiator connection listener. 

        Args:
            websocket (WebSocket): initiator's websocket connection
        """
        self._initiator = websocket
        await self._initiator.accept()
        await self._listen_initiator()

    async def _disconnect_initiator(self) -> None:
        """Closes initiator's websocket and sets self._initiator to None."""
        await self._initiator.close()
        self._initiator = None

    async def _connect_subscriber(self, websocket: WebSocket) -> None:
        """Assigns id to client's connection? accepts its connection and initiates connection listening.

        Args:
            websocket (WebSocket): client's websocket connection
        """
        subscriber_id = self._generate_subscriber_id()
        self._subscribers[subscriber_id] = websocket
        await websocket.accept()
        await self._listen_subscriber(websocket, subscriber_id)

    async def _disconnect_subscriber(self, subscriber_id: int) -> None:
        """Closes client's websocket & removes it from subscribers dict.

        Args:
            subscriber_id (int): client's connection id
        """
        subscriber_websocket = self._subscribers.pop(subscriber_id)
        await subscriber_websocket.close()

    async def accept_connection(self, websocket: WebSocket, is_initiator: bool) -> None:
        """Checks conditions to accept incomming websocket conection.

        Args:
            websocket (WebSocket): incomming websocket connection
            is_initiator (bool): incomming connection's initiator flag
        """
        if is_initiator and not self._initiator:
            await self._connect_initiator(websocket)
        elif not is_initiator:
            await self._connect_subscriber(websocket)
        else:
            websocket.close()

    async def _notify_subscribers(self, signal: bytes) -> None:
        """Broadcasts signal to subscribers.

        Args:
            signal (bytes): signal to be broadcasted to subscribers
        """
        for subscriber_id, subscriber in self._subscribers.items():
            try:
                await subscriber.send_bytes(signal)
            except Exception as e:
                if not isinstance(e, ConnectionClosed):
                    print(type(e), e)
                await self._disconnect_subscriber(subscriber_id)
                
    async def _notify_initiator(self, signal: bytes) -> None:
        """Sends signal to initiator.

        Args:
            signal (bytes): signal to be sent to initiator
        """
        try:
            if self._initiator:
                await self._initiator.send_bytes(signal)

        except Exception as e:
            if not isinstance(e, ConnectionClosed):
                print(type(e), e)
            await self._disconnect_initiator()

    async def _notify_initiator_with_json(self, data: dict) -> None:
        """Sends JSON to initiator.

        Args:
            data (dict): dict-like object to be converted to JSON and sent
        """
        try:
            if self._initiator:
                await self._initiator.send_json(data)
        
        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                print(type(e), e)
            await self._disconnect_initiator()

    async def _send_connected_clients_info_to_initiator(self) -> None:
        """Sends information about connected clients to initiator."""
        try:
            await self._notify_initiator(Commands.UPDATE_CLIENTS_STATISTIC.value)
            await self._notify_initiator_with_json({
                'connections': f'{len(self._subscribers)}',
            })
        except Exception as e:
            if not isinstance(e, (WebSocketDisconnect, ConnectionClosed)):
                print(type(e), e)
            await self._disconnect_initiator()

    async def _listen_initiator(self) -> None:
        """Receives & processes initiator's signals."""
        try:
            await self._send_connected_clients_info_to_initiator()
            await self._notify_subscribers(Commands.INITIATOR_CONNECTED.value)

            while True:
                signal = await self._initiator.receive_bytes()
                await self._notify_subscribers(signal)

        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                print(type(e), e)
            await self._disconnect_initiator()
            await self._notify_subscribers(Commands.INITIATOR_DISCONNECTED.value)

    async def _listen_subscriber(self, websocket: WebSocket, subscriber_id: int) -> None:
        """Recieves & and processes subscriber's signals.

        Args:
            websocket (WebSocket): client's websocket connection
            subscriber_id (int): client's connection id
        """
        try:
            if not self._initiator:
                await websocket.send_bytes(Commands.INITIATOR_DISCONNECTED.value)
            else:
                await websocket.send_bytes(Commands.INITIATOR_CONNECTED.value)
            
            await self._send_connected_clients_info_to_initiator()

            while True:
                signal = await websocket.receive_bytes()
                print(f'Client {subscriber_id} sent: {int.from_bytes(signal, "big", signed=False)}')

        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                print(type(e), e)
            await self._disconnect_subscriber(subscriber_id)
            await self._send_connected_clients_info_to_initiator()
