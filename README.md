# MysterySeek

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Streamlit-Powered-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/LangChain-Powered-orange.svg" alt="LangChain">
</p>

🔍 **MysterySeek** is a unified AI-powered mystery game platform that brings together multiple reasoning and deduction games in a single cohesive interface. Currently featuring two exciting games powered by Large Language Model (LLM) agents.

## ✨ Features

- 🎮 **Unified Interface**: Single entry point for all mystery games with consistent UI/UX
- 🐺 **AutoWerewolf**: 12-player AI Werewolf game with watch and play modes
- 🎭 **Echoes of Deceit (Turtle Soup)**: Lateral thinking puzzle game with AI agents
- 🌍 **Multi-language Support**: English and Chinese
- 🤖 **Flexible Model Backend**: Supports Ollama (local) and OpenAI-compatible APIs
- 📊 **Game Analytics**: Session tracking and performance statistics

## 🎮 Included Games

### 🐺 AutoWerewolf
An LLM-driven Werewolf (Mafia) game where AI agents play against each other or alongside human players.
- 12-player games with complete Werewolf rules
- Multiple role sets (Seer, Witch, Hunter, Guard/Village Idiot)
- Watch mode and play mode
- [AutoWerewolf Repository](https://github.com/Linorman/AutoWerewolf)

### 🎭 Echoes of Deceit (Turtle Soup)
A lateral thinking puzzle game (also known as "Situation Puzzle" or "海龟汤" in Chinese) where players ask yes/no questions to uncover the truth.
- AI Dungeon Master and Judge
- RAG-powered knowledge base
- Hint system and hypothesis validation
- [Echoes-of-Deceit-v2 Repository](https://github.com/Linorman/Echoes-of-Deceit-v2)

## 📁 Project Structure

```
MysterySeek/
├── unified_webui/              # Main unified web interface
│   ├── app.py                  # Streamlit entry point
│   ├── config.py               # Unified configuration
│   ├── i18n.py                 # Internationalization
│   ├── session_state.py        # Session management
│   ├── components.py           # Reusable UI components
│   └── pages/                  # Game pages
│       ├── home.py             # Home/landing page
│       ├── werewolf.py         # AutoWerewolf game page
│       └── turtle_soup.py      # Turtle Soup game page
├── AutoWerewolf/               # Werewolf game submodule (external repo)
└── Echoes-of-Deceit-v2/        # Turtle Soup game submodule (external repo)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Git**
- **[Ollama](https://ollama.ai/)** (for local models) or an OpenAI-compatible API key

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Linorman/MysterySeek.git
cd MysterySeek
```

#### 2. Clone the Game Submodules

Since AutoWerewolf and Echoes-of-Deceit-v2 are stored in separate repositories, you need to clone them:

```bash
# Clone AutoWerewolf
git clone https://github.com/Linorman/AutoWerewolf.git

# Clone Echoes-of-Deceit-v2
git clone https://github.com/Linorman/Echoes-of-Deceit-v2.git

# Or use git submodules
git submodule update --init --recursive
```

#### 3. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate
```
Please note that you can use other environment management tools like Conda if preferred, but please use python 3.12+.
For Conda, create and activate the environment with:
```bash
conda create -n mysteryseek python=3.12 -y
conda activate mysteryseek
```
#### 4. Install Dependencies

```bash
pip install -e "./AutoWerewolf[all]"
pip install -r ./Echoes-of-Deceit-v2/requirements.txt
```

### Configuration

#### Model Configuration

**For Ollama (Local Models):**

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull a model:
   ```bash
   ollama pull qwen3:4b-instruct-2507-q4_K_M
   ollama pull qwen3-embedding:4b
   ```

#### Game-Specific Configuration

- **AutoWerewolf**: Configuration is done through the Web UI or CLI options
- **Echoes-of-Deceit-v2**: Edit `Echoes-of-Deceit-v2/config/models.yaml`:

```yaml
# For Ollama
provider: ollama
ollama:
  base_url: http://localhost:11434
  llm_model_name: llama3
  embedding_model_name: nomic-embed-text

# For OpenAI API
provider: api
api:
  base_url: https://api.openai.com/v1
  api_key: ${OPENAI_API_KEY}
  llm_model_name: gpt-4o-mini
  embedding_model_name: text-embedding-3-small
```

### Running the Application

#### Option 1: Unified WebUI (Recommended)

```bash
# From the MysterySeek root directory
streamlit run unified_webui/app.py
```

Then open your browser at `http://localhost:8501`

#### Option 2: Run Individual Games

**AutoWerewolf CLI:**
```bash
cd AutoWerewolf
autowerewolf run-game --backend ollama --model llama3
```

**AutoWerewolf Web Server:**
```bash
cd AutoWerewolf
autowerewolf serve --host 0.0.0.0 --port 8000
```

**Echoes-of-Deceit CLI:**
```bash
cd Echoes-of-Deceit-v2/src
python play.py list                    # List puzzles
python play.py start <puzzle_id>       # Start a game
```

**Echoes-of-Deceit Web UI:**
```bash
cd Echoes-of-Deceit-v2/src
streamlit run webui/app.py
```

## 🎯 Usage Guide

### Home Page
- View available games
- Select a game to play
- Switch between languages (English/Chinese)

### AutoWerewolf
- **Watch Mode**: Observe AI agents play a complete Werewolf game
- **Play Mode**: Join the game as a human player alongside AI agents
- Configure model settings (Ollama or API, model name, temperature)
- Adjust game rules and role sets

### Echoes of Deceit (Turtle Soup)
- Select from available puzzles
- Ask yes/no questions to uncover the truth
- Use hints when you're stuck
- Propose your hypothesis when ready
- Enable AI player mode to watch the AI solve puzzles

## 🛠️ Development

### Running Tests

```bash
# AutoWerewolf tests
cd AutoWerewolf
pytest tests/

# Echoes-of-Deceit-v2 tests
cd Echoes-of-Deceit-v2
pytest tests/
```
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔗 Related Projects

- [AutoWerewolf](https://github.com/Linorman/AutoWerewolf) - LLM-driven Werewolf Game Agents
- [Echoes-of-Deceit-v2](https://github.com/Linorman/Echoes-of-Deceit-v2) - AI-powered Turtle Soup Game System

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

