from typing import List, Tuple
from time import time

from fastapi import WebSocket


# class Room:
#     _LIFE_TIME = 420 # 7 minutes

#     def __init__(self, room_id: str, initiator: WebSocket=None, subscribers: List[WebSocket]=[]):
#         self._room_id: str = room_id
#         self._initiator: WebSocket = initiator
#         self._subscribers: List[WebSocket] = subscribers
#         self._created_at = time()

#     @property
#     def room_id(self) -> str:
#         return self._room_id

#     @property
#     def initiator(self) -> WebSocket:
#         return self._initiator

#     @initiator.setter
#     def initiator(self, initiator: WebSocket) -> None:
#         if self._initiator:
#             raise ValueError('Initiator already exists')
#         self._initiator = initiator

#     @property
#     def subscribers(self) -> Tuple[WebSocket]:
#         return tuple(self._subscribers)
    
#     def drop_client(self, client: WebSocket) -> None:
#         if self._initiator == client:
#             self._initiator = None
#         else:
#             for subscriber_index, _ in self._subscribers:
#                 if self._subscribers[subscriber_index] == client:
#                     self._subscribers.pop(subscriber_index)

#     def drop

#     def is_alive(self) -> bool:
#         return (self._initiator) or ((time() - self._created_at) < self._LIFE_TIME)

#     def add_subscriber(self, client_websocket: WebSocket) -> None:
#         pass

#     def remove_subscriber(self) -> None:
#         pass

#     def notify_subscribers() -> None:
#         pass


class Room:
    
    def __init__(self) -> None:
        self._initiator: WebSocket = None
        self._subscribers: List[WebSocket] = []

    @property
    def initiator(self) -> WebSocket:
        return self._initiator

    @initiator.setter
    def initiator(self, initiator) -> None:
        if self._initiator:
            raise ValueError('Initiator already set')
        else:
            self._initiator = initiator

    def drop_initiator(self) -> WebSocket:
        initiator = self.initiator
        self._initiator = None
        return initiator


    @property
    def subscribers(self) -> Tuple[WebSocket]:
        return tuple(self._subscribers)

    def add_subscriber(self, subscriber: WebSocket) -> None:
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber_websocket: WebSocket) -> None:
        for subscriber_index, subscriber in enumerate(self._subscribers):
            if subscriber_websocket == subscriber:
                self._subscribers.pop(subscriber_index)

    

