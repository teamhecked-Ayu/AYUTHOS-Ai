import asyncio
import os
from dotenv import load_dotenv

from ingestors import TwitterIngestor, RedditIngestor, NewsIngestor
from nervous_system import RedisClient

load_dotenv()

async def simulate_ingestion():
    redis_client = RedisClient()

    ingestors = [
        TwitterIngestor(),
        RedditIngestor(),
        NewsIngestor(),
    ]

    print("Starting real-time data ingestion simulation...")

    for ingestor in ingestors:
        print(f"Ingesting data from {ingestor.name}...")
        data = await ingestor.ingest()
        for item in data:
            channel = f"data_stream:{ingestor.name.lower().replace(' ', '_')}"
            message = str(item) # Convert dict to string for Redis publish
            await redis_client.publish(channel, message)
            print(f"Published to {channel}: {message[:50]}...")

    print("Data ingestion simulation complete.")

if __name__ == "__main__":
    asyncio.run(simulate_ingestion())
