from typing import Dict

from fastapi import WebSocket
from nanoid import generate as generate_nanoid

from .singleton import Singleton
from . import Room


class RoomsManager(metaclass=Singleton):
    _NANOID_ALPHABET = '0123456789'
    _NANOID_LENGTH = 6
    
    _rooms: Dict[int, Room] = {}

    def init_room(self) -> int:
        room_id = int(generate_nanoid(self._NANOID_ALPHABET, self._NANOID_LENGTH))
        while self._rooms.get(room_id):
            room_id = generate_nanoid(self._NANOID_ALPHABET, self._NANOID_LENGTH)
    
        self._rooms[room_id] = Room(room_id)
        return room_id

    def close_room(self, room: Room):
        self._rooms.pop(room.room_id, None)

    async def accept_connection(self, websocket: WebSocket, room_id: int, is_initiator: bool):
        room = self._rooms.get(room_id)

        if not room:
            await websocket.close()
            return
            
        await room.connect(websocket, is_initiator)
