

from commands import Commands
from .room_state import RoomState
from .exceptions import RoomClosedException


class ClosingRoomState(RoomState):

    async def run(self):
        from room.rooms_manager import RoomsManager

        print('Closing Room State')

        if self.context.initiator:
            await self.context.initiator.close()
        
        for subscriber_ws in self.context.subscribers:
            await self.context.notify_subscribers(Commands.ROOM_CLOSED.value)
            await subscriber_ws.close()

        RoomsManager().close_room(self.context)

        raise RoomClosedException()
