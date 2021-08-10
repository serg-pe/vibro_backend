from enum import Enum


class Commands(Enum):
    VIBRATION_ON = int.to_bytes(1, 1, 'big')
    VIBRATION_OFF = int.to_bytes(2, 1, 'big')
    PING = int.to_bytes(3, 1, 'big')
    ROOM_CLOSED = int.to_bytes(4, 1, 'big')
    # OUT_OF_CLIENTS = int.to_bytes(3, 1, 'big')
    # INITIATOR_DISCONNECTED = int.to_bytes(4, 1, 'big')
    # ROOM_CLOSED = int.to_bytes(5, 1, 'big')
