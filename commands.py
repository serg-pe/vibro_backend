from enum import Enum


class Commands(Enum):
    
    VIBRATION_ON = int.to_bytes(1, 1, 'big', signed=False)
    VIBRATION_OFF = int.to_bytes(2, 1, 'big', signed=False)
    OUT_OF_CLIENTS = int.to_bytes(3, 1, 'big', signed=False)
    INITIATOR_DISCONNECTED = int.to_bytes(4, 1, 'big', signed=False)
    INITIATOR_CONNECTED = int.to_bytes(5, 1, 'big', signed=False)
    CLIENT_CONNECTED = int.to_bytes(6, 1, 'big', signed=False)
    CLIENT_DISCONNECTED = int.to_bytes(7, 1, 'big', signed=False)
