from abc import ABC, abstractmethod


class RoomState(ABC):

    _context: 'RoomContext' = None

    @property
    def context(self) -> 'RoomContext':
        return self._context

    @context.setter
    def context(self, context: 'RoomContext') -> None:
        self._context = context

    @abstractmethod
    async def run(self):
        pass