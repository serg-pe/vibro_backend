from asyncio import sleep

from .room_state import RoomState


class InitiatorDisconnectedState(RoomState):

    async def run(self):
        from . import EmptyRoomState
        from . import InitiatorRecievingState

        print('Initiator Disconnected State')
        while True:
            if self.context.initiator:
                self.context.change_state(InitiatorRecievingState())
                return
            elif await self.context.is_empty():
                self.context.change_state(EmptyRoomState())
                return
            
            await sleep(1)
