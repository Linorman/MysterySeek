"""Unified configuration for MysterySeek platform."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

APP_NAME = "MysterySeek"
APP_VERSION = "1.0.0"
APP_ICON = "🔍"

WEREWOLF_ICON = "🐺"
TURTLE_SOUP_ICON = "🎭"

DEFAULT_LANGUAGE = "en"
DEFAULT_PLAYER_ID = "player"

PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Hide default Streamlit navigation
HIDE_STREAMLIT_STYLE = """
<style>
    /* Hide the default Streamlit header and navigation */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Hide default sidebar navigation (pages list) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hide the hamburger menu */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Hide "Made with Streamlit" footer */
    footer {
        visibility: hidden !important;
    }
    
    /* Hide deploy button */
    .stDeployButton {
        display: none !important;
    }
    
    /* Adjust sidebar top padding */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
</style>
"""

EMOJI_MAP = {
    "yes": "✅",
    "no": "❌",
    "yes_and_no": "⚖️",
    "irrelevant": "🔄",
    "correct": "🎉",
    "partial": "🤔",
    "incorrect": "💭",
    "hint": "💡",
    "player": "🎮",
    "dm": "🎲",
    "thinking": "🤔",
    "puzzle": "🧩",
    "trophy": "🏆",
    "star": "⭐",
    "warning": "⚠️",
    "error": "❌",
    "success": "✅",
    "info": "ℹ️",
    "question": "❓",
    "home": "🏠",
    "settings": "⚙️",
    "history": "📜",
    "game": "🎮",
    "werewolf": "🐺",
    "turtle_soup": "🎭",
}

WEREWOLF_ROLE_ICONS = {
    "werewolf": "🐺",
    "seer": "🔮",
    "witch": "🧙",
    "hunter": "🔫",
    "guard": "🛡️",
    "village_idiot": "🃏",
    "villager": "👤",
    "hidden": "❓",
}


@dataclass
class UISettings:
    show_thinking: bool = False
    auto_scroll: bool = True
    sound_effects: bool = False
    player_agent_mode: bool = False


@dataclass
class WerewolfSettings:
    backend: str = "ollama"
    model_name: str = "qwen3:4b-instruct-2507-q4_K_M"
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    ollama_base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024
    enable_corrector: bool = True
    corrector_max_retries: int = 2
    role_set: str = "A"
    game_language: str = "en"
    random_seed: Optional[int] = None


@dataclass
class TurtleSoupSettings:
    player_id: str = DEFAULT_PLAYER_ID
    display_name: str = ""
    player_agent_mode: bool = False


@dataclass
class PlatformSettings:
    language: str = DEFAULT_LANGUAGE
    current_game: str = "home"
    ui_settings: UISettings = field(default_factory=UISettings)
    werewolf_settings: WerewolfSettings = field(default_factory=WerewolfSettings)
    turtle_soup_settings: TurtleSoupSettings = field(default_factory=TurtleSoupSettings)


CSS_STYLES = """
<style>
    /* ============================================
       Global Styles
       ============================================ */
    
    /* Keep default background for better text readability */
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* ============================================
       Game Cards
       ============================================ */
    
    .game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .game-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .game-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .game-card:hover::before {
        opacity: 1;
    }
    
    .game-card.werewolf {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        box-shadow: 0 4px 15px rgba(26, 26, 46, 0.4);
    }
    
    .game-card.werewolf:hover {
        box-shadow: 0 20px 40px rgba(26, 26, 46, 0.5);
    }
    
    .game-card.turtle-soup {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .game-card.turtle-soup:hover {
        box-shadow: 0 20px 40px rgba(118, 75, 162, 0.5);
    }
    
    .game-card h2 {
        margin: 0 0 0.75rem 0;
        font-size: 1.85rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .game-card h3 {
        margin: 0 0 1rem 0;
        font-size: 1.15rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .game-card p {
        margin: 0;
        opacity: 0.9;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* ============================================
       Puzzle Cards
       ============================================ */
    
    .puzzle-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .puzzle-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .puzzle-card h3 {
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    /* ============================================
       Status Badges
       ============================================ */
    
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }
    
    .status-lobby {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        box-shadow: 0 2px 8px rgba(254, 243, 199, 0.5);
    }
    
    .status-in-progress {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e40af;
        box-shadow: 0 2px 8px rgba(219, 234, 254, 0.5);
    }
    
    .status-completed {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        box-shadow: 0 2px 8px rgba(209, 250, 229, 0.5);
    }
    
    .status-aborted {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        box-shadow: 0 2px 8px rgba(254, 226, 226, 0.5);
    }
    
    /* ============================================
       Verdict Badges
       ============================================ */
    
    .verdict-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .verdict-yes {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
    }
    
    .verdict-no {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
    }
    
    .verdict-yes_and_no {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
    }
    
    .verdict-irrelevant {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        color: #374151;
    }
    
    /* ============================================
       Feature Boxes
       ============================================ */
    
    .feature-box {
        text-align: center;
        padding: 1.75rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-box .icon {
        font-size: 2.75rem;
        margin-bottom: 0.75rem;
        display: block;
        line-height: 1;
        font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", "Segoe UI Symbol", sans-serif;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }
    
    .feature-box .title {
        font-weight: 600;
        font-size: 1rem;
        color: #374151;
    }
    
    /* ============================================
       Commands Panel
       ============================================ */
    
    .command-list {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .command-list code {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-family: 'Fira Code', 'Consolas', monospace;
        font-size: 0.9rem;
        color: #374151;
    }
    
    /* ============================================
       Sidebar Enhancements
       ============================================ */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e5e7eb;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e5e7eb !important;
    }
    
    /* ============================================
       Button Enhancements
       ============================================ */
    
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5a6fd6 0%, #6a4190 100%);
    }
    
    /* ============================================
       Metrics Styling
       ============================================ */
    
    [data-testid="stMetricValue"] {
        font-weight: 700;
        color: #1f2937;
    }
    
    /* ============================================
       Chat Messages
       ============================================ */
    
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 0.5rem;
    }
    
    /* ============================================
       Expander Styling
       ============================================ */
    
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #374151;
    }
    
    /* ============================================
       Divider Styling
       ============================================ */
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
        margin: 1.5rem 0;
    }
</style>
"""
