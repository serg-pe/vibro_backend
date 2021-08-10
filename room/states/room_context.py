from abc import ABC, abstractmethod

from .room_state import RoomState
from .exceptions import RoomClosedException


class RoomContext(ABC):
    
    _state: RoomState = None

    def __init__(self, state: RoomState):
        self.change_state(state)

    def change_state(self, state: RoomState):
        self._state = state
        self._state.context = self

    async def enter_state(self):
        try:
            while True:
                await self._state.run()
        
        except RoomClosedException:
            pass