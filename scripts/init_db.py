import os
import asyncio
import asyncpg
import json
from dotenv import load_dotenv
from personas.agent_registry import generate_and_store_personas

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env. Skipping database initialization.")
        return

    print(f"Connecting to database: {DATABASE_URL}")
    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        
        # Create agents table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id SERIAL PRIMARY KEY,
                persona_name TEXT NOT NULL,
                background TEXT,
                personality_traits JSONB,
                memory JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create sessions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                session_id TEXT UNIQUE NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT,
                config JSONB
            );
        """)

        # Create verdicts table (renamed from simulation_runs and adjusted schema)
        await conn.execute("""
            DROP TABLE IF EXISTS simulation_runs;
            CREATE TABLE IF NOT EXISTS verdicts (
                id SERIAL PRIMARY KEY,
                run_id TEXT UNIQUE NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                requirement TEXT NOT NULL,
                agents_active INTEGER,
                simulation_rounds INTEGER,
                scenarios JSONB,
                consensus_signal TEXT,
                consensus_confidence NUMERIC,
                recommended_action TEXT,
                risk_assessment JSONB,
                agent_agreement JSONB,
                top_agents JSONB,
                raw_output JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create knowledge_graph table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_graph (
                id SERIAL PRIMARY KEY,
                entity_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                properties JSONB,
                relationships JSONB,
                source_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Create memory table (for long-term agent memory)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id SERIAL PRIMARY KEY,
                agent_id INTEGER REFERENCES agents(id),
                memory_type TEXT NOT NULL, -- e.g., 'episodic', 'semantic'
                content TEXT NOT NULL,
                embedding VECTOR(1536), -- Placeholder for vector embeddings
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        print("Database initialized successfully with agents, sessions, verdicts, knowledge_graph, and memory tables.")
        
        # Generate and store initial personas if the agents table is empty
        agent_count = await conn.fetchval("SELECT COUNT(*) FROM agents;")
        if agent_count == 0:
            await generate_and_store_personas()
        else:
            print("Agents already exist in the database. Skipping persona generation.")

    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())
