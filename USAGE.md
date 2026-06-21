# 🌍 AYUTHOS-AI Multi-OS Setup & Usage Guide

This guide provides step-by-step instructions to get **AYUTHOS-AI** running on any platform, including Linux (Ubuntu/Parrot), Android (Termux), macOS, and Windows.

---

## 🛠️ Prerequisites (All Systems)
Before starting, ensure you have the following installed:
- **Python 3.11+**
- **Rust (Cargo)**
- **PostgreSQL 15+**
- **Redis 7+**

---

## 🐧 Linux (Ubuntu, Debian, Parrot OS, Kali)

### 1. Install System Dependencies
```bash
sudo apt update && sudo apt install -y git build-essential libclang-dev postgresql redis-server python3-pip python3-venv
```

### 2. Clone and Setup
```bash
git clone https://github.com/teamhecked-Ayu/AYUTHOS-Ai.git
cd AYUTHOS-Ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3. Build Rust Core
```bash
cargo build --release --manifest-path orchestrator/Cargo.toml
```

---

## 📱 Android (Termux)

### 1. Install Required Packages
```bash
pkg update && pkg upgrade
pkg install git python rust make clang postgresql redis-server
```

### 2. Setup Database & Redis
Start the services in separate Termux sessions or in the background:
```bash
redis-server &
initdb -D $PREFIX/var/lib/postgresql
pg_ctl -D $PREFIX/var/lib/postgresql start
createdb ayuthos
```

### 3. Clone and Setup
```bash
git clone https://github.com/teamhecked-Ayu/AYUTHOS-Ai.git
cd AYUTHOS-Ai
pip install -r requirements.txt
pip install -e .
cargo build --release --manifest-path orchestrator/Cargo.toml
```

---

## 🍎 macOS (Intel & Apple Silicon)

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Dependencies
```bash
brew install python rust postgresql@15 redis
brew services start postgresql@15
brew services start redis
```

### 3. Clone and Setup
```bash
git clone https://github.com/teamhecked-Ayu/AYUTHOS-Ai.git
cd AYUTHOS-Ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
cargo build --release --manifest-path orchestrator/Cargo.toml
```

---

## 🪟 Windows (WSL2 Recommended)

### 1. Install WSL2 (Ubuntu)
Open PowerShell as Administrator and run:
```powershell
wsl --install
```

### 2. Follow Linux Instructions
Restart your computer, open the **Ubuntu** terminal, and follow the **Linux** steps above.

*Note: Running natively on Windows CMD/PowerShell is possible but requires manual installation of PostgreSQL and Redis for Windows, which is less stable for this engine.*

---

## ⚙️ Final Configuration (All Platforms)

1. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Open .env and add your LLM API keys (OpenAI, Claude, etc.)
   ```

2. **Initialize Database**:
   ```bash
   python scripts/init_db.py
   ```

3. **Run Your First Forecast**:
   ```bash
   ayuthos run --requirement "Predict the impact of AI on global labor markets by 2030"
   ```

---

## 🚀 Troubleshooting
- **Rust Build Errors**: Ensure `libclang` is installed. On Linux: `sudo apt install libclang-dev`.
- **Database Connection**: Verify PostgreSQL is running and the `DATABASE_URL` in `.env` is correct.
- **Redis Error**: Ensure `redis-server` is active.
