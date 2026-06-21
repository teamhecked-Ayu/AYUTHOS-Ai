import json
from typing import Dict, Any

class BaseAgent:
    def __init__(self, agent_id: int, persona_name: str, background: str, personality_traits: Dict[str, Any], memory: Dict[str, Any]):
        self.agent_id = agent_id
        self.persona_name = persona_name
        self.background = background
        self.personality_traits = personality_traits
        self.memory = memory

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Abstract method for agent-specific analysis."""
        raise NotImplementedError("Subclasses must implement the analyze method")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "persona_name": self.persona_name,
            "background": self.background,
            "personality_traits": self.personality_traits,
            "memory": self.memory,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            agent_id=data["agent_id"],
            persona_name=data["persona_name"],
            background=data["background"],
            personality_traits=data["personality_traits"],
            memory=data["memory"],
        )
