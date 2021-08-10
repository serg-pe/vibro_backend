from time import time
from asyncio import sleep

from .room_state import RoomState


class EmptyRoomState(RoomState):
    _ACTIVE_TIME = 10

    def __init__(self):
        self._measurements_started = time()

    def _is_room_active(self):
        time_diff = time() - self._measurements_started
        return time_diff < self._ACTIVE_TIME

    async def run(self):
        from . import InitiatorDisconnectedState
        from . import InitiatorRecievingState
        from . import ClosingRoomState
        
        print('Empty Room State')
        while True:
            if not await self.context.is_empty():
                if self.context.initiator:
                    self.context.change_state(InitiatorRecievingState())
                    return
                elif not await self.context.is_empty():
                    self.context.change_state(InitiatorDisconnectedState())
                    return

            if not self._is_room_active():
                self.context.change_state(ClosingRoomState())
                return
            
            print(f'{self.context._room_id}: {time() - self._measurements_started}')
            await sleep(1)
            
            # print('empty room')
