# MysterySeek Unified WebUI

A unified Streamlit-based web interface for the MysterySeek game platform, combining **AutoWerewolf** and **Echoes of Deceit (Turtle Soup)** games into a single cohesive application.

## Features

- 🎮 **Single Entry Point**: Choose from multiple games in one unified interface
- 🐺 **AutoWerewolf**: AI-powered Werewolf game with watch and play modes
- 🎭 **Echoes of Deceit**: Lateral thinking puzzle game (Turtle Soup)
- 🌍 **Multi-language Support**: English and Chinese
- 🎨 **Consistent UI/UX**: Unified styling across all games

## Project Structure

```
unified_webui/
├── app.py                 # Main Streamlit entry point
├── config.py              # Unified configuration
├── i18n.py                # Internationalization support
├── session_state.py       # Session state management
├── components.py          # Reusable UI components
├── pages/
│   ├── home.py            # Home/landing page
│   ├── werewolf.py        # AutoWerewolf game page
│   └── turtle_soup.py     # Turtle Soup game page
├── pyproject.toml
└── README.md
```

## Prerequisites

This unified WebUI requires both game projects to be properly installed:

1. **AutoWerewolf** - Located at `../AutoWerewolf`
2. **Echoes-of-Deceit-v2** - Located at `../Echoes-of-Deceit-v2`

## Installation

1. First, install the dependencies for both game projects:

```bash
# Install AutoWerewolf dependencies
cd ../AutoWerewolf
pip install -e .

# Install Echoes of Deceit dependencies
cd ../Echoes-of-Deceit-v2
pip install -r requirements.txt
```

2. Install the unified WebUI dependencies:

```bash
cd ../unified_webui
pip install streamlit nest-asyncio
```

## Running the Application

```bash
# From the unified_webui directory
streamlit run app.py

# Or from the MysterySeek root directory
streamlit run unified_webui/app.py
```

The application will start at `http://localhost:8501`

## Usage

### Home Page
- View available games
- Select a game to play
- Switch between languages

### AutoWerewolf
- **Watch Mode**: Observe AI agents play a complete Werewolf game
- **Play Mode**: Join the game as a human player
- Configure model settings (Ollama or API)
- Adjust game rules and role sets

### Echoes of Deceit (Turtle Soup)
- Select from available puzzles
- Ask yes/no questions to solve the mystery
- Use hints when stuck
- Enable AI player mode to watch the AI solve puzzles

## Configuration

### Language Settings
Switch between English and Chinese using the language selector in the sidebar.

### Model Configuration (AutoWerewolf)
- Backend: Ollama or API
- Model name
- Temperature and max tokens
- Output corrector settings

### Game Settings
- Role set selection (A or B)
- Game language for AI prompts
- Random seed for reproducibility

## Development

### Adding New Games
1. Create a new page in `pages/`
2. Add translations to `i18n.py`
3. Add session state management in `session_state.py`
4. Update the home page and main app routing

### Customizing UI
- Modify `config.py` for styling constants
- Update `components.py` for shared UI elements
- Edit CSS in `config.py` `CSS_STYLES`

## License

MIT License
