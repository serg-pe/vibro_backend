from enum import Enum


class Commands(Enum):
    """Signals list to be sent & received in connection process."""

    VIBRATION_ON = int.to_bytes(1, 1, 'big', signed=False)
    VIBRATION_OFF = int.to_bytes(2, 1, 'big', signed=False)

    INITIATOR_DISCONNECTED = int.to_bytes(3, 1, 'big', signed=False)
    INITIATOR_CONNECTED = int.to_bytes(4, 1, 'big', signed=False)

    UPDATE_CLIENTS_STATISTIC = int.to_bytes(5, 1, 'big', signed=False)
    
    PING = int.to_bytes(6, 1, 'big', signed=False)
    PONG = int.to_bytes(7, 1, 'big', signed=False)