import asyncpg, os, json
from datetime import datetime

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
    return _pool

async def init_db():
    pool = await get_pool()
    async with pool.acquire() as con:
        await con.execute("""
            CREATE TABLE IF NOT EXISTS status (
                id SERIAL PRIMARY KEY,
                overall_status TEXT,
                affected_cities JSONB,
                primary_reason TEXT,
                reasoning TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS cursor (
                id INT PRIMARY KEY DEFAULT 1,
                last_msg_id BIGINT DEFAULT 0
            );
            INSERT INTO cursor (id, last_msg_id) VALUES (1, 0)
            ON CONFLICT (id) DO NOTHING;
        """)

async def save_status(final) -> None:
    pool = await get_pool()
    async with pool.acquire() as con:
        await con.execute(
            """INSERT INTO status (overall_status, affected_cities, primary_reason, reasoning)
               VALUES ($1,$2,$3,$4)""",
            final.overall_status,
            json.dumps(final.affected_cities),
            final.primary_reason,
            final.reasoning,
        )

async def load_last_id() -> int:
    pool = await get_pool()
    async with pool.acquire() as con:
        row = await con.fetchrow("SELECT last_msg_id FROM cursor WHERE id=1")
        return row["last_msg_id"]

async def save_last_id(mid: int) -> None:
    pool = await get_pool()
    async with pool.acquire() as con:
        await con.execute("UPDATE cursor SET last_msg_id=$1 WHERE id=1", mid)

async def latest_status() -> dict | None:
    pool = await get_pool()
    async with pool.acquire() as con:
        row = await con.fetchrow("SELECT * FROM status ORDER BY created_at DESC LIMIT 1")
        return dict(row) if row else None