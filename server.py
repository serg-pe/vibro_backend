from typing import Dict, List

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from nanoid import generate as generate_nanoid

from room.room import Room
from room.rooms_manager import RoomsManager
from commands import Commands


app = FastAPI()
rooms_manager = RoomsManager()


@app.get('/api/create-room')
async def create_room():
    room_id = rooms_manager.init_room()

    return JSONResponse({
        'roomId': f'{room_id}',
    })


async def listen_initiator(websocket: WebSocket, room: Room):    
    room.initiator = websocket

    try:
        while True:
            command_bytes = await websocket.receive_bytes()
            print(command_bytes, int.from_bytes(command_bytes, 'big'))
            for subscriber in room.subscribers:
                await subscriber.send_bytes(command_bytes)
            
    except Exception:
        await websocket.close()
        room.drop_initiator()


async def notify_subscriber(websocket: WebSocket, room: Room):
    room.add_subscriber(websocket)
    
    try:
        while True:
            pass
    
    except Exception:
        await websocket.close()
        room.unsubscribe(websocket)


@app.websocket('/room/{room_id}/')
async def listener(websocket: WebSocket, room_id: int, is_initiator: bool=Query(False, alias='is-initiator')):
    await rooms_manager.accept_connection(websocket, room_id, is_initiator)
    # room = rooms.get(room_id)

    # if (not room) or (is_initiator and room.initiator):
    #     await websocket.close()
    #     return
    
    # await websocket.accept()
    
    # if is_initiator:
    #     await listen_initiator(websocket, room)
    # else:
    #     await notify_subscriber(websocket, room)
