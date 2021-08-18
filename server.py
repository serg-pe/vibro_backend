from fastapi import WebSocket, Query, APIRouter

from connections_manager import ConnectionsManager


router = APIRouter()
connections_manager = ConnectionsManager()


@router.websocket('/connection/')
async def listener(websocket: WebSocket, is_initiator: bool=Query(False, alias='is-initiator')):
    """Websockets server endpoint.

    Args:
        websocket (WebSocket): incoming connection websocket
        is_initiator (bool, optional): initiator flag. Defaults to False.
    """
    await connections_manager.accept_connection(websocket, is_initiator)
