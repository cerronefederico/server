import asyncio


import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware

from dataBase import AsyncDatabase
from plc import PLC

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
plc1=PLC()
plc2=PLC()
plc3=PLC()
db = AsyncDatabase()



@app.websocket("/ws/plc1/contatori")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await db.connect()
    try:
        data1s = await db.fetch_one("SELECT * FROM plc1.stati")
        data1c = await db.fetch_one("SELECT * FROM plc1.contatori")
        data1n = await db.fetch_all("""SELECT id,stato,to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora  FROM plc1.notifiche""")
        data2s = await db.fetch_one("SELECT * FROM plc2.stati")
        data2c = await db.fetch_one("SELECT * FROM plc2.contatori")
        data2n = await db.fetch_all("""SELECT id,stato,to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora  FROM plc2.notifiche""")
        data3s = await db.fetch_one("SELECT * FROM plc3.stati")
        data3c = await db.fetch_one("SELECT * FROM plc3.contatori")
        data3n = await db.fetch_all("""SELECT id,stato,to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora  FROM plc3.notifiche""")

        plc1.aggiornaStato(list(data1s.values())[1:])
        plc1.aggiornaContatori(list(data1c.values())[1:])
        plc2.aggiornaStato(list(data2s.values())[1:])
        plc2.aggiornaContatori(list(data2c.values())[1:])
        plc3.aggiornaStato(list(data3s.values())[1:])
        plc3.aggiornaContatori(list(data3c.values())[1:])

        await websocket.send_json({ "plc1": {
            "stati": data1s,
            "contatori": data1c,
            "notifiche": data1n},
            "plc2" : {
                "stati": data2s,
                "contatori": data2c,
                "notifiche": data2n},
            "plc3" : {
                "stati": data3s,
                "contatori": data3c,
                "notifiche": data3n}
        })
        while True:
            await db.connect()
            data1s = await db.fetch_one("SELECT * FROM plc1.stati")
            data1c = await db.fetch_one("SELECT * FROM plc1.contatori")
            data1n = await db.fetch_all("""SELECT id, stato, to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora FROM plc1.notifiche""")
            data2s = await db.fetch_one("SELECT * FROM plc2.stati")
            data2c = await db.fetch_one("SELECT * FROM plc2.contatori")
            data2n = await db.fetch_all("""SELECT id, stato, to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora FROM plc2.notifiche""")
            data3s = await db.fetch_one("SELECT * FROM plc3.stati")
            data3c = await db.fetch_one("SELECT * FROM plc3.contatori")
            data3n = await db.fetch_all("""SELECT id, stato, to_char(ora, 'YYYY-MM-DD"T"HH24:MI:SS.US') AS ora FROM plc3.notifiche""")
            if not plc1.controlloStato(list(data1s.values())[1:]):
                plc1.aggiornaStato(list(data1s.values())[1:])
                await websocket.send_json({"plc1": {
                    "stati": data1s,
                    "notifiche": data1n
                    }})
            if not plc1.controlloContatori(list(data1c.values())[1:]):
                plc1.aggiornaContatori(list(data1c.values())[1:])
                await websocket.send_json({"plc1": {
                    "contatori": data1c,
                    }})
            if not plc2.controlloStato(list(data2s.values())[1:]):
                plc2.aggiornaStato(list(data2s.values())[1:])
                await websocket.send_json({"plc2": {
                    "stati": data2s,
                    "notifiche": data2n
                    }})
            if not plc2.controlloContatori(list(data2c.values())[1:]):
                plc2.aggiornaContatori(list(data2c.values())[1:])
                await websocket.send_json({"plc2": {
                    "contatori": data2c,
                    }})
            if not plc3.controlloStato(list(data3s.values())[1:]):
                plc3.aggiornaStato(list(data3s.values())[1:])
                await websocket.send_json({"plc3": {
                    "stati": data3s,
                    "notifiche": data3n
                    }})
            if not plc3.controlloContatori(list(data3c.values())[1:]):
                plc3.aggiornaContatori(list(data3c.values())[1:])
                await websocket.send_json({"plc3": {
                    "contatori": data3c,
                    }})
            await asyncio.sleep(1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
