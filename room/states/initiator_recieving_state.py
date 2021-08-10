from fastapi import WebSocketDisconnect, WebSocket

from .room_state import RoomState
from commands import Commands


class InitiatorRecievingState(RoomState):

    async def run(self):
        from . import InitiatorDisconnectedState
        from . import ClosingRoomState

        try:
            while True:
                command_bytes = await self.context.initiator.receive_bytes()
                await self.context.notify_subscribers(command_bytes)
                
                if command_bytes == Commands.ROOM_CLOSED.value:
                    self.context.change_state(ClosingRoomState())
                    return

        except Exception:
            self.context.initiator.close()
            self.context.drop_initiator()
            self.context.change_state(InitiatorDisconnectedState())
