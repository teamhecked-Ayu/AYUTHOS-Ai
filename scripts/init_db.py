
import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env. Skipping database initialization.")
        return

    print(f"Connecting to database: {DATABASE_URL}")
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Create tables
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id SERIAL PRIMARY KEY,
                persona_name TEXT NOT NULL,
                background TEXT,
                personality_traits JSONB,
                memory JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS simulation_runs (
                id SERIAL PRIMARY KEY,
                requirement TEXT NOT NULL,
                status TEXT NOT NULL,
                verdict JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        print("Database initialized successfully.")
        await conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())
