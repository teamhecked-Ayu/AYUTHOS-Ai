
import asyncio
import asyncpg
import os
import json
from dotenv import load_dotenv
from models import BaseAgent

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

AGENT_CATEGORIES = {
    "Macro Analysts": {"count": 15, "description": "Global economic trends, interest rates, GDP"},
    "Quant Traders": {"count": 15, "description": "Technical indicators, price action, volatility"},
    "Skeptics": {"count": 10, "description": "Contrarian views, stress-testing consensus"},
    "Social Sentiment": {"count": 15, "description": "Twitter/Reddit sentiment, meme dynamics"},
    "Geopolitical": {"count": 10, "description": "International relations, policy impacts"},
    "On-Chain Analysts": {"count": 10, "description": "Blockchain data, whale movements, DeFi flows"},
    "Retail Investors": {"count": 15, "description": "Emotional, FOMO-driven, trend-following"},
    "Institutional": {"count": 10, "description": "Large-scale positioning, OTC flows"},
}

async def generate_and_store_personas():
    if not DATABASE_URL:
        print("DATABASE_URL not found in .env. Skipping persona generation.")
        return

    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to database for persona generation.")

        agent_id_counter = 0
        for category, details in AGENT_CATEGORIES.items():
            for i in range(details["count"]):
                agent_id_counter += 1
                persona_name = f"{category.replace(" ", "")}_{i+1}"
                background = details["description"]
                personality_traits = {"risk_tolerance": 0.5, "optimism": 0.5} # Placeholder
                memory = {"long_term": []} # Placeholder

                agent = BaseAgent(
                    agent_id=agent_id_counter,
                    persona_name=persona_name,
                    background=background,
                    personality_traits=personality_traits,
                    memory=memory
                )

                await conn.execute(
                    "INSERT INTO agents (id, persona_name, background, personality_traits, memory) VALUES ($1, $2, $3, $4, $5)",
                    agent.agent_id, agent.persona_name, agent.background, json.dumps(agent.personality_traits), json.dumps(agent.memory)
                )
                print(f"Generated and stored agent: {agent.persona_name}")
        print(f"Successfully generated and stored {agent_id_counter} agent personas.")

    except Exception as e:
        print(f"Error generating or storing personas: {e}")
    finally:
        if conn:
            await conn.close()

if __name__ == "__main__":
    asyncio.run(generate_and_store_personas())
