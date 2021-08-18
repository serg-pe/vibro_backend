from fastapi import WebSocket, Query, APIRouter

from connections_manager import ConnectionsManager


router = APIRouter()
connections_manager = ConnectionsManager()


@router.websocket('/connection/')
async def listener(websocket: WebSocket, is_initiator: bool=Query(False, alias='is-initiator')):
    await connections_manager.accept_connection(websocket, is_initiator)
