import asyncpg
from typing import List, Dict, Any


class AsyncDatabase:
    """Gestisce il pool di connessioni asincrone per PostgreSQL."""

    def __init__(self):
        self.pool = None

    async def connect(self):
        """Crea il pool di connessioni all'avvio dell'applicazione."""
        if self.pool is None:
            try:
                # asyncpg utilizza l'URL costruito
                self.pool = await asyncpg.create_pool( database="postgres", user="postgres", password="admin", host="192.168.40.13", port=5432, min_size=5,max_size=10,timeout=60)
                print("Connessione al database PostgreSQL stabilita con successo.")
            except Exception as e:
                print(f"ERRORE CRITICO DI CONNESSIONE DB: {e}")
                # Potresti voler rilanciare l'eccezione o gestire l'uscita qui

    async def close(self):
        """Chiude il pool di connessioni alla chiusura dell'applicazione."""
        if self.pool:
            await self.pool.close()
            print("Pool di connessioni al database chiuso.")

    async def fetch_one(self, query: str, *args) -> Dict[str, Any] | None:
        """Esegue una query e restituisce una singola riga come dizionario."""
        if self.pool is None: return None
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(query, *args)
            return dict(record) if record else None

    async def fetch_all(self, query: str, *args) -> List[Dict[str, Any]]:
        """Esegue una query e restituisce tutte le righe come lista di dizionari."""
        async with self.pool.acquire() as conn:
            # fetch restituisce una lista di record, convertiti in dizionari
            records = await conn.fetch(query, *args)
            return [dict(record) for record in records]

    async def execute(self, query: str, *args) -> str:
        """Esegue un comando DML (INSERT, UPDATE, DELETE) e restituisce lo stato."""
        async with self.pool.acquire() as conn:
            # execute restituisce il tag di stato (es. 'INSERT 0 1')
            status = await conn.execute(query, *args)
            return status

