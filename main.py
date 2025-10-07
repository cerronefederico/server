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
        data2s = await db.fetch_one("SELECT * FROM plc2.stati")
        data2c = await db.fetch_one("SELECT * FROM plc2.contatori")
        data3s = await db.fetch_one("SELECT * FROM plc3.stati")
        data3c = await db.fetch_one("SELECT * FROM plc3.contatori")

        plc1.aggiornaStato(list(data1s.values())[1:])
        plc1.aggiornaContatori(list(data1c.values())[1:])
        plc2.aggiornaStato(list(data2s.values())[1:])
        plc2.aggiornaContatori(list(data2c.values())[1:])
        plc3.aggiornaStato(list(data3s.values())[1:])
        plc3.aggiornaContatori(list(data3c.values())[1:])

        await websocket.send_json({ "plc1": {
            "acceso": data1s.get("acceso", 0),
            "blocco": data1s.get("blocco", 0),
            "regime": data1s.get("regime", 0),
            "wTermico": data1s.get("wtermico", 0),
            "wAnomaliaNastro": data1s.get("wanomalianastro", 0),
            "wMancanzaProdotto": data1s.get("wmancanzaprodotto", 0),
            "wPieno": data1s.get("wpieno", 0),
            "wPortelloneAperto": data1s.get("wportelloneaperto", 0),
            "aAnomaliaGenerica": data1s.get("aanomaliagenerica", 0),
            "aMotoreNastro": data1s.get("amotorenastro", 0),
            "aMancanzaConsenso": data1s.get("amancanzaconsenso", 0),
            "aTemperaturaProdottoAlta": data1s.get("atemperaturaprodottoalta", 0),
            "aEmergenzaInserita": data1s.get("aemergenzainserita", 0),
            "aTemperaturaCpuElevata": data1s.get("atemperaturacpuelevata", 0),
            "aAggraffatriceSpenta": data1s.get("aaggraffatricespenta", 0),
            "aNastroSpento": data1s.get("anastrospento", 0),
            "contatorePezziTotale": data1c.get("contatorepezzitotale", False),
            "contatorePezziParziale": data1c.get("contatorepezziparziale", False),
            "contatorePezziParzialeBackup": data1c.get("contatorepezziparzialebackup", False),
            "velocitaProduzionePezziMinuto": data1c.get("velocitaproduzionepezziminuto", False),
            "temperaturaCpu": data1c.get("temperaturacpu", False)},
            "plc2" : {
                "acceso": data2s.get("acceso", 0),
                "blocco": data2s.get("blocco", 0),
                "regime": data2s.get("regime", 0),
                "wTermico": data2s.get("wtermico", 0),
                "wAnomaliaNastro": data2s.get("wanomalianastro", 0),
                "wMancanzaProdotto": data2s.get("wmancanzaprodotto", 0),
                "wPieno": data2s.get("wpieno", 0),
                "wPortelloneAperto": data2s.get("wportelloneaperto", 0),
                "aAnomaliaGenerica": data2s.get("aanomaliagenerica", 0),
                "aMotoreNastro": data2s.get("amotorenastro", 0),
                "aMancanzaConsenso": data2s.get("amancanzaconsenso", 0),
                "aTemperaturaProdottoAlta": data2s.get("atemperaturaprodottoalta", 0),
                "aEmergenzaInserita": data2s.get("aemergenzainserita", 0),
                "aTemperaturaCpuElevata": data2s.get("atemperaturacpuelevata", 0),
                "aAggraffatriceSpenta": data2s.get("aaggraffatricespenta", 0),
                "aNastroSpento": data2s.get("anastrospento", 0),
                "contatorePezziTotale": data2c.get("contatorepezzitotale", False),
                "contatorePezziParziale": data2c.get("contatorepezziparziale", False),
                "contatorePezziParzialeBackup": data2c.get("contatorepezziparzialebackup", False),
                "velocitaProduzionePezziMinuto": data2c.get("velocitaproduzionepezziminuto", False),
                "temperaturaCpu": data2c.get("temperaturacpu", False)},
            "plc3" : {
                "acceso": data3s.get("acceso", 0),
                "blocco": data3s.get("blocco", 0),
                "regime": data3s.get("regime", 0),
                "wTermico": data3s.get("wtermico", 0),
                "wAnomaliaNastro": data3s.get("wanomalianastro", 0),
                "wMancanzaProdotto": data3s.get("wmancanzaprodotto", 0),
                "wPieno": data3s.get("wpieno", 0),
                "wPortelloneAperto": data3s.get("wportelloneaperto", 0),
                "aAnomaliaGenerica": data3s.get("aanomaliagenerica", 0),
                "aMotoreNastro": data3s.get("amotorenastro", 0),
                "aMancanzaConsenso": data3s.get("amancanzaconsenso", 0),
                "aTemperaturaProdottoAlta": data3s.get("atemperaturaprodottoalta", 0),
                "aEmergenzaInserita": data3s.get("aemergenzainserita", 0),
                "aTemperaturaCpuElevata": data3s.get("atemperaturacpuelevata", 0),
                "aAggraffatriceSpenta": data3s.get("aaggraffatricespenta", 0),
                "aNastroSpento": data3s.get("anastrospento", 0),
                "contatorePezziTotale": data3c.get("contatorepezzitotale", False),
                "contatorePezziParziale": data3c.get("contatorepezziparziale", False),
                "contatorePezziParzialeBackup": data3c.get("contatorepezziparzialebackup", False),
                "velocitaProduzionePezziMinuto": data3c.get("velocitaproduzionepezziminuto", False),
                "temperaturaCpu": data3c.get("temperaturacpu", False)}

        })
        while True:
            await db.connect()
            data1s = await db.fetch_one("SELECT * FROM plc1.stati")
            data1c = await db.fetch_one("SELECT * FROM plc1.contatori")
            data2s = await db.fetch_one("SELECT * FROM plc2.stati")
            data2c = await db.fetch_one("SELECT * FROM plc2.contatori")
            data3s = await db.fetch_one("SELECT * FROM plc3.stati")
            data3c = await db.fetch_one("SELECT * FROM plc3.contatori")
            if not plc1.controlloStato(list(data1s.values())[1:]):
                plc1.aggiornaStato(list(data1s.values())[1:])
                await websocket.send_json({"plc1": {
                    "acceso": data1s.get("acceso", 0),
                    "blocco": data1s.get("blocco", 0),
                    "regime": data1s.get("regime", 0),
                    "wTermico": data1s.get("wtermico", 0),
                    "wAnomaliaNastro": data1s.get("wanomalianastro", 0),
                    "wMancanzaProdotto": data1s.get("wmancanzaprodotto", 0),
                    "wPieno": data1s.get("wpieno", 0),
                    "wPortelloneAperto": data1s.get("wportelloneaperto", 0),
                    "aAnomaliaGenerica": data1s.get("aanomaliagenerica", 0),
                    "aMotoreNastro": data1s.get("amotorenastro", 0),
                    "aMancanzaConsenso": data1s.get("amancanzaconsenso", 0),
                    "aTemperaturaProdottoAlta": data1s.get("atemperaturaprodottoalta", 0),
                    "aEmergenzaInserita": data1s.get("aemergenzainserita", 0),
                    "aTemperaturaCpuElevata": data1s.get("atemperaturacpuelevata", 0),
                    "aAggraffatriceSpenta": data1s.get("aaggraffatricespenta", 0),
                    "aNastroSpento": data1s.get("anastrospento", 0)}})
            if not plc1.controlloContatori(list(data1c.values())[1:]):
                plc1.aggiornaContatori(list(data1c.values())[1:])
                await websocket.send_json({"plc1": {
                    "contatorePezziTotale": data1c.get("contatorepezzitotale", False),
                    "contatorePezziParziale": data1c.get("contatorepezziparziale", False),
                    "contatorePezziParzialeBackup": data1c.get("contatorepezziparzialebackup", False),
                    "velocitaProduzionePezziMinuto": data1c.get("velocitaproduzionepezziminuto", False),
                    "temperaturaCpu": data1c.get("temperaturacpu", False)
                    }})
            if not plc2.controlloStato(list(data2s.values())[1:]):
                plc2.aggiornaStato(list(data2s.values())[1:])
                await websocket.send_json({"plc2": {
                    "acceso": data2s.get("acceso", 0),
                    "blocco": data2s.get("blocco", 0),
                    "regime": data2s.get("regime", 0),
                    "wTermico": data2s.get("wtermico", 0),
                    "wAnomaliaNastro": data2s.get("wanomalianastro", 0),
                    "wMancanzaProdotto": data2s.get("wmancanzaprodotto", 0),
                    "wPieno": data2s.get("wpieno", 0),
                    "wPortelloneAperto": data2s.get("wportelloneaperto", 0),
                    "aAnomaliaGenerica": data2s.get("aanomaliagenerica", 0),
                    "aMotoreNastro": data2s.get("amotorenastro", 0),
                    "aMancanzaConsenso": data2s.get("amancanzaconsenso", 0),
                    "aTemperaturaProdottoAlta": data2s.get("atemperaturaprodottoalta", 0),
                    "aEmergenzaInserita": data2s.get("aemergenzainserita", 0),
                    "aTemperaturaCpuElevata": data2s.get("atemperaturacpuelevata", 0),
                    "aAggraffatriceSpenta": data2s.get("aaggraffatricespenta", 0),
                    "aNastroSpento": data2s.get("anastrospento", 0)}})
            if not plc2.controlloContatori(list(data2c.values())[1:]):
                plc2.aggiornaContatori(list(data2c.values())[1:])
                await websocket.send_json({"plc2": {
                    "contatorePezziTotale": data2c.get("contatorepezzitotale", False),
                    "contatorePezziParziale": data2c.get("contatorepezziparziale", False),
                    "contatorePezziParzialeBackup": data2c.get("contatorepezziparzialebackup", False),
                    "velocitaProduzionePezziMinuto": data2c.get("velocitaproduzionepezziminuto", False),
                    "temperaturaCpu": data2c.get("temperaturacpu", False)
                    }})
            if not plc3.controlloStato(list(data3s.values())[1:]):
                plc3.aggiornaStato(list(data3s.values())[1:])
                await websocket.send_json({"plc3": {
                    "acceso": data3s.get("acceso", 0),
                    "blocco": data3s.get("blocco", 0),
                    "regime": data3s.get("regime", 0),
                    "wTermico": data3s.get("wtermico", 0),
                    "wAnomaliaNastro": data3s.get("wanomalianastro", 0),
                    "wMancanzaProdotto": data3s.get("wmancanzaprodotto", 0),
                    "wPieno": data3s.get("wpieno", 0),
                    "wPortelloneAperto": data3s.get("wportelloneaperto", 0),
                    "aAnomaliaGenerica": data3s.get("aanomaliagenerica", 0),
                    "aMotoreNastro": data3s.get("amotorenastro", 0),
                    "aMancanzaConsenso": data3s.get("amancanzaconsenso", 0),
                    "aTemperaturaProdottoAlta": data3s.get("atemperaturaprodottoalta", 0),
                    "aEmergenzaInserita": data3s.get("aemergenzainserita", 0),
                    "aTemperaturaCpuElevata": data3s.get("atemperaturacpuelevata", 0),
                    "aAggraffatriceSpenta": data3s.get("aaggraffatricespenta", 0),
                    "aNastroSpento": data3s.get("anastrospento", 0)}})
            if not plc3.controlloContatori(list(data3c.values())[1:]):
                plc3.aggiornaContatori(list(data3c.values())[1:])
                await websocket.send_json({"plc3": {
                    "contatorePezziTotale": data3c.get("contatorepezzitotale", False),
                    "contatorePezziParziale": data3c.get("contatorepezziparziale", False),
                    "contatorePezziParzialeBackup": data3c.get("contatorepezziparzialebackup", False),
                    "velocitaProduzionePezziMinuto": data3c.get("velocitaproduzionepezziminuto", False),
                    "temperaturaCpu": data3c.get("temperaturacpu", False)
                    }})
            await asyncio.sleep(1)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
