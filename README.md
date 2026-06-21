# AYUTHOS-AI — The 100-Agent Civilization Forecasting Engine

A CLI-native, real-time, 100-agent swarm intelligence engine that transforms live global data into probability-ranked future scenarios, confidence scores, risk assessments, and strategic intelligence reports.

## 🏛️ Architecture
- **CLI Layer (Python)**: The Brain. Handles strategy, coordination, and user interface.
- **Orchestrator (Rust)**: The Muscles. Manages tick-based parallel agent execution.
- **PostgreSQL**: The Memory. Stores personas, knowledge graphs, and history.
- **Redis**: The Nervous System. Real-time event streams and agent communication.

## 🚀 Quick Start
```bash
# Setup Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build Rust Orchestrator
cargo build --release --manifest-path orchestrator/Cargo.toml

# Initialize
cp .env.example .env
python scripts/init_db.py

# Run
ayuthos run --files sample.md --requirement "Predict market reaction"
```

## 📜 License
MIT
