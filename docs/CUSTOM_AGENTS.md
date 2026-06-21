# 🧬 Adding Custom Agents and Data Sources to AYUTHOS-AI

AYUTHOS-AI is designed for extensibility, allowing you to easily integrate new agent types and data ingestion sources to tailor the simulation to your specific needs.

---

## 🧠 Adding New Agent Types

To add a new agent type, you need to create a new Python class that inherits from `BaseAgent` and implement its `analyze` method. This method defines the core logic for how your agent processes information and generates insights.

### 1. Create a New Agent File

Create a new Python file in the `models/` directory (e.g., `models/defi_analyst.py`).

```python
# models/defi_analyst.py
from .base_agent import BaseAgent
from typing import Dict, Any

class DeFiAnalyst(BaseAgent):
    def __init__(self, agent_id: int, persona_name: str, background: str, personality_traits: Dict[str, Any], memory: Dict[str, Any]):
        super().__init__(agent_id, persona_name, background, personality_traits, memory)
        self.role = "DeFi Specialist"
        # You can add more specific initialization for your agent here

    async def analyze(self, data: Any) -> Dict[str, Any]:
        """Custom logic for DeFi protocols analysis."""
        # Implement your agent's specific analysis logic here.
        # This could involve:
        # - Processing data from Redis streams
        # - Querying the Knowledge Graph in PostgreSQL
        # - Making LLM calls via the Python CLI
        # - Performing complex calculations with pandas/numpy
        
        print(f"DeFi Analyst {self.persona_name} analyzing data: {data}")
        
        # Example: Dummy analysis result
        signal = "BULLISH" if "positive news" in str(data).lower() else "NEUTRAL"
        confidence = 0.78 if signal == "BULLISH" else 0.5

        return {"signal": signal, "confidence": confidence, "agent_id": self.agent_id}

```

### 2. Update `models/__init__.py`

Add your new agent class to `models/__init__.py` so it can be imported easily.

```python
# models/__init__.py
from .base_agent import BaseAgent
from .knowledge_graph import KnowledgeGraph
from .report_agent import ReportAgent
from .defi_analyst import DeFiAnalyst # Add your new agent here
```

### 3. Integrate into `agent_registry.py`

Modify `personas/agent_registry.py` to include your new agent type in the `AGENT_CATEGORIES` and ensure it's instantiated correctly.

```python
# personas/agent_registry.py (excerpt)
# ...
AGENT_CATEGORIES = {
    # ... existing categories ...
    "DeFi Analysts": {"count": 5, "description": "Decentralized Finance protocols, on-chain data"},
}

async def generate_and_store_personas():
    # ...
    for category, details in AGENT_CATEGORIES.items():
        for i in range(details["count"]):
            agent_id_counter += 1
            persona_name = f"{category.replace(" ", "")}_{i+1}"
            background = details["description"]
            personality_traits = {"risk_tolerance": 0.5, "optimism": 0.5} # Placeholder
            memory = {"long_term": []} # Placeholder

            # Instantiate your custom agent based on category
            if category == "DeFi Analysts":
                agent = DeFiAnalyst(
                    agent_id=agent_id_counter,
                    persona_name=persona_name,
                    background=background,
                    personality_traits=personality_traits,
                    memory=memory
                )
            else:
                agent = BaseAgent(
                    agent_id=agent_id_counter,
                    persona_name=persona_name,
                    background=background,
                    personality_traits=personality_traits,
                    memory=memory
                )
            # ... rest of the storage logic ...
```

---

## 📡 Adding New Data Sources

To add a new data source, create a new Python class that inherits from `BaseIngestor` and implement its `ingest` method. This method should handle fetching data from your chosen source and returning it in a structured format.

### 1. Create a New Ingestor File

Create a new Python file in the `ingestors/` directory (e.g., `ingestors/glassnode_ingestor.py`).

```python
# ingestors/glassnode_ingestor.py
import asyncio
from typing import List, Dict, Any
from .base_ingestor import BaseIngestor

class GlassnodeIngestor(BaseIngestor):
    def __init__(self):
        super().__init__("Glassnode")

    async def ingest(self) -> List[Dict[str, Any]]:
        """Fetches on-chain data from the Glassnode API."""
        print(f"[{self.name}] Fetching data from Glassnode...")
        # Implement actual API call to Glassnode here
        # Ensure you handle API keys securely via .env
        await asyncio.sleep(2) # Simulate API call latency
        return [
            {"source": self.name, "timestamp": "2026-06-21T13:00:00Z", "metric": "whale_activity", "value": 0.23},
            {"source": self.name, "timestamp": "2026-06-21T13:05:00Z", "metric": "exchange_flows", "value": -450},
        ]
```

### 2. Update `ingestors/__init__.py`

Add your new ingestor class to `ingestors/__init__.py`.

```python
# ingestors/__init__.py
from .base_ingestor import BaseIngestor
from .twitter_ingestor import TwitterIngestor
from .reddit_ingestor import RedditIngestor
from .news_ingestor import NewsIngestor
from .cryptopanic_ingestor import CryptoPanicIngestor
from .glassnode_ingestor import GlassnodeIngestor # Add your new ingestor here
```

### 3. Integrate into `simulate_ingestion.py` (or Orchestrator)

If you want to include your new ingestor in the simulation or the main orchestrator, add it to the list of ingestors.

```python
# scripts/simulate_ingestion.py (excerpt)
# ...
from ingestors import TwitterIngestor, RedditIngestor, NewsIngestor, CryptoPanicIngestor, GlassnodeIngestor
# ...

async def simulate_ingestion():
    # ...
    ingestors = [
        TwitterIngestor(),
        RedditIngestor(),
        NewsIngestor(),
        CryptoPanicIngestor(),
        GlassnodeIngestor(), # Add your new ingestor here
    ]
    # ...
```

By following these steps, you can extend AYUTHOS-AI with custom agents and data sources, making it even more powerful for your specific forecasting needs. 🚀
