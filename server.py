from typing import Dict, List

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from nanoid import generate as generate_nanoid

from room import Room
from commands import Commands


NANOID_ALPHABET = '0123456789'
NANOID_LENGTH = 10


app = FastAPI()


rooms: Dict[int, Room] = {}

listened_clients = []


@app.get('/api/create-room')
async def create_room():
    room_id = int(generate_nanoid(NANOID_ALPHABET, NANOID_LENGTH))
    while rooms.get(room_id):
        room_id = generate_nanoid(NANOID_ALPHABET, NANOID_LENGTH)
    
    rooms[room_id] = Room()

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
    room = rooms.get(room_id)

    if (not room) or (is_initiator and room.initiator):
        await websocket.close()
        return
    
    await websocket.accept()
    
    if is_initiator:
        await listen_initiator(websocket, room)
    else:
        await notify_subscriber(websocket, room)
